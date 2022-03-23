"Generate gallery index file"

import os
import os.path
import json
from PIL import Image

def run(folder):
    "Generate gallery index file for the folder specified"

    if not os.path.exists(folder):
        raise Exception(f"Folder does not exist: {folder}")

    baseurl = "https://img.gymnewsium.ch/"

    title = folder.split(os.path.sep)[-1]
    slug = title.lower().replace(" ", "-")

    files = []

    for filename in os.listdir(folder):
        if filename.split(".")[-1].lower() in ["jpeg", "jpg", "png"]:
            imgpath = os.path.join(folder, filename)
            im = Image.open(imgpath)
            h, w = im.size
            files.append((filename, {"height": h, "width": w, "ratio": w/h}))

    data = {
        "title": title,
        "images": [
            {
                "url": baseurl+slug+"/"+filename.replace(" ", "%20"),
                "author": filename.split(" - ")[0],
                "dimensions": dimensions,
            } for filename, dimensions in files
        ]
    }

    raw = json.dumps(data, indent=4, ensure_ascii=False)

    print(raw)

    input("Press enter to write...")

    with open(folder+os.path.sep+"index.json", "w+", encoding="utf-8") as file:
        file.write(raw)


if __name__ == "__main__":
    run(os.getcwd())
