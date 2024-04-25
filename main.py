import cv2




# Initialize the webcam
print("initializing webcam...")
cap = cv2.VideoCapture(0)
print("webcam initialized")

max_fps = cap.get(cv2.CAP_PROP_FPS)

delay_seconds = 1
buffer_cap = int(max_fps * delay_seconds)
buffer = []
slow_mo = False
show_frame = True

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    buffer.append(frame)

    if len(buffer) > buffer_cap:
        if show_frame:
            cv2.imshow("Webcam", buffer.pop(0))

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("quitting...")        
        cap.release()
        cv2.destroyAllWindows()
        exit(0)

    if cv2.waitKey(1) & 0xFF == ord("s"):
        if not slow_mo:
            print("okay slow mo now")
            slow_mo = True
        else:
            print("back to regs")
            slow_mo = False
            buffer = buffer[:buffer_cap]
            show_frame = True

    if slow_mo:
        show_frame = not show_frame

