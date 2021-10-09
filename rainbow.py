#!/usr/bin/env python

from PIL import Image, ImageChops, ImageSequence
import argparse
import sys

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
parser.add_argument("--frame-speed", default=1.5, type=float)
parser.add_argument("--disposal", default=2, type=float, help='Honestly not sure what this does')
args = parser.parse_args()
print("Starting up")






DEBUG = args.debug
if DEBUG:
    print("DEBUG - Debug mode on")
RGBA_MODE = "RGBA"
PALETTE_MODE = "P"



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
    rgba_img = img.convert(RGBA_MODE)
    palette_img = img.convert(PALETTE_MODE)
    for idx, val in enumerate(rgba_img.getdata()):
        alpha = val[3]
        width, height = palette_img.size
        x,y = divmod(idx, width)
        if alpha < sensitivity:
            palette_img.putpixel((y,x), trans_loc)
    return palette_img.convert(RGBA_MODE)

def colorize_image(image, hue):
    rgba_image = image.convert(RGBA_MODE)
    hsv_string = f"hsv({hue},100%,100%)"
    im = Image.new(RGBA_MODE, rgba_image.size, hsv_string)
    blended = ImageChops.blend(rgba_image, im, args.blend_amount)
    composited = ImageChops.composite(blended, rgba_image, rgba_image)
    return composited.convert(PALETTE_MODE)


MIN_FRAMES = 12


def get_step_size(num_frames):
    iterations = int((MIN_FRAMES - 1) / num_frames) + 1
    total_frames = iterations * num_frames
    return int(360 / total_frames)

def rainbowify(
        input_file,
        output_file="out/output.gif",
        blend_amount=0.25,
        transparency_sensitivity=1,
        frame_speed=1.5,
        disposal=2.0,
        disable_transparency=False,
        hue_rate=30,
        duration=60,
        optimize=False
        ):
    input_file = input_file

    base_image = Image.open(input_file)
    rgba_base_image = base_image.convert(RGBA_MODE)

    images = []

#import pdb; pdb.set_trace()

    frames = [base_image]
    if base_image.format == 'GIF':
        frames = [frame.copy() for frame in ImageSequence.Iterator(base_image)]

    num_frames = len(frames)

    if DEBUG:
        for f in frames:
            print(f.getpixel((0, 0)))
            print(f.info)
    frame_idx = 0
    for hue in range(0, 360, hue_rate):
        frame_to_color = frames[int(frame_idx) % num_frames]
        frame_idx += frame_speed
        colorized_image = colorize_image(frame_to_color, hue)
        images.append(colorized_image)

    if DEBUG:
        print("_+____)___)__)__)_____")
        for f in images:
            print(f.getpixel((0, 0)))
            print(f.info)


    gif_encoder_args = {
        "duration": duration,
        "loop": 0,
        "optimize": optimize
    }

    transparency_loc = get_transparency_palette_loc(rgba_base_image)
    if DEBUG:
        print(f"DEBUG - transparency_loc was {transparency_loc}")
    if transparency_loc is not None and not disable_transparency:
        images = [make_all_transparent_into_same_pallete(x, transparency_loc) for x in images]
        gif_encoder_args["transparency"] = transparency_loc
        gif_encoder_args["background"] = transparency_loc
        gif_encoder_args["disposal"] = disposal

    print(f"INFO - Printing to {output_file}")
    images[0].save(output_file,
                   save_all=True,
                   append_images=images[1:],
                   **gif_encoder_args)
    print("Job's done")

def main(args):
    rainbowify(
            input_file=args.input_file,
            output_file=args.output_file,
            blend_amount=args.blend_amount,
            transparency_sensitivity=args.transparency_sensitivity,
            frame_speed=args.frame_speed,
            disposal=args.disposal,
            disable_transparency=args.disable_transparency,
            hue_rate=args.hue_rate,
            duration=args.duration,
            optimize=args.optimize

if __name__ == '__main__':
    main(args)
