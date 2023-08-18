from simpletransformers.language_generation import (
    LanguageGenerationModel
)

def generate_song_titles(temperature=1.0, number=1, prompt="", model_name="models/2023-08-17_gpt2_best"):
    """generate a list of song titles"""
    print(model_name)
    model = LanguageGenerationModel(
        "gpt2", model_name,
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

    stdbFile = open("data/stdb.txt", "r")
    stdbData = stdbFile.read()
    stdb = stdbData.split('\n')

    for element in song_titles_raw:
        song_title = "".join(element.split("<<bst>>")[1].split("<<est>>")[0])
        if song_title in stdb:
            song_title = "".join(["<s>",song_title,"</s> <span>[AiDB]</span>"])
        else:
            historyFile = open("data/history.txt", "a")
            historyFile.write("\n" + song_title)
            historyFile.close
        song_titles += [song_title]
    return song_titles
