import cv2
import time
import numpy as np
import ModuleHandTracking as htm
import math
import pyautogui  # keyboard

################################
wCam, hCam = 1024, 768
################################

# Inisialisasi variabel untuk mendeteksi gerakan swipe
previous_hand_x = 0
swipe_threshold = 100  # Jarak minimum untuk mendeteksi swipe
cooldown_time = 1  # Waktu cooldown dalam detik untuk mencegah multiple swipes
last_action_time = 0
action_ready = True  # Flag untuk melacak apakah action dapat dideteksi

# Inisialisasi kamera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

# Inisialisasi hand detector
detector = htm.handDetector(detectionCon=0.7)

# Status presentasi
presentation_active = False

# Konfigurasi tampilan
action_status = "None"

# Threshold untuk gesture pinch (jarak antara jempol dan telunjuk)
pinch_threshold = 40  # Jarak dalam pixel

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        break
    
    # Flip image untuk tampilan mirror
    img = cv2.flip(img, 1)
    
    # Deteksi tangan
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)

    # Hitung waktu sejak aksi terakhir
    current_time = time.time()
    time_since_last_action = current_time - last_action_time
    
    # Reset cooldown jika waktu sudah berlalu
    if time_since_last_action > cooldown_time:
        action_ready = True

    if len(lmList) > 8: 
        
        # Start and End Presentation
        # Ambil posisi jari jempol (4) dan telunjuk (20)
        x1, y1 = lmList[4][1], lmList[4][2]
        startX, startY = lmList[20][1], lmList[20][2]
        cx, cy = (x1 + startX) // 2, (y1 + startY) // 2

        # Swipe Right
        rightX, rightY = lmList[8][1], lmList[8][2]

        # Swipe Left
        leftX, leftY = lmList[12][1], lmList[12][2]
        
        # Gambar lingkaran di ujung jari untuk visualisasi
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)

        cv2.circle(img, (startX, startY), 10, (255, 0, 255), cv2.FILLED)

        cv2.circle(img, (rightX, rightY), 10, (255, 0, 0), cv2.FILLED)

        cv2.circle(img, (leftX, leftY), 10, (255, 255, 0), cv2.FILLED)
        
        cv2.line(img, (x1, y1), (startX, startY), (255, 0, 255), 2)

        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        
        # Hitung jarak antara jempol dan telunjuk
        lengthStartEnd = math.hypot(startX - x1, startY - y1)
        lengthRight = math.hypot(rightX - x1, rightY - y1)
        lengthLeft = math.hypot(leftX - x1, leftY - y1)

        # Deteksi gesture pinch untuk memulai/mengakhiri presentasi
        if lengthStartEnd < pinch_threshold and action_ready:
            if not presentation_active:
                print("Starting Presentation")
                pyautogui.press('f5')  # Memulai slideshow
                presentation_active = True
                action_status = "Starting Presentation"

            else:
                print("Ending Presentation")
                pyautogui.press('escape')  # Mengakhiri slideshow
                presentation_active = False
                action_status = "Ending Presentation"
            last_action_time = current_time
            action_ready = False
        
        if presentation_active:
            if lengthRight < pinch_threshold and action_ready:
                    print("Next Slide")
                    pyautogui.press('right')  # Tekan tombol kanan untuk next slide
                    action_status = "Next Slide"
                    last_action_time = current_time
                    action_ready = False

            if lengthLeft < pinch_threshold and action_ready:
                print("Previous Slide")
                pyautogui.press('left')  
                action_status = "Previous Slide"
                last_action_time = current_time
                action_ready = False
        
    # Tampilkan status aksi terakhir
    cv2.putText(img, f'Action: {action_status}', (40, 110), cv2.FONT_HERSHEY_COMPLEX,
                0.7, (255, 0, 0), 2)
    
    # Tampilkan status presentasi
    status_text = "Active" if presentation_active else "Inactive"
    cv2.putText(img, f'Presentation: {status_text}', (40, 140), cv2.FONT_HERSHEY_COMPLEX,
                0.7, (255, 0, 0), 2)
                
    # Tampilkan petunjuk di layar
    cv2.putText(img, "Gestures:", (400, 50), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 0, 0), 1)
    cv2.putText(img, "- Swipe kiri: Next slide", (400, 80), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
    cv2.putText(img, "- Swipe kanan: Prev slide", (400, 110), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
    cv2.putText(img, f"- Tempel Ibu jari dengn Telunjuk: Start/End", (40, 200), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 2)

    cv2.imshow("PowerPoint Hand Controller", img)

    # Tombol 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()