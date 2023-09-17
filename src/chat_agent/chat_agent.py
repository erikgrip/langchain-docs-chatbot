import os
from tqdm import tqdm
from langchain import HuggingFaceHub
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain import PromptTemplate, LLMChain
from pprint import pprint
from langchain.llms import GPT4All
import requests

model = "ggml-model-gpt4all-falcon-q4_0.bin"
local_path = f"./data/{model}"
download_url = f"https://huggingface.co/nomic-ai/gpt4all-falcon-ggml/resolve/main/{model}"

# Download model from url with redirect using requests, if not already downloaded
if not os.path.exists(local_path):
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in tqdm(r.iter_content(chunk_size=8192)):
                f.write(chunk)



question = "Who were the two most expensive players?"
context = """We're going to let you in on a little industry secret: it is quite difficult to preview a soccer league's season when all of the teams in that league still have another month to both acquire more players and get rid of the ones they no longer want.

For example, seven players either joined or departed from Premier League clubs for transfer fees of at least €50 million since we wrote our preview at the beginning of last month:

Moisés Caicedo, from Brighton to Chelsea for €116 million

Harry Kane, from Tottenham to Bayern Munich for €100 million

Romeo Lavia, from Southampton to Chelsea for €62.1 million

Matheus Nunes, from Wolverhampton to Manchester City for €62 million

Jérémy Doku, from Stade Rennais to Manchester City for €60 million

Brennan Johnson, from Nottingham Forest to Tottenham for €55 million

Aleksandar Mitrovic, from Fulham to Al Hilal for ​​€52.6 million

So, with plenty of player movement and four match weeks since we last evaluated each of the 20 teams in the Premier League, we figured we'd rank them all again. To be clear: these are power rankings, not a prediction for how we think the table will shake out. In other words, if one team is ranked above another team, it means we think it should be favored over the other team if they met on a neutral field. These are our forward-looking estimates for how all 20 teams will perform from here on out.
"""

template = """
Question: {question}

Context: {context}

Answer: Let's think step by step.
"""

prompt = PromptTemplate(template=template, input_variables=["question", "context"])

local_path = "./data/ggml-model-gpt4all-falcon-q4_0.bin"

callbacks = [StreamingStdOutCallbackHandler()]
llm = GPT4All(model=local_path, callbacks=callbacks, verbose=True)
llm_chain = LLMChain(prompt=prompt, llm=llm)
pprint(llm_chain.run({"question": question, "context": context}))
