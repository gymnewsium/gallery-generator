"Generate gallery index file"

import sys
import os
import os.path
import json
import random
from PIL import Image

def get_img_dimensions(img_path):
    "Get image dimensions"

    image = Image.open(img_path)

    w, h = image.size
    return {"width": w, "height": h, "ratio": w/h}

def run(folder):
    "Generate gallery index file for the folder specified"

    if not os.path.exists(folder):
        raise Exception(f"Folder does not exist: {folder}")

    baseurl = "https://img.gymnewsium.ch/"

    title = folder.split(os.path.sep)[-1]
    slug = title.lower().replace(" ", "-")

    files = []

    for filename in os.listdir(folder):
        if not filename.startswith("_") and not filename.startswith("preview"):
            if filename.split(".")[-1].lower() in ["jpeg", "jpg", "png"]:
                imgpath = os.path.join(folder, filename)
                dimensions = get_img_dimensions(imgpath)
                files.append((filename, dimensions))

    images = [
        {
            "url": baseurl+slug+"/"+filename.replace(" ", "%20"),
            "author": filename.split(" - ")[0],
            "dimensions": dimensions,
        } for filename, dimensions in files
    ]

    while True:
        print(json.dumps(images, indent=4, ensure_ascii=False))
        inp = input("Press enter to shuffle, q and enter to quit or s and enter to save: ")

        if inp == "":
            random.shuffle(images)
        elif inp == "q":
            sys.exit()
        elif inp == "s":
            break

    data = {
        "title": title,
        "images": images,
    }

    raw = json.dumps(data, indent=4, ensure_ascii=False)

    with open(folder+os.path.sep+"index.json", "w+", encoding="utf-8") as file:
        file.write(raw)


if __name__ == "__main__":
    run(os.getcwd())
