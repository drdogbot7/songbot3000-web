from simpletransformers.language_generation import (
    LanguageGenerationModel
)


def clean_output(string):
    """remove the prefix and suffix from model output"""
    prefix = "<<bst>>"
    suffix = "<<est>>"
    song_title = ''.join(string.split(prefix)[1].split(suffix)[0])
    return song_title


def generate_song_titles(temperature=1.0, number=1, prompt=""):
    """generate a list of song titles"""
    model = LanguageGenerationModel(
        "gpt2", "models/bot_13082023_1358/best_model",
        args={
            # "use_multiprocessing": False,
            "max_length": 40,
            "length_penalty": 1,
            "temperature": temperature,
            "num_return_sequences": number,
            "prompt": "<<bst>>" + prompt
        }, use_cuda=False
    )
    song_titles_raw = model.generate()
    song_titles = []
    for string in song_titles_raw:
        song_titles += [clean_output(string)]
    return song_titles
