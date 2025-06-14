from scipy.spatial import distance
from imutils import face_utils
from playsound import playsound
import imutils
import dlib
import cv2

def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear
	
thresh = 0.25
frame_check = 20
detect = dlib.get_frontal_face_detector()
#predict = dlib.shape_predictor("E:\Github projects\Drowsiness_Detection_fork\shape_predictor_68_face_landmarks.dat")# Dat file is the crux of the code
predict = dlib.shape_predictor(r"C:\Users\Arjun\OneDrive\Desktop\Arjun\Drowsiness-alert-system\Drowsiness_Detection-master\shape_predictor_68_face_landmarks\shape_predictor_68_face_landmarks.dat")# Dat file is the crux of the code


(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
detector = dlib.get_frontal_face_detector()



# cv2.imshow('Result', image_with_landmarks)
# cv2.imwrite('image_with_landmarks.jpg',image_with_landmarks)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


cap=cv2.VideoCapture(0)
flag=0
while True:
	ret, frame=cap.read()
	frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	subjects = detect(gray,0)

	for subject in subjects:
		shape = predict(gray, subject)
		shape = face_utils.shape_to_np(shape)#converting to NumPy Array
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)
		ear = (leftEAR + rightEAR) / 2.0
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
		if ear < thresh:
			flag += 1
			print (flag)
			if flag >= frame_check:
				cv2.putText(frame, "****************ALERT!****************", (10, 30),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				cv2.putText(frame, "****************ALERT!****************", (10,325),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

				print ("Drowsy")
				playsound(r'music.mp3')
		else:
			flag = 0
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(20) & 0xFF
	if key == ord("q"):
		break
cv2.destroyAllWindows()
cap.stop()
