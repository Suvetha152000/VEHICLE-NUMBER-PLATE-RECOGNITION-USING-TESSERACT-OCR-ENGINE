import cv2
import pytesseract

# read & display the original img file
car_image = cv2.imread("F:/unnamed1.jpg")
cv2.imshow("1 - Original car_image", car_image)

# find edges of the gray scale img
edged = cv2.Canny(car_image, 170, 200)
cv2.imshow("2 - Edges", edged)

# find contours based on edges
contours, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Create copy of original img to draw all contours
car_image1 = car_image.copy()
cv2.drawContours(car_image1, contours, -1, (0, 255, 0) ,3)
cv2.imshow("3 - All Contours", car_image1)

# sort contours based on their area keeping minimum area as '30'
contours=sorted(contours, key = cv2.contourArea, reverse = True)[:30]
Number_Plate_Contour = None # we currently have no Number plate contour

# top 30 contours
car_image2 = car_image.copy()
cv2.drawContours(car_image2, contours, -1,(0,255,0), 3)
cv2.imshow("4 - Top 30 Contours", car_image2)

# loop over contour to find number plate
count=0
index=6
for c in contours:
    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c,0.02 * perimeter, True)
    # print("approx=",approx)
    if len(approx)==4:  # select the contour with 4 contents
        Number_Plate_Contour = approx

        # crop those contours and store it in cropped img folder
        x,y,w,h=cv2.boundingRect(c)
        new_image=car_image[y:y+h,x:x+w]
        cv2.imwrite('cropped images-text/'+str(index)+'.jpg', new_image)
        index+=1
        break

# drawing the selected contour on the original img
cv2.drawContours(car_image, [Number_Plate_Contour], -1, (0,255,0), 3)
cv2.imshow("5 - Final image with number plate detected", car_image)
Cropped_img = 'Cropped images-text/6.jpg'
cv2.imshow("6 - Cropped license plate Image", new_image)

# use tesseract to convert img into string
pytesseract.pytesseract.tesseract_cmd=r"C:\program files\Tesseract-OCR\tesseract.exe"
text = pytesseract.image_to_string(Cropped_img,lang='eng')

# print(NumberPlate)
print("License plate number is :",text)
cv2.waitKey(0)