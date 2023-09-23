import os

import requests
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import GPT4All
from tqdm import tqdm


def download_model(save_path, url):
    """Download model from url if not already downloaded."""
    if not os.path.exists(save_path):
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(save_path, "wb") as f:
                for chunk in tqdm(response.iter_content(chunk_size=8192)):
                    f.write(chunk)


def get_gpt4all():
    """Get GPT4All model."""
    model_file = "ggml-model-gpt4all-falcon-q4_0.bin"
    save_path = f"./data/{model_file}"
    download_url = (
        f"https://huggingface.co/nomic-ai/gpt4all-falcon-ggml/resolve/main/{model_file}"
    )
    download_model(save_path, download_url)
    callbacks = [StreamingStdOutCallbackHandler()]
    return GPT4All(model=save_path, callbacks=callbacks, verbose=True)
