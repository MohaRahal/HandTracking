#bibliotecas necessarias
import cv2
import mediapipe as mp


#mp.solutions.hands para detectar as maos
mp_hands = mp.solutions.hands
#mp.solutions.drawing_utils para desenhar as maos detectadas
mp_drawing = mp.solutions.drawing_utils


#tamanho da tela que ira mostrar a camera
resolution_X = 1280
resolution_Y = 720

#qual camera sera usada, caso tenha apenas uma entao retorne 0 para a funcao , e caso tenha duas retorne 1 ,
#e assim por diante, caso tenha mais de uma camera conectada ao computador
camera = cv2.VideoCapture(0)

#setando a resolucao da camera
camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolution_X)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution_Y)

#inicializando o detector de maos e setando o numero de maximo de maos que serao detectadas
hands = mp_hands.Hands(max_num_hands=4,)

def find_coord_hand(img,side_invert = False):
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    all_hands = []
    if result.multi_hand_landmarks:
        for hand_side , hand_landmarks in zip(result.multi_handedness, result.multi_hand_landmarks):
            hand_info = {}
            coords = []
            for mark in hand_landmarks.landmark:
                coord_x = int(mark.x * resolution_X)
                coord_y = int(mark.y * resolution_Y)
                coord_z = int(mark.z * resolution_X)
                coords.append((coord_x, coord_y, coord_z))
                hand_info['coordenadas'] = coords
            if side_invert:
                if hand_side.classification[0].label == 'Left':
                    hand_info["side"] = 'Right'
                else:
                    hand_info["side"] = 'Left'
            else:
                hand_info["side"] = hand_side.classification[0].label

            all_hands.append(hand_info)  
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    return img, all_hands



def fingers_raised(hand):
    fingers = []
    for fingerstip in [8, 12, 16, 20]:
        if hand['coordenadas'][fingerstip][1] < hand['coordenadas'][fingerstip - 2][1]:
            #coordenda y e a media do dedo
            fingers.append(True)
        else:
            fingers.append(False)
    return fingers




#loop para mostrar a camera
while camera.isOpened():
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)  # espelhando a imagem da camera
    if not ret:
        print("Frame vazio da camera")
        continue
    #chamando a funcao que detecta as maos e retorna as coordenadas
    img, all_hands = find_coord_hand(frame, False)

    if len(all_hands) == 1:
        info_finger_hand = fingers_raised(all_hands[0])
        print(info_finger_hand)

    cv2.imshow("Camera",img)
    key = cv2.waitKey(1)
    if key == 27:
        break