import cv2
import numpy as np
import matplotlib.pyplot as plt

def read_and_resize_watermark(filepath, size):
    """Read and resize the watermark image."""
    watermark = cv2.imread(filepath, 1)
    return cv2.resize(watermark, size)


def calAvgBrightness(frame_bg, frame_count):
    """Detect day/night time and adjust night time brightness"""  
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame_bg, cv2.COLOR_BGR2GRAY)
    # Calculate the average brightness of all pixels
    avg_brightness = np.mean(gray)
    return avg_brightness

def isDayOrNight(average_brightness_values, frame_bg):
    # Set a threshold to determine daytime or nighttime
    threshold = 100
    # Calculate the overall average brightness for the video
    overall_avg_brightness = np.mean(average_brightness_values)
    if overall_avg_brightness <= threshold:
        # Increase brightness by a factor 
        frame_bg = cv2.add(frame_bg, 20)
        daytime = False 
    else:
        daytime = True
        
    return daytime, frame_bg

def smooth_detection(facedetection_history, current_faces):
    """to smooth face detections"""
    detection_checkerlist = []
    for i in range(len(facedetection_history)):
        for (x, y, w, h) in facedetection_history[i]:
            # Check if the current face is within a certain range of a historical face
            # Use to abs to prevent the result to be negative, coordinate may be negative sometimes
            for (cx, cy, cw, ch) in current_faces:
                if abs(x - cx) < w and abs(y - cy) < h:
                    detection_checkerlist.append((cx, cy, cw, ch))
                    break
            else:
                # If no match found, add historical face
                detection_checkerlist.append((x, y, w, h))
    return detection_checkerlist


def blurface(frame, face_cascade):
    history_length = 5
    facedetection_history = [] 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    facedetection_history.append(faces)
    if len(facedetection_history) > history_length:
        facedetection_history.pop(0)
        
    smooth_detection(facedetection_history, faces)

    # Blur each detected face
    for (x, y, w, h) in faces:
        # Extract the region of the image that contains the face
        faces_region = frame[y:y+h, x:x+w]
        
        # initialize blur region
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 1)

        # Apply a blur to the face region
        blurred_faces = cv2.blur(faces_region, (99, 99), cv2.BORDER_DEFAULT)
        
        # Replace the original face region with the blurred face
        frame[y:y+h, x:x+w] = blurred_faces
    return frame


def overlay_talking(frame_fg, frame_bg, frame_size):
    """Overlay the talking video frame onto the background video frame."""
    frame_fg = cv2.resize(frame_fg, (frame_size[0] // 2, frame_size[1] // 2))
    mask = frame_fg[:, :, 1] <= 240
    frame_bg[-frame_fg.shape[0]:, :frame_fg.shape[1]][mask] = frame_fg[mask]
    return frame_bg


def add_watermark(frame, watermarks):
    """Add the watermark to the frame."""
    wm_gray = cv2.cvtColor(watermarks, cv2.COLOR_BGR2GRAY)
    mask = wm_gray >= 45
    frame[mask] = watermarks[mask]
    return frame


def switch_wm_sec(frame_count, watermarks, target_fps):
    """Switch watermark every segment per 5 seconds"""
    switch_interval_sec = 5
    frames_per_segment = switch_interval_sec * target_fps
    segment_index = (frame_count // frames_per_segment) % len(watermarks)
    watermark = watermarks[segment_index]
    # # for debug purpose
    # if frame_count % frames_per_segment == 0:
    #     print(f"\nSwitching watermark at frame {frame_count} (segment index: {segment_index})")
    return watermark


def add_logo(frame, position):
    """Add the logo to the frame at specified position."""
    logo = cv2.imread("logo.png", 1)
    x_offset, y_offset = position
    height, width = logo.shape[:2]
    if x_offset + width > frame.shape[1]:
        width = frame.shape[1] - x_offset
    if y_offset + height > frame.shape[0]:
        height = frame.shape[0] - y_offset
    frame[y_offset:y_offset + height, x_offset:x_offset + width] = logo
    return frame


def fadeIn_fadeOut(frame, total_no_frames, fps, frame_count):
    fade_frames = int(2 * fps) # fade_duration * fps
    # fade-in effect
    if frame_count < fade_frames:
        alpha = frame_count / fade_frames
        fade_frame = (frame * alpha).astype(np.uint8)
                
    # fade-out effect
    elif frame_count >= total_no_frames - fade_frames:
        alpha = (total_no_frames - frame_count - 1) / fade_frames
        fade_frame = (frame * alpha).astype(np.uint8)
    # Normal frame
    else:
        fade_frame = frame
        
    return fade_frame


def print_progress(frame_count, total_no_frames):
    """Prints the progress as a percentage, replacing the previous output in the terminal."""
    progress = (frame_count / total_no_frames) * 100
    print(f"\rProgress: {progress:.2f}%", end='', flush=True)


def main():
    original_video_path = "street.mp4"
    final_output_path = "processed_video.avi"
    talking_video_path = "talking.mp4"
    end_screen_path = "endscreen.mp4"
    frame_size = (1280, 720)
    watermark_paths = ["watermark1.png", "watermark2.png"]
    target_fps = 30
    logo_position = (frame_size[0] - 170, 110)

    
    # Open video files
    cap_bg = cv2.VideoCapture(original_video_path)
    cap_talking = cv2.VideoCapture(talking_video_path)
    cap_end = cv2.VideoCapture(end_screen_path)
    
    # Load the face cascade classifier
    face_cascade = cv2.CascadeClassifier("face_detector.xml")

    # Create a video writer for the final output
    out = cv2.VideoWriter(final_output_path, cv2.VideoWriter_fourcc(*'MJPG'), target_fps, frame_size)
    
    total_no_frames = int(cap_bg.get(cv2.CAP_PROP_FRAME_COUNT))
    total_no_endframes = int(cap_end.get(cv2.CAP_PROP_FRAME_COUNT))
    fps_main = int(cap_bg.get(cv2.CAP_PROP_FPS))
    print(f"Frame rate of video(FPS): {fps_main}")
    print(f"Total number of frames: {total_no_frames}")
   
    average_brightness_values = []
    
    # Load and resize watermark images
    watermarks = [read_and_resize_watermark(path, frame_size) for path in watermark_paths]

    # Process the main video
    for frame_count in range(total_no_frames):
        success_bg, frame_bg = cap_bg.read()
        success_talking, frame_talking = cap_talking.read()

        if not success_bg :
            print("Error reading background frame")
            break
        
        elif not success_talking:
            cap_talking.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success_talking, frame_talking = cap_talking.read()
            
        # Resize video to 1280x720
        frame_bg = cv2.resize(frame_bg, frame_size)
        
        # Detect and adjust frame brightness
        avg_brightness = calAvgBrightness(frame_bg, frame_count)
        average_brightness_values.append(avg_brightness)
        daytime, frame_bg = isDayOrNight(average_brightness_values, frame_bg)
        
        # Detect and blur faces
        frame_bg = blurface(frame_bg, face_cascade)
        
        # Overlay the talking frame onto the background frame
        frame_bg = overlay_talking(frame_talking, frame_bg, frame_size)

        # Switch watermark every segment(every 5 seconds)
        watermark = switch_wm_sec(frame_count, watermarks, target_fps)

        # Add watermark and logo to the frame
        frame_bg = add_watermark(frame_bg, watermark)
        frame_bg = add_logo(frame_bg, logo_position)
        
        # Apply fade-in fade-out effect 
        frame_bg = fadeIn_fadeOut(frame_bg, total_no_frames, target_fps, frame_count)
        
        # Write the processed frame to the output video
        out.write(frame_bg)
     
        # Print progress
        print_progress(frame_count + 1, total_no_frames)
    
    if daytime == False:
        print('\nNighttime Detected.')
    
    else:
        print('\nDaytime Detected.')
        
    # Plot the histogram of average brightness values
    plt.figure(figsize=(10, 6))
    plt.hist(average_brightness_values, bins=256, range=(0, 255))
    plt.title('Histogram of Average Brightness Values')
    plt.xlabel('Average Brightness')
    plt.ylabel('Frequency')
    plt.show()     
    

    # Process and append the end screen video
    for frame_count in range(total_no_endframes):
        success_end, frame_end = cap_end.read()
        
        if not success_end:
            break
        
        # Resize video to 1280x720
        frame_end = cv2.resize(frame_end, frame_size)
        
        # Apply fade-in fade-out effect
        frame_end = fadeIn_fadeOut(frame_end, total_no_endframes, target_fps, frame_count)
        out.write(frame_end)
        

    cap_bg.release()
    cap_talking.release()
    cap_end.release()
    out.release()
    cv2.destroyAllWindows()
    print("\nVideo processing completed successfully.")

if __name__ == "__main__":
    main()
