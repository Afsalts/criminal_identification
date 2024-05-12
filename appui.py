import streamlit as st
from opencv-python import cv2 # Assuming you have OpenCV installed
import numpy as np
from app import extract_frames,process, get_image_paths,live_process  # Import backend functions
from ultralytics import YOLO
from ultralytics.engine.results import Results
from deepface import DeepFace
from PIL import Image
# import gradio as gr
import shutil
import pandas
import os
import time
def main():
    """Streamlit app for criminal detection in video"""

    st.title("Criminal Detector App")
    st.write("Upload a video file or use your webcam to detect criminals.")

    
    source_option = st.selectbox("Source", ["Video Upload", "Webcam"])

    
    if source_option == "Video Upload":
        uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "avi"])
        if uploaded_file is not None:
           
            video_bytes = uploaded_file.read()
            filename = uploaded_file.name
   
    else:
        video_capture = cv2.VideoCapture(0)  

    
    database = st.text_input("Criminal Image Database Path")
    if not database:
        st.error("Please provide a criminal image database path.")
        return

    
    if st.button("Start Detection"):
       
        output_folder = "output_folder"
        video_folder = "video"
        try:
            os.makedirs(video_folder, exist_ok=True)  
        except OSError as e:
            st.error(f"Error creating folder: {e}")
            return
        try:
            os.makedirs(output_folder, exist_ok=True) 

           
            if source_option == "Video Upload":
                with open(os.path.join("video", filename), "wb") as f:
                    f.write(video_bytes)  # Write video bytes to temporary file
                video_path = os.path.join("video", filename)
                print("video path is")
                print(video_path)
                extract_frames(video_path, output_folder)
                image_paths=get_image_paths(output_folder)
                image=process(image_paths)

                st.image(image)
            else:
                
                while True:
                    ret, frame = video_capture.read()
                    if not ret:
                        break

                    cv2.imwrite(os.path.join(output_folder, f"frame_{time.time()}.jpg"), frame)
                    V=live_process(os.path.join(output_folder, f"frame_{time.time()}.jpg"))
                    if V==True:
                        st.write("KITTI POI")
                        st.image(os.path.join(output_folder, f"frame_{time.time()}.jpg"))
                        break
                    cv2.imshow('Video', frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            

        except Exception as e:
            st.error(f"An error occurred: {e}")
        #finally:
           
            #shutil.rmtree(output_folder, ignore_errors=True) 

  
    if source_option == "Webcam":
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

