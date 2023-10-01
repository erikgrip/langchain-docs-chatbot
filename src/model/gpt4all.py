import os

import requests
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import GPT4All
from tqdm import tqdm


def download_model(save_path, url):
    """Download model from url if not already downloaded."""
    if not os.path.exists(save_path):
        with requests.get(url, stream=True, timeout=5) as response:
            response.raise_for_status()
            with open(save_path, "wb") as f:
                for chunk in tqdm(response.iter_content(chunk_size=8192)):
                    f.write(chunk)


def get_gpt4all_falcon(**kwargs):
    """Get GPT4All model."""
    model_file = "ggml-model-gpt4all-falcon-q4_0.bin"
    save_path = f"./data/{model_file}"
    download_url = (
        f"https://huggingface.co/nomic-ai/gpt4all-falcon-ggml/resolve/main/{model_file}"
    )
    download_model(save_path, download_url)
    callbacks = [StreamingStdOutCallbackHandler()]
    return GPT4All(model=save_path, callbacks=callbacks, verbose=True, **kwargs)


def get_gpt4all_llama(**kwargs):
    """Get GPT4All model."""
    model_file = "llama-2-7b-chat.ggmlv3.q4_0.bin"
    save_path = f"./data/{model_file}"
    download_url = (
        "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/"
        + f"resolve/main/{model_file}"
    )
    download_model(save_path, download_url)
    callbacks = [StreamingStdOutCallbackHandler()]
    return GPT4All(model=save_path, callbacks=callbacks, verbose=True, **kwargs)
