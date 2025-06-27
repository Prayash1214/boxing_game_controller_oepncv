import cv2
import mediapipe as mp
import math
import pyautogui
import time
import os
cv2.namedWindow("frame",cv2.WINDOW_NORMAL)
time.sleep(1)
os.system("wmctrl -r frame -b add,above")
cap=cv2.VideoCapture(0)

mp_pose=mp.solutions.pose
pose=mp_pose.Pose()
mp_draw=mp.solutions.drawing_utils
def find_angle(p1,p2,p3):
    x1,y1=p1
    x2,y2=p2
    x3,y3=p3
    
    angle= math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
    angle = abs(angle)
    if angle > 180 :
        angle = 360 - angle
    return int(angle)


while True:
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
  
    h,w,c=frame.shape
    frame_rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result=pose.process(frame_rgb)
    if result.pose_landmarks:
        mp_draw.draw_landmarks(frame,result.pose_landmarks,mp_pose.POSE_CONNECTIONS)
        lm=result.pose_landmarks.landmark
        shoulder=lm[12]
        elbow=lm[14]
        wrist = lm[16]
        a_shoulder=lm[11]
        a_elbow=lm[13]
        a_wrist=lm[15]
        nose=lm[0]
        nose_y = int(nose.y*h)
        a_sx,a_sy=int(a_shoulder.x*w),int(a_shoulder.y*h)
        a_ex,a_ey = int(a_elbow.x*w),int(a_elbow.y*h)
        a_wx,a_wy=int (a_wrist.x*w),int (a_wrist.y*h)
        sx,sy=int(shoulder.x*w),int(shoulder.y*h)
        ex,ey = int(elbow.x*w),int(elbow.y*h)
        wx,wy=int (wrist.x*w),int (wrist.y*h)
        cv2.circle(frame,(sx,sy),6,(0,0,0),-1)
        cv2.circle(frame,(ex,ey),6,(0,255,0),-1)
        cv2.circle(frame,(wx,wy),6,(0,0,255),-1)


        cv2.circle(frame,(a_sx,a_sy),6,(0,0,0),-1)
        cv2.circle(frame,(a_ex,a_ey),6,(0,255,0),-1)
        cv2.circle(frame,(a_wx,a_wy),6,(0,0,255),-1)


        cv2.line(frame,(sx,sy),(ex,ey),(0,0,0),2)
        cv2.line(frame,(ex,ey),(wx,wy),(0,0,0),2)


        cv2.line(frame,(a_sx,a_sy),(a_ex,a_ey),(0,0,0),2)
        cv2.line(frame,(a_ex,a_ey),(a_wx,a_wy),(0,0,0),2)

        angle=find_angle((sx,sy),(ex,ey),(wx,wy))
        cv2.putText(frame,f"Angle : {angle}",(ex , ey),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2)

        cv2.putText(frame,f"y_value :{nose_y}",(40,80),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),4)

        
        cv2.putText(frame,f"x_value :{a_sx}",(40,120),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),4)

        a_angle=find_angle((a_sx,a_sy),(a_ex,a_ey),(a_wx,a_wy))
        cv2.putText(frame,f"Angle : {a_angle}",(a_ex , a_ey),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2)

        if ( 160 <= angle <= 180):  # left arm punch
            print("r")
            pyautogui.press('r')
        if (160 <= a_angle <= 180):  # right arm punch 
            print("t")
            pyautogui.press('t')
        if (150 <= nose_y <= 250): # for up and down 
            print("s")
            pyautogui.keyDown('s')
        else:
            print(" ")
            pyautogui.keyUp('s')     
        if (200 <= a_sx <= 299):
            pyautogui.keyDown('a') # for back save 
        else:
            pyautogui.keyUp('a')
        
        


       

        
        
    cv2.imshow("frame",frame)
    
    if cv2.waitKey(1) &0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()