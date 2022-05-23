"Generate gallery index file"

import os
import os.path
import json
import random
import re
from PIL import Image

THUMB_SIZE = (512, 512)
BASEURL = "https://img.gymnewsium.ch/"

def get_img_dimensions(image):
    "Get image dimensions"

    width, height = image.size
    return {"width": width, "height": height, "ratio": width/height}

def fix_image_rotation(image):
    orientation = dict(image.getexif().items())[274]

    if orientation == 3:
        image = image.rotate(180, expand=True)
    elif orientation == 6:
        image = image.rotate(270, expand=True)
    elif orientation == 8:
        image = image.rotate(90, expand=True)
    return image

def get_image_thumbnail(image):
    "Generate thumbnail for the image"

    thumb = image.copy()
    thumb.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
    return thumb

def get_filename_info(filename):
    "Get author and caption from the filename"

    res = re.match(r"([\w ]*) - ([\w\d ]*)(?: - \d*)?\.\w{3,4}", filename).groups()
    author, caption = res

    if caption.isdigit():
        return {
            "author": author,
        }
    return {
        "author": author,
        "caption": caption,
    }

def run(folder):
    "Generate gallery index file and thumbnails for the folder specified"

    print("Started generating...")

    if not os.path.exists(folder):
        raise Exception(f"Folder does not exist: {folder}")

    originalfolder = os.path.join(folder, "original")
    imagefolder = os.path.join(folder, "image")
    thumbnailfolder = os.path.join(folder, "thumbnail")

    os.makedirs(thumbnailfolder, exist_ok=True)
    os.makedirs(imagefolder, exist_ok=True)
    os.makedirs(originalfolder, exist_ok=True)

    title = folder.split(os.path.sep)[-1]
    slug = title.lower().replace(" ", "-")

    images = []

    for filename in os.listdir(originalfolder):
        if not filename.startswith("_") and not filename.startswith("preview"):
            if filename.split(".")[-1].lower() in ["jpeg", "jpg", "png"]:
                originalimgpath = os.path.join(originalfolder, filename)
                imageimgpath = os.path.join(imagefolder, filename)
                thumbnailimgpath = os.path.join(thumbnailfolder, filename)

                image = Image.open(originalimgpath)
                image = fix_image_rotation(image)
                dimensions = get_img_dimensions(image)
                image.save(imageimgpath, optimize=True, quality=75)

                thumbnail = get_image_thumbnail(image)
                thumbnail.save(thumbnailimgpath, optimize=True, quality=75)

                images.append(
                    {
                        "url": BASEURL+slug+"/image/"+filename.replace(" ", "%20"),
                        "thumbnailurl": BASEURL+slug+"/thumbnail/"+filename.replace(" ", "%20"),
                        "dimensions": dimensions,
                        **get_filename_info(filename),
                    }
                )

    while True:
        print(json.dumps(images, indent=4, ensure_ascii=False))
        inp = input("Press r to shuffle, o to sort, q to quit or s to save: (enter to confirm) ")

        if inp == "r":
            random.shuffle(images)
        elif inp == "o":
            key = input("Enter key for sorting: ")
            if key.startswith("-"):
                images.sort(key=lambda x: getattr(x, key.lstrip("-"), ""), reverse=True)
            else:
                images.sort(key=lambda x: getattr(x, key, ""))
        elif inp == "q":
            break
        elif inp == "s":
            data = {
                "title": title,
                "images": images,
            }

            raw = json.dumps(data, indent=4, ensure_ascii=False)

            with open(folder+os.path.sep+"index.json", "w+", encoding="utf-8") as file:
                file.write(raw)


if __name__ == "__main__":
    run(os.getcwd())
