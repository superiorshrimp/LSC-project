import os
import shutil

MRI_dataset_folder_path = "./dataset"
destination_folder = "./MRI_transformed"

subfolders = ["Testing", "Training"]

for subfolder in subfolders:
    labels = os.listdir(f"{MRI_dataset_folder_path}/{subfolder}")
    os.makedirs(f"{destination_folder}/{subfolder}")
    for label in labels:
        image_names = os.listdir(f"{MRI_dataset_folder_path}/{subfolder}/{label}")
        for index, image_name in enumerate(image_names):
            new_image_name = f"{label}_{index}.jpg"
            shutil.copyfile(f"{MRI_dataset_folder_path}/{subfolder}/{label}/{image_name}", f"{destination_folder}/{subfolder}/{new_image_name}")
    

