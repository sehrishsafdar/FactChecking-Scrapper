from PIL import Image

def extract_label_from_image():

    image_path = "C:\\Users\\PC\\scrappercode\\sochfactcheck\\did_a_woman_shout_at_nawaz_sharif_and_maryam_nawaz_in_switzerland.png"  # Replace with your image path
    image = Image.open(image_path)
    width, height = image.size
    crop_box = (width - 200, 0, width, 100)  # Adjust these values as per your requirements

    # Crop the image
    cropped_image = image.crop(crop_box)

    # Save the cropped image
    save_path = "C:\\Users\\PC\\scrappercode\\sochfactcheck\\did_a_woman_shout_at_nawaz_sharif_and_maryam_nawaz_in_switzerland.png"  # Path to save the cropped image
    cropped_image.save(save_path)

    print(f"Cropped image saved at: {save_path}")

extract_label_from_image()
