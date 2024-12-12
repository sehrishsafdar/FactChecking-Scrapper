import cv2
import numpy as np

image_path = "C:\\Users\\PC\\scrappercode\\sochfactcheck\\did_a_woman_shout_at_nawaz_sharif_and_maryam_nawaz_in_switzerland.png"  # Path to the larger image
template_path = "C:\\Users\\PC\\scrappercode\\sfc_templates\\misleading.PNG"  # Path to the template image

# Read the images
image = cv2.imread(image_path)
template = cv2.imread(template_path)
# Get the dimensions of the image and template
image_height, image_width = image.shape[:2]
template_height, template_width = template.shape[:2]

# Resize the template if it's larger than the image
if template_height > image_height or template_width > image_width:
    print("Template is larger than image. Resizing template.")
    template = cv2.resize(template, (image_width, image_height))

# Perform template matching
result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

# Find the location of the best match
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# Set a threshold for a "good" match
threshold = 0.9 # You can adjust this value (between 0 and 1)

# Check if the best match exceeds the threshold
if max_val >= threshold:
    print("Pattern matched!")
    
    # Get the top-left corner of the matching region
    top_left = max_loc
    
    # Get the dimensions of the template
    template_height, template_width = template.shape[:2]

    # Define the bottom-right corner based on template size
    bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

    # Draw a rectangle around the matching area
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

    # Save or display the result
    cv2.imwrite("matched_result.jpg", image)
    cv2.imshow("Matched Result", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Pattern not matched.")