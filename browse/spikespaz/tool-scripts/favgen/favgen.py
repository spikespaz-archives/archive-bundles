#! /usr/bin/env python3
from json import load
from subprocess import Popen, call
from argparse import ArgumentParser


DEFAULTS = {
    "config": None,
    "svg": "favicon.svg",
    "png_sizes": [16, 32, 48, 64, 72, 96, 128, 196],
    "ico_sizes": [16, 32],
    "png_name": "out/favicon-{}.png",
    "ico_name": "out/favicon.ico"
}


parser = ArgumentParser(description="Generate favicons from an SVG.")

parser.add_argument("-c", "--config", dest="config", default=DEFAULTS["config"],
                    help="Configuration file with settings to use instead of commands.")
parser.add_argument("-s", "--svg", dest="svg", default=DEFAULTS["svg"],
                    help="Input SVG path to generate icons from.")
parser.add_argument("-ps", "--png-sizes", dest="png_sizes", default=DEFAULTS["png_sizes"], nargs="+", type=int,
                    help="List of sizes (by pixel width) to generate PNG icons for.")
parser.add_argument("-is", "--ico-sizes", dest="ico_sizes", default=DEFAULTS["ico_sizes"], nargs="+", type=int,
                    help="List of PNG icon sizes to embed in the ICO file. Merged with PNG sizes.")
parser.add_argument("-pn", "--png-name", dest="png_name", default=DEFAULTS["png_name"],
                    help="Base filename to use for PNG files. Use '{}' as a variable placeholder for size.")
parser.add_argument("-in", "--ico-name", dest="ico_name", default=DEFAULTS["ico_name"],
                    help="Filename for the generated ICO output file.")

args = vars(parser.parse_args())


if args["config"]:
    print("Configuration: " + args["config"])

    with open(args["config"], "r") as config:
        config = load(config)

        for key, val in args.items():
            if key not in config:
                config[key] = val

        args = config


args["png_sizes"] = tuple(set(args["png_sizes"] + args["ico_sizes"]))


print("\nInput SVG: " + args["svg"] +
      "\nPNG Sizes: " + ", ".join([str(png_size) for png_size in args["png_sizes"]]) +
      "\nPNG Names:\n  " + "\n  ".join([args["png_name"].format(png_size) for png_size in args["png_sizes"]]) +
      "\nICO Name: " + args["ico_name"])


png_queue = []


for png_size in args["png_sizes"]:
    png_queue.append(Popen("inkscape -z {svg} -w {png_size} -e {png_name}".format(
        svg=args["svg"], png_size=png_size,
        png_name=args["png_name"].format(png_size)), shell=True))


for png_cmd in png_queue:
    png_cmd.wait()


call("magick convert {png_names} {ico_name}".format(
    png_names=" ".join([args["png_name"].format(ico_size) for ico_size in args["ico_sizes"]]),
    ico_name=args["ico_name"]), shell=True)
