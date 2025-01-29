import cv2
import numpy as np
import matplotlib.pyplot as plt

def extract_bars_from_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bar_heights = []

    for contour in contours:
        # Calculate the bounding box of each contour
        x, y, w, h = cv2.boundingRect(contour)
        bar_heights.append(h)  # Get height as the value of the bar

    # Sort bars by their position on the x-axis (optional)
    bar_heights = np.array(sorted(bar_heights))
    return bar_heights

# Call the function to extract data from image
bar_heights = extract_bars_from_image('image.png')
print(bar_heights)

# Optionally, visualize the bars
plt.bar(range(len(bar_heights)), bar_heights)
plt.show()
