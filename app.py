from flask import Flask, render_template, jsonify, request
from generator import generate_song_titles
import asyncio
from functools import partial
import os

app = Flask(__name__)

models = []
model_dir = "models"
for entry in os.scandir(model_dir):
    if entry.is_dir():
        models += [entry.path]
models.reverse()

@app.route("/")
def song_bot_web():
    return render_template('base.html', models=models)


@app.route('/_do_songs')
async def do_songs():
    # get our parameters from the form
    raw_number = request.args.get('number', 1, type=int)
    number = 10 if raw_number > 10 else raw_number
    prompt = request.args.get('prompt', "", type=str)
    model_name = request.args.get('model_name', "", type=str)
    temperature = request.args.get('temperature', 1.0, type=float)

    # we need to run this asynchronously
    loop = asyncio.get_running_loop()

    # we can't pass parameters to a synchronous function in loop.run_in_executor, so this is a wrapper function
    st = partial(generate_song_titles, number=number,
                 prompt=prompt, temperature=temperature, model_name=model_name)

    # run song title generation asynchronously
    my_result = await loop.run_in_executor(None, st)

    return jsonify(my_result)


@app.route("/history")
def song_bot_history():
    history_file = open('data/history.txt', "r")
    history_data = history_file.read()
    history = history_data.split('\n')
    history.reverse()
    return render_template('history.html', history=history)