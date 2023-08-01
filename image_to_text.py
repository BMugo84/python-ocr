import cv2

# load images onto cv2
image_paths = ["anime_test_1.jpg", "anime_test_2.jpg", "anime_test_3.jpg", "anime_test_4.jpg", "anime_test_5.jpg", "anime_test_6.jpg"]
images = [cv2.imread(image_path) for image_path in image_paths]

# get the width and heights of image 1 assumming all image sizes are the same
height, width, _ = images[0].shape

# calculate the y co-ordinates for each line (divided into 3)
x_coordinates = [width // 5 * i for i in range(1, 5)]

# use the y co-ordinates to draw green lines on each image 
for x in x_coordinates:
    for image in images:
        cv2.line(image, (x, 0), (x, height), (0, 255, 0), 2)

# display images with green lines 
for i, img in enumerate(images, start=1):
    cv2.imshow(f"image {i}", img)

cv2.waitKey(0)
cv2.destroyAllWindows()