 View online at https://rainbowgifs.com

# Example usage
```bash
./rainbow.py examples/void.png \
    --output-file=examples/outputs/party_void.gif \
    --duration=120 \
    --hue-rate=15 \
    --blend-amount=0.5
```

# Getting the Code

```bash
git clone https://github.com/tanelso2/rainbow_gifs

cd rainbow_gifs
```

# Setup

```bash

python3 -m venv rainbow_gif_venv
source rainbow_gif_venv/bin/activate

pip install -r requirements.txt
```

# Running

```bash
./rainbow.py -h
usage: rainbow.py [-h] [--blend-amount BLEND_AMOUNT] [--hue-rate HUE_RATE]
                  [--duration DURATION] [--optimize] [--disable-transparency]
                  [--transparency-sensitivity TRANSPARENCY_SENSITIVITY]
                  [--output-file OUTPUT_FILE] [--pdb] [--debug]
                  input_file

positional arguments:
  input_file            The file to rainbowiefy

optional arguments:
  -h, --help            show this help message and exit
  --blend-amount BLEND_AMOUNT, -b BLEND_AMOUNT
                        How vibrant the colours are
  --hue-rate HUE_RATE, -r HUE_RATE
                        How fast the colors change
  --duration DURATION, -d DURATION
                        How long the gif is
  --optimize            Tell the gif encoder to "optimize" it. Not sure what that
                        means
  --disable-transparency
                        Make the resulting image not have any transparency (not
                        recommended)
  --transparency-sensitivity TRANSPARENCY_SENSITIVITY, -t TRANSPARENCY_SENSITIVITY
                        if alpha < sensitivity, make that pixel transparent
  --output-file OUTPUT_FILE
                        The file to save the gif to
  --pdb                 Trips a PDB tracepoint for debugging
  --debug               Print debug messages
```
