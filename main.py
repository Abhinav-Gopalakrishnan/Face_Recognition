import cv2
from simple_facerec import SimpleFacerec

#encode faces from folder
sfr=SimpleFacerec()
sfr.load_encoding_images("C:/Users/abhi6/OneDrive/Documents/Face_Recog/images/")


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera at index 1")
    exit()

while True:
    ret, frame = cap.read()


    #Detect faces
    face_locations,face_names = sfr.detect_known_faces(frame)
    for face_loc,name in zip(face_locations,face_names):
        y1,x2,y2,x1=face_loc[0],face_loc[1],face_loc[2],face_loc[3]

        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,200),4)
        cv2.putText(frame,name,(x1,y1-10),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,500),2)


    if not ret or frame is None:
        print("Failed to grab frame")
        break

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27: 
        break

cap.release()
cv2.destroyAllWindows()
