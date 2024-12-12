import cv2
import numpy as np

# Load the images
image_path = "C:\\Users\\PC\\scrappercode\\sochfactcheck\\afghan_singer_hasiba_noori_was_not_killed_in_peshawar.png"  # Source image path
template_path = "C:\\Users\\PC\\scrappercode\\sfc_templates\\false.PNG"  # Template image path

image = cv2.imread(image_path)
template = cv2.imread(template_path)

# Check if images are loaded properly
if image is None or template is None:
    print("Error: One or both images could not be loaded.")
    exit()

# Perform template matching
result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

# Find the location of the best match
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# Get the top-left corner of the matching region
top_left = max_loc

# Get the dimensions of the template
template_height, template_width = template.shape[:2]

# Define the bottom-right corner based on template size
bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

# Draw a rectangle around the matching area (optional)
cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

# Save or display the result
cv2.imwrite("matched_result.jpg", image)  # Save the image with matched pattern
cv2.imshow("Matched Result", image)  # Display the image with the matched pattern
cv2.waitKey(0)
cv2.destroyAllWindows()
