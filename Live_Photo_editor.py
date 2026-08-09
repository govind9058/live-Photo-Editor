import cv2
import numpy as np
from tkinter import Tk  #----GUI Library of py
from tkinter.filedialog import asksaveasfilename 
from tkinter import filedialog

#-------------------------choose image from Pc

file_path = filedialog.askopenfilename(
    title="Choose Image",
    filetypes=[
        ("Image Files", "*.jpg *.jpeg *.png *.bmp")
    ]
)

image = cv2.imread(file_path)
original = cv2.imread(file_path)

if original is None:
    print("Image not found!")
    exit()

# --------------Original image (Reset ke liye)
master = original.copy()
original = original.copy()

# ----------------------Window ka name
window_name = "Live Photo Editor"

#-----------------------Create Another window to show Buttons

BUTTONS = np.zeros((300, 400, 3), dtype=np.uint8)

cv2.putText(BUTTONS, "BUTTONS", (70, 35),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

keys = [
    "H = Flip Horizontal",        "V = Flip Vertical",
    "R = Rotate 90",              "G = Grayscale",
    "O = Reset Original",         "U = Undo / Redo",
    "S = Save Image",             "Q = Quit"
]

y = 70
for text in keys:
    cv2.putText(BUTTONS, text, (30, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,255,255), 1)
    y += 28

cv2.namedWindow(window_name)
cv2.WINDOW_NORMAL
cv2.imshow("Shortcuts", BUTTONS)





# Slider Function
# slider ke liye empty / callback funtion 
# slider jb move krta h to vo function ko call back krta h
def nothing(x):
    pass

cv2.namedWindow(window_name)


# Brightness Slider
cv2.createTrackbar("Brightness", window_name, 50, 100, nothing)

# Contrast Slider
cv2.createTrackbar("Contrast", window_name, 10, 30, nothing)

# Saturation Slider
cv2.createTrackbar("Saturation", window_name, 100,200, nothing)

# Blur Slider

cv2.createTrackbar("Blur",window_name, 0,20, nothing)

# Sharpen slider

cv2.createTrackbar("Sharpen",window_name, 0,10, nothing)

# Undo Redo funtion
def show_comparison(master, display):

    height = min(master.shape[0], display.shape[0])

    master = cv2.resize(
        master,
        (int(master.shape[1] * height / master.shape[0]), height)
    )

    display = cv2.resize(
        display,
        (int(display.shape[1] * height / display.shape[0]), height)
    )

    comparison = np.hstack((master, display))

    cv2.imshow("Original | Edited", comparison)

while True:
# ---------------- Brightness Slider ----------------
 brightness = cv2.getTrackbarPos("Brightness", window_name) - 50

# ---------------- Contrast Slider ----------------
 contrast = cv2.getTrackbarPos("Contrast", window_name)

# ---------------- Saturation Slider ----------------
 saturation = cv2.getTrackbarPos("Saturation", window_name)

 #----------------Blur Slider-------------------------
 
 blur =cv2.getTrackbarPos("Blur",window_name)

 #--------------Sharpen slider------------------

 sharpen =cv2.getTrackbarPos("Sharpen",window_name) 

# Start from current image
 display = original.copy()

# ---------------- Apply Brightness ----------------
 display = np.clip(
    display.astype(np.int16) + brightness,
    0,
    255
).astype(np.uint8)

# ---------------- Apply Contrast ----------------
 display = np.clip(
    display.astype(np.float32) * (contrast / 10),
    0,
    255
).astype(np.uint8)

# ---------------- Apply Saturation ----------------
# h= hue (color type)
# s = saturation
# v = value
 hsv = cv2.cvtColor(display, cv2.COLOR_BGR2HSV)

 h, s, v = cv2.split(hsv)

 s = np.clip(
    s.astype(np.float32) * (saturation / 100), #change value of saturation (pixel)
    0,
    255
).astype(np.uint8)

 hsv = cv2.merge((h, s, v))

 display = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR) 

 #-------------- Apply Blur ---------------------
 if blur>0:
       kernel = blur*2+1
       display = cv2.GaussianBlur(display,(kernel,kernel),0)


#--------------- Apply Sharpen ---------------------------

 if sharpen>0:
    kernel= np.array([[0,-1,0],
                   [-1,5 + sharpen,-1],
                   [0,-1,0]],dtype=np.float32)
    display= cv2.filter2D(display,-1,kernel)



    
# ---------------- Show ----------------

 cv2.namedWindow(window_name)
 cv2.WINDOW_NORMAL
 cv2.imshow(window_name, display)


   #--------------------- Keyboard Input
 key = cv2.waitKey(1) 

 # ---------------- Horizontal Flip
 if key == ord('h'):
        original = cv2.flip(original, 1)
        print("Horizontal Flip")

    # ---------------- Vertical Flip
 elif key == ord('v'):
        original = cv2.flip(original, 0)
        print("Vertical Flip")

    # ---------------- Rotate by 90
 elif key == ord('r'):
        original = cv2.rotate(original, cv2.ROTATE_90_CLOCKWISE)
        print("Rotated")

    # ---------------- Grayscale(Black and White)
 elif key == ord('g'):
        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        original = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        print("Grayscale")

    # ---------------- Reset
 elif key == ord('o'):
        original = master.copy()
        cv2.setTrackbarPos("Brightness", window_name, 50)
        cv2.setTrackbarPos("Contrast", window_name, 10)
        cv2.setTrackbarPos("Saturation", window_name, 100)
        cv2.setTrackbarPos("Blur", window_name, 0)
        cv2.setTrackbarPos("Sharpen", window_name, 0)
        print("Image Reset")

    # -----------------UNdo/Redo for comparison

 elif key == ord('u'):
    show_comparison(master, display)

    # ---------------- Save image by using Tkinter library ( GUI ) of python
 elif key == ord('s'):

    root = Tk()
    root.withdraw()

    file_path = asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[
            ("JPEG Image", "*.jpg"),
            ("PNG Image", "*.png"),
            ("All Files", "*.*")
        ]
    )

    if file_path:
        cv2.imwrite(file_path, display)
        print("Image Saved Successfully")
    else:
        print("Save Cancelled")

    # ---------------- Quit
 elif key == ord('q'):
        print("Closing Editor...")
        break

cv2.destroyAllWindows()