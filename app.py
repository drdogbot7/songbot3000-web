from flask import Flask, render_template, jsonify, request
from generator import generate_song_titles
import asyncio
from functools import partial

app = Flask(__name__)

# songs = generate_song_titles()


@app.route("/")
def song_bot_web():
    return render_template('base.html')


@app.route('/_do_songs')
async def do_songs():
    loop = asyncio.get_running_loop()
    raw_number = request.args.get('number', 1, type=int)
    number = 10 if raw_number > 10 else raw_number
    prompt = request.args.get('prompt', "", type=str)
    temperature = request.args.get('temperature', 1.0, type=float)

    st = partial(generate_song_titles, number=number,
                 prompt=prompt, temperature=temperature)

    my_result = await loop.run_in_executor(None, st)

    return jsonify(my_result)
