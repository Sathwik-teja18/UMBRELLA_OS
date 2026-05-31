import os
import cv2
from deepface import DeepFace
from settings import BIOMETRICS_DIR

def capture_face(emp_id="temp"):
    """
    Initializes the webcam, draws a targeting grid, and captures a frame
    when the user presses SPACE.
    """
    cap = cv2.VideoCapture(0)
    saved_path = None
    
    if not os.path.exists(BIOMETRICS_DIR): 
        os.makedirs(BIOMETRICS_DIR)
        
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        height, width, _ = frame.shape
        
        # Draw the Umbrella Targeting Grid
        cv2.rectangle(frame, (width//4, height//4), (width*3//4, height*3//4), (0, 0, 255), 2)
        cv2.putText(frame, "ALIGN FACE IN GRID", (width//4, height//4 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(frame, "PRESS 'SPACE' TO INITIATE SCAN", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        cv2.imshow("UMBRELLA CORP // BIOMETRIC SCANNER", frame)
        
        key = cv2.waitKey(1)
        if key == 32:  # Spacebar pressed
            file_name = f"{emp_id}_scan.jpg"
            saved_path = os.path.join(BIOMETRICS_DIR, file_name)
            cv2.imwrite(saved_path, frame)
            break
        elif key == 27:  # Escape key pressed
            break
            
    cap.release()
    cv2.destroyAllWindows()
    return saved_path