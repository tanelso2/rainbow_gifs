from PIL import Image, ImageChops, ImageSequence
import sys

RGBA_MODE = "RGBA"
PALETTE_MODE = "P"

input_file = sys.argv[1]

base_image = Image.open(input_file)
rgba_base_image = base_image.convert(RGBA_MODE)

images = []

#import pdb; pdb.set_trace()

frames = [base_image]
if base_image.format == 'GIF':
    frames = [frame.copy() for frame in ImageSequence.Iterator(base_image)]

num_frames = len(frames)

for f in frames:
    print(f.getpixel((0, 0)))
    print(f.info)


def get_transparency_palette_loc(img):
    # Too lazy to do conversions right now. Just pass in the right mode
    if img.mode != RGBA_MODE:
        return None
    paletted_data = img.convert(PALETTE_MODE).getdata()
    for idx, val in enumerate(img.getdata()):
        alpha = val[3]
        if alpha == 0:
            return paletted_data[idx]
    # If none of the pixels are fully transparent, just give up
    return None


def colorize_image(image, hue):
    rgba_image = image.convert(RGBA_MODE)
    hsv_string = f"hsv({hue},100%,100%)"
    im = Image.new(RGBA_MODE, rgba_image.size, hsv_string)
    blended = ImageChops.blend(rgba_image, im, 0.5)
    composited = ImageChops.composite(blended, rgba_image, rgba_image)
    return composited.convert(PALETTE_MODE)


MIN_FRAMES = 12


def get_step_size(num_frames):
    iterations = int((MIN_FRAMES - 1) / num_frames) + 1
    total_frames = iterations * num_frames
    return int(360 / total_frames)


frame_idx = 0
for hue in range(0, 360, get_step_size(num_frames)):
    frame_to_color = frames[frame_idx % num_frames]
    frame_idx += 1
    colorized_image = colorize_image(frame_to_color, hue)
    images.append(colorized_image)

print("_+____)___)__)__)_____")
for f in images:
    print(f.getpixel((0, 0)))
    print(f.info)

import pdb; pdb.set_trace()

gif_encoder_args = {
    "duration": 60,
    "loop": 0,
    "optimize": False
}

transparency_loc = get_transparency_palette_loc(rgba_base_image)
# if transparency_loc is not None:
#     gif_encoder_args["transparency"] = transparency_loc
#     gif_encoder_args["background"] = transparency_loc
#     gif_encoder_args["disposal"] = 2

output_file = "out/output.gif"

images[0].save(output_file,
               save_all=True,
               append_images=images[1:],
               background=22,
               disposal=2,
               **gif_encoder_args)
