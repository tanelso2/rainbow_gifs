from PIL import Image, ImageChops
import sys

RGBA_MODE = "RGBA"
PALETTE_MODE = "P"

input_file = sys.argv[1]

base_image = Image.open(input_file).convert(RGBA_MODE)

images = []


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


for hue in range(0, 360, 30):
    hsv_string = f"hsv({hue},100%,100%)"
    im = Image.new(RGBA_MODE, base_image.size, hsv_string)
    blended = ImageChops.blend(base_image, im, 0.25)
    composited = ImageChops.composite(blended, base_image, base_image)
    images.append(composited)


#import pdb; pdb.set_trace()

gif_encoder_args = {
    "duration": 60,
    "loop": 0,
    "optimize": False
}

transparency_loc = get_transparency_palette_loc(base_image)
if transparency_loc is not None:
    gif_encoder_args["transparency"] = transparency_loc

output_file = "out/output.gif"

images[0].save(output_file,
               save_all=True,
               append_images=images[1:],
               **gif_encoder_args)
