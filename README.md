# 🎥 Digital Image Processing – Video Editing System  

This project was developed as my **Year 2 – Digital Image Processing Assignment**.  
The program processes **4 input videos** (`street.mp4`, `singapore.mp4`, `traffic.mp4`, `office.mp4`) with multiple automated tasks using:  
<p align="left">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://numpy.org/"><img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy"></a>
  <a href="https://matplotlib.org/"><img src="https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=matplotlib&logoColor=white" alt="Matplotlib"></a>
</p>

## 🚀 Features  

1. **Day/Night Detection & Brightness Adjustment**  
   - Detects brightness using average grayscale values.  
   - Auto-adjusts nighttime videos (+20 brightness).  

2. **Face Blurring (Privacy Protection)**  
   - Uses Haar Cascade Classifier.  
   - Implements smoothing to handle side faces & misdetections.  

3. **Talking Video Overlay**  
   - Overlays `talking.mp4` at **bottom-left corner**.  
   - Green background removed via masking.  

4. **Logo & Watermarks**  
   - Inserts **custom 64×64 logo** at **top-right corner**.  
   - Alternates between `watermark1.png` & `watermark2.png` every 5s.  

5. **Fade Transitions & End Screen**  
   - Fade-in & fade-out effects at start and end.  
   - Appends `endscreen.mp4` with smooth transition.  


## 🛠️ Methodology  

- **Brightness Analysis** → grayscale conversion, pixel averaging (`np.mean`)  
- **Face Detection** → Haar Cascade (`face_detector.xml`) + blur filters  
- **Overlay Techniques** → masking + resizing with `cv2.resize`  
- **Watermark Switching** → alternates via frame count & FPS intervals  
- **Logo Creation** → generated with NumPy & overlayed per frame  
- **Transitions** → alpha blending for fade-in/out effects  


## ⚙️ Setup Guide  

For detailed installation and configuration steps, see the [Setup Guide](https://github.com/ChristinaTUNA/Youtube-Video-Processing/blob/main/Guideline%20to%20run%20the%20code.pdf).
