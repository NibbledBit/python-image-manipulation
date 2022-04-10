from pathlib import Path
from PIL import Image
import numpy as np
from file_helper import get_image
from image_helper import replace_white_colour, superimpose
from random import randint
import glob
from collections import Counter
import os, shutil

COLOURS = [
    (0xC5, 0x8C, 0x85),
    (0xEC, 0xBC, 0xB4),
    (0xD1, 0xA3, 0xA4),
    (0xA1, 0x66, 0x5E),
    (0x50, 0x33, 0x35),
    (0x59, 0x2F, 0x2A),
]

FOLDERS = [
    # "body",
    "neck",
    "clothes",
    "face",
    "eyes",
    "iris",
    "nose",
    "mouth",
    "facialhair",
    "eyebrows",
    "hair",
    "trait",
]


def main():
    print("Starting...")

    base_dir = "./assets/"
    output_folder = "./output/"

    # Delete directory contents before starting
    for filename in os.listdir(output_folder):
        file_path = os.path.join(output_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))

    # loop around composing the images
    for i in range(100):

        # skin colour randoms
        rnd_skin = randint(0, 5)
        skin_colour = COLOURS[rnd_skin]

        # get a body image
        body_filename = f"./assets/body/body.png"
        body_image = get_image(body_filename)
        # apply body skin colour
        body_image = replace_white_colour(body_image, skin_colour)

        # this is the image we will work on
        working_image = body_image.copy()

        for f in FOLDERS:
            # trait and face hair randoms
            rnd_trait = randint(0, 100)
            rnd_face = randint(0, 100)
            # restrict use of facial hair and optional traits
            restrict_custom = (rnd_trait < 40 and f == "trait") or (
                rnd_face < 75 and f == "facialhair"
            )

            print(f"Folder: {f}")
            print(f"restrict: {restrict_custom}")
            # get random image
            filenames = glob.glob(f"{base_dir}/{f}/*.png")
            print(f"Files: {len(filenames)}")
            random_trait = randint(0, len(filenames) - 1)
            chosen_filename = filenames[random_trait]
            print(f"Applying: {chosen_filename}")

            image_overlay = get_image(chosen_filename)

            # if image is body part, colour it with skin colour
            if f == "face" or f == "neck" or f == "nose" or f == "eyes" or f == "body":
                image_overlay = replace_white_colour(image_overlay, skin_colour)

            if restrict_custom == False:
                working_image = superimpose(working_image, image_overlay)

        # Crop the image
        left = 800
        top = 200
        right = working_image.width - 1000
        bottom = working_image.height - 500
        working_image = working_image.crop((left, top, right, bottom))

        working_image.save(os.path.join(output_folder, f"{i}.png"))

    print("Script complete!")


def get_random_rgb():
    return (randint(0, 255), randint(0, 255), randint(0, 255))


# run main
main()
