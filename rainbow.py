#!/usr/bin/env python

from PIL import Image, ImageChops
import argparse
import sys

print("Starting up")
parser = argparse.ArgumentParser()
parser.add_argument("input_file", type=str, help='The file to rainbowiefy')
parser.add_argument("--blend-amount", "-b", type=float, default=0.25, help='How vibrant the colours are')
parser.add_argument("--hue-rate", "-r", type=int, default=30, help='How fast the colors change')
parser.add_argument("--duration", "-d", type=int, default=60, help='How long the gif is')
parser.add_argument("--optimize", default=False, action='store_true', help='Tell the gif encoder to "optimize" it. Not sure what that means')
parser.add_argument("--disable-transparency", default=False, action='store_true', help='Make the resulting image not have any transparency (not recommended)')
parser.add_argument("--transparency-sensitivity", "-t", type=int, default=1, help='if alpha < sensitivity, make that pixel transparent')
parser.add_argument("--output-file", default="out/output.gif", type=str, help='The file to save the gif to')
parser.add_argument("--pdb", default=False, action='store_true', help='Trips a PDB tracepoint for debugging')
parser.add_argument("--debug", default=False, action='store_true', help='Print debug messages')
args = parser.parse_args()

DEBUG = args.debug
RGBA_MODE = "RGBA"
PALETTE_MODE = "P"

input_file = args.input_file

base_image = Image.open(input_file).convert(RGBA_MODE)

images = []


def get_transparency_palette_loc(img):
    # Too lazy to do conversions right now. Just pass in the right mode
    if img.mode != RGBA_MODE:
        print(f"WARN - img mode was not RGBA_MODE. Actual: {img.mode}")
        return None
    paletted_data = img.convert(PALETTE_MODE).getdata()
    for idx, val in enumerate(img.getdata()):
        alpha = val[3]
        if alpha == 0:
            return paletted_data[idx]
    # If none of the pixels are fully transparent, just give up
    print(f"INFO - none of the pixels were fully transparent")
    return None

def make_all_transparent_into_same_pallete(img, trans_loc, sensitivity=args.transparency_sensitivity):
    palette_img = img.convert(PALETTE_MODE)
    for idx, val in enumerate(img.getdata()):
        alpha = val[3]
        if DEBUG:
            print(f"DEBUG - alpha is {alpha}")
        width, height = palette_img.size
        x,y = divmod(idx, width)
        if alpha < sensitivity:
            palette_img.putpixel((y,x), trans_loc)
    return palette_img.convert(RGBA_MODE)


for hue in range(0, 360, args.hue_rate):
    hsv_string = "hsv({hue},100%,100%)".format(hue=hue)
    im = Image.new(RGBA_MODE, base_image.size, hsv_string)
    blended = ImageChops.blend(base_image, im, args.blend_amount)
    composited = ImageChops.composite(blended, base_image, base_image)
    images.append(composited)


if args.pdb:
    import pdb; pdb.set_trace()

gif_encoder_args = {
    "duration": args.duration,
    "loop": 0,
    "optimize": args.optimize
}

transparency_loc = get_transparency_palette_loc(base_image)
print(f"DEBUG - transparency_loc was {transparency_loc}")
if transparency_loc is not None and not args.disable_transparency:
    images = [make_all_transparent_into_same_pallete(x, transparency_loc) for x in images]
    gif_encoder_args["transparency"] = transparency_loc

print(f"INFO - Printing to {args.output_file}")
images[0].save(args.output_file,
               save_all=True,
               append_images=images[1:],
               **gif_encoder_args)
print("Job's done")
