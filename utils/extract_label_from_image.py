import cv2
import numpy as np
from scrappers.sochfactcheck.news_extractor import extract_details
from scrappers.sochfactcheck.crawl_all_news import scrape_all_pages



#image_folder = "sochfactcheck"
#image_path = os.path.join(image_folder, title_to_file_name("Woman doctored into selfie of Maulana Fazlur Rehman and son"))


# TODO: create a function get_image_label 
# which receives an image as an argument and returns its label or None if no lable is found


def get_image_label(save_path):
    #image_path = "sochfactcheck"
    #image = cv2.imread(save_path)
    image = cv2.imread(save_path, cv2.IMREAD_GRAYSCALE)
    template_paths = [
        ("False", r"sfc_templates\false.PNG"),
        ("Misleading", r"sfc_templates\misleading.PNG"),
        ("True", r"sfc_templates\true.PNG")
    ]
   
    scores = []

    for idx, template_path in enumerate(template_paths):
        template = cv2.imread(template_path[1])

        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        scores.append(max_val)
    
    idx = np.argmax(scores)
    return (template_paths[idx][0])
    #print(template_paths[idx][0])
    