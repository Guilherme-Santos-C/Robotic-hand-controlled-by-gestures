import cv2 as cv
import mediapipe as mp
import serial

while True: #Loop para a conexão com o Arduino
    try:  #Tenta se conectar, se conseguir, o loop se encerra
        arduino = serial.Serial('COM6', 9600)
        print('Arduino conectado')
        break
    except:
        pass

webcam = cv.VideoCapture(0)

mp_hands = mp.solutions.hands
Hand = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

if webcam.isOpened():
    verification, frame = webcam.read()
    while verification:
        verification, frame = webcam.read()
        frame_RGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        key_press = cv.waitKey(2) 
        processar_img = Hand.process(frame_RGB)
        hands_points = processar_img.multi_hand_landmarks
        h,w,_ = frame.shape
        points_fingers = []
        if hands_points:
            for hand_landmarks in hands_points:
                mp_draw.draw_landmarks(frame_RGB, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                for id,coords in enumerate(hand_landmarks.landmark):
                    coord_x, coord_y = int(coords.x*w), int(coords.y*h)
                    # cv.putText(frame_RGB, str(id), (coord_x, coord_y+10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
                    points_fingers.append((coord_x,coord_y))
            highs_points_fingers = [8, 12, 16, 20]
            if points_fingers:
                arduino_arr = ["0","0","0","0","0"]
                for i in highs_points_fingers:
                    if points_fingers[i][1] > points_fingers[i-1][1] and points_fingers[i][1] < points_fingers[i-2][1]:
                        print("pouco flexionado")
                        if i == 8:
                            arduino_arr[0] = "1"
                        elif i == 12:
                            arduino_arr[1] = "1"
                        elif i == 16:
                            arduino_arr[2] = "1"
                        elif i == 20:
                            arduino_arr[3] = "1"
                    elif points_fingers[i][1] > points_fingers[i-2][1] and points_fingers[i][1] < points_fingers[i-3][1]:
                        print("metade flexionado")
                        if i == 8:
                            arduino_arr[0] = "2"
                        elif i == 12:
                            arduino_arr[1] = "2"
                        elif i == 16:
                            arduino_arr[2] = "2"
                        elif i == 20:
                            arduino_arr[3] = "2"
                    elif points_fingers[i][1] > points_fingers[i-3][1]:
                        print("totalmente flexionado")
                        if i == 8:
                            arduino_arr[0] = "3"
                        elif i == 12:
                            arduino_arr[1] = "3"
                        elif i == 16:
                            arduino_arr[2] = "3"
                        elif i == 20:
                            arduino_arr[3] = "3"
                    enviar_arduino = "".join(arduino_arr) + "\n"
                    arduino.write(enviar_arduino.encode())
        if key_press == 27:
            break
        cv.imshow("webcam", frame_RGB)
    else:
        arduino.close()
        webcam.release()
        cv.destroyAllWindows()