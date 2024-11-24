import os
import shutil
from random import randint, random, shuffle, choice
from time import sleep

IMAGES_PER_MINUTE = 60
SOURCE_DIR = "dataset/iris/"
DESTINATION_DIR = "data/"

def main():
    while True:
        timestamps = {second : 0 for second in range(60)}
        for _ in range(IMAGES_PER_MINUTE):
            timestamps[randint(0,59)] += 1

        for i in range(60):
            count = timestamps[i]
            images = get_images_to_send(count)
            send_images(images)
            sleep(1)

def get_images_to_send(count):
    return [choice(os.listdir(SOURCE_DIR)) for _ in range(count)]

def send_images(images):
    for image in images:
        # windows below; for linux use: os.popen('cp source.txt destination.txt')
        try:
            result = shutil.copy(SOURCE_DIR + image, DESTINATION_DIR + image)
            print(result)
        except:
            print("copying file failed (possibly file already there)")

if __name__ == "__main__":
    # del data/*
    # copy iris-setosa/* dataset/iris/
    # copy iris-versicolour/* dataset/iris/
    # copy iris-virginica/* dataset/iris/
    main()
