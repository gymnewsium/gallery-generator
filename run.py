"Generate gallery index file"
import os
import os.path
import json

def run(folder):
    "Generate gallery index file for the folder specified"

    if not os.path.exists(folder):
        raise Exception(f"Folder does not exist: {folder}")

    baseurl = "https://img.gymnewsium.ch/"

    title = folder.split(os.path.sep)[-1]
    slug = title.lower().replace(" ", "-")

    files = []

    for file in os.listdir(folder):
        if file.split(".")[-1].lower() in ["jpeg", "jpg", "png"]:
            files.append(file)

    data = {
        "title": title,
        "images": [
            {
                "url": baseurl+slug+"/"+filename.replace(" ", "%20"),
                "author": filename.split(" - ")[0]
            } for filename in files
        ]
    }

    raw = json.dumps(data, indent=4, ensure_ascii=False)

    print(raw)

    input("Press enter to write...")

    with open(folder+os.path.sep+"index.json", "w+", encoding="utf-8") as file:
        file.write(raw)


if __name__ == "__main__":
    run(os.getcwd())
