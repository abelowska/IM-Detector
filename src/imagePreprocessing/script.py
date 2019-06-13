import os
from collections import Counter

from src.imagePreprocessing.tickBarsDetector import ImageResizerFactory
from src.imagePreprocessing.annotationsRemover import AnnotationRemoverCreator
import matplotlib.pyplot as plt


path = ''

files_list = os.listdir(path)  # returns list
image_resizer = ImageResizerFactory().columbia_images()
ticks = []

for file in files_list:
    image = image_resizer.read_image(path + file)
    # cv2.imshow("Image", my_image)
    # cv2.waitKey(0)
    roi = image_resizer.crop_ticks_bar_area(image)
    thresh_image = image_resizer.threshold_image(roi)
    coordinates = image_resizer.find_white_points(thresh_image)
    tick = image_resizer.calculate_tick(coordinates)
    image_resizer.save_bar_tick(path + file, tick)

    ticks.append(tick)

diffs_dict = Counter(ticks)
default_bar_tick = diffs_dict.most_common(1)[0][0]
print(default_bar_tick)

annotation_remover = AnnotationRemoverCreator.columbia_annotations()

for file in files_list:
    image = annotation_remover.read_image(path + file)
    my_coordinates = annotation_remover.find_roi(image)
    image = annotation_remover.crop_image(image, my_coordinates)
    image, pixels = annotation_remover.find_annotations_with_neighbourhood(image=image)
    image = annotation_remover.restore_gaps(image=image, pixels_with_bad_neighbours=pixels)

    metadata_tick = image_resizer.read_tick(path + file)
    image = image_resizer.resize(metadata_tick, default_bar_tick, image)
    image_resizer.save_image(image, path + file)



