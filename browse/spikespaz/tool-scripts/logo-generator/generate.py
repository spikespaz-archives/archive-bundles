from PIL import Image, ImageDraw, ImageFont
from json import load
import os
from shutil import rmtree


class Dict:
    def __init__(self, dictionary):
        self.__dict__ = dictionary


print("Loading settings into dictionary literal object.")
settings = Dict(load(open("settings.json")))


print("Defining supersample sizes.")
base = settings.base[0] * 3, settings.base[1] * 3
size = settings.size


if os.path.isdir("out"):
    print("Out directory exists, deleting.")
    rmtree("out")

print("Creating out directory.")
os.mkdir("out")


def generate(text, font):
    print("Creating logo supersample.")
    logo = Image.new("RGBA", base)
    print("Creating drawing context.")
    draw = ImageDraw.Draw(logo)

    displacement = 0

    for region in text:
        print("Drawing region with displacement " + str(displacement) + ".")
        draw.text((displacement, 0), region["text"], font=font, fill=tuple(region["color"]))
        displacement += draw.textsize(region["text"], font=font)[0]

    print("Resizing, cropping and antialiasing.")
    logo = logo.resize(tuple(settings.base), Image.ANTIALIAS)
    logo = logo.crop(logo.getbbox())

    final_size = logo.width + settings.padding[0] * 2, logo.height + settings.padding[1] * 2

    print("Creating background and layering.")
    image = Image.new("RGBA", final_size, tuple(settings.background))
    image.paste(logo, (settings.padding[0], settings.padding[1]), logo)

    return(image)


for path, dirs, files in os.walk("fonts"):
    for file in files:
        if file.endswith(".ttf"):
            print(os.path.join(path, file) + " is a font, processing.")
            name = file.replace(".ttf", "").rsplit("-", 1)
            weight = "Regular"

            if len(name) > 1:
                weight = name[1]
                name = name[0]

            if weight in settings.weights:
                print("Font weight is acceptable, continue.")
                font = ImageFont.truetype(os.path.join(path, file), size)
                generate(settings.text, font).save(os.path.join("out", file.replace(".ttf", "-" + "".join(
                    [region["text"] for region in settings.text]) + ".png")))
            else:
                print("Font weight not acceptable, skipping.")

        else:
            print(os.path.join(path, file) + " is not a font, skipping.")
