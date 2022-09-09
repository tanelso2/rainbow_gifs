from flask import Flask, render_template, request, url_for, flash, redirect
from rainbow import rainbowify
import os
import logging
import random
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

params = [{'name': 'blend_amount',
           'type': float,
           'default': 0.25,
           'min': 0.0,
           'max': 1.0,
           'help': 'How vibrant the rainbow colors should be'},
          {'name': 'hue_rate',
           'type': int,
           'default': 30,
           'min': 5,
           'max': 100,
           'help': 'How fast the colors change'},
          {'name': 'duration',
           'type': int,
           'default': 60,
           'min': 5,
           'max': 300,
           'help': 'How long the gif should be'}
         ]

def random_name():
    return os.urandom(12).hex()

def path_for(id):
    output_filename = f"{id}.gif"
    output_path = os.path.join('static', 'images', 'output', output_filename)
    return output_path

examples_dir = os.path.join('static', 'images', 'examples')

def get_examples():
    possible_examples = []
    with os.scandir(examples_dir) as it:
        for x in it:
            if x.is_dir():
                in_file = os.path.join(examples_dir, x.name, "in.png")
                out_file = os.path.join(examples_dir, x.name, "out.gif")
                if os.path.isfile(in_file) and os.path.isfile(out_file):
                    possible_examples.append({"in": in_file, "out": out_file})
    return possible_examples
            


@app.route('/')
def index():
    all_examples = get_examples()
    random.shuffle(all_examples)
    how_many = 2
    examples = all_examples[0:how_many]

    return render_template('index.html', examples=examples)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        inputfile = request.files['inputfile']
        logging.info(f'{inputfile=}')
        logging.info(f'{type(inputfile)=}')
        print(f'{inputfile=}')
        print(f'{type(inputfile)=}')
        blend_amount = float(request.form['blend_amount'])
        hue_rate = int(request.form['hue_rate'])
        duration = int(request.form['duration'])
        print(f'{hue_rate=}')
        print(f'{blend_amount=}')
        print(f'{duration=}')

        if not inputfile:
            flash('FILE is required!')
        else:
            id = random_name()
            output_path = path_for(id)
            # TODO: Some checks on the inputfile
            rainbowify(inputfile, output_file=output_path, blend_amount=blend_amount, hue_rate=hue_rate, duration=duration)
            return redirect(url_for('display', id=id))
    return render_template('create.html', params=params)

@app.route('/display/<id>')
def display(id):
   return render_template('display.html', image_path=path_for(id))
