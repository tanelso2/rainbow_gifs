from flask import Flask, render_template, request, url_for, flash, redirect
from rainbow import rainbowify
import os
import logging

app = Flask(__name__)

messages = [{'title': 'Message One',
             'content': 'Message One Content'}]

def random_name():
    return os.urandom(12).hex()

def path_for(id):
    output_filename = f"{id}.gif"
    output_path = os.path.join('static', 'output', output_filename)
    return output_path

@app.route('/')
def index():
    return render_template('index.html', messages=messages)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        inputfile = request.files['inputfile']
        logging.info(f'{inputfile=}')
        logging.info(f'{type(inputfile)=}')
        print(f'{inputfile=}')
        print(f'{type(inputfile)=}')

        if not inputfile:
            flash('FILE is required!')
        else:
            id = random_name()
            output_path = path_for(id)
            # TODO: Some checks on the inputfile
            rainbowify(inputfile, output_file=output_path)
            return redirect(url_for('display', id=id))
    return render_template('create.html')

@app.route('/display/<id>')
def display(id):
   return render_template('display.html', image_path=path_for(id))
