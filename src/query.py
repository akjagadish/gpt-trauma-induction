import openai
import time
import pandas as pd
import numpy as np
import torch
import argparse
import sys
from prompts import retrieve_prompt
import os
from dotenv import load_dotenv
import anthropic

load_dotenv() # load environment variables from .env
TOKEN_COUNTER = 0
def act(text=None, run_gpt='gpt4', temperature=1., max_length=300):

    global TOKEN_COUNTER

    if run_gpt=='gpt4':
        
        openai.api_key = os.getenv("OPENAI_API_KEY") # load key from env
        text = [{"role": "system", "content": ""}, \
                {"role": "user", "content": text}]
        engine = 'gpt-4'
        try:
            response = openai.ChatCompletion.create(
                model = engine,
                messages = text,
                max_tokens = max_length,
                temperature = temperature,
            )
            TOKEN_COUNTER += response['usage']['total_tokens'] 
            return response.choices[0].message.content.replace(' ', '')
        except:
            print("Error, trying again...ratelimiterror")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(exc_value)


    elif run_gpt=='gpt3':
        
        openai.api_key = os.getenv("OPENAI_API_KEY") # load key from env
        engine = "text-davinci-003"
        try:
            response = openai.Completion.create(
                engine = engine,
                prompt = text,
                max_tokens = max_length,
                temperature = temperature,
            )
            TOKEN_COUNTER += response['usage']['total_tokens'] 
            return response.choices[0].text.strip().replace(' ', '')
        except:
            print("Error")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(exc_value)
            #time.sleep(3**iter)
            
    elif run_gpt=='claude':

        client = anthropic.Anthropic()
        response = client.completions.create(
                prompt = anthropic.HUMAN_PROMPT + text + anthropic.AI_PROMPT,
                #stop_sequences=[anthropic.HUMAN_PROMPT],
                model="claude-2",
                temperature=temperature,
                max_tokens_to_sample=max_length,
            ).completion.replace(' ', '')
    
        return response
 
    else:

        return NotImplementedError 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm", type=str, required=True, choices=['gpt3', 'gpt4', 'claude'])
    parser.add_argument("--temperature", type=float, required=False, default=1.0)
    parser.add_argument("--max-length", type=int, required=False, default=1)
    parser.add_argument("--proc-id", type=int, required=False, default=0)
    parser.add_argument("--num-runs", type=int, required=False, default=1)
    parser.add_argument("--prompt-version", type=str, required=False, default=None)
    parser.add_argument("--prompt-length", type=str, required=True, default=None)
    parser.add_argument("--condition", type=str, required=True, default=None)

    args = parser.parse_args()
    llm = args.llm
    # model parameters
    temperature = args.temperature
    max_length = args.max_length
    # task parameters
    condition = args.condition
    length = args.prompt_length
    # runtime parameters
    proc_id = args.proc_id
    num_runs = args.num_runs
    prompt_version = args.prompt_version

    trauma_cues = ['military', 'disaster', 'interpersonal', 'accident', 'ambush']
    relaxation_cues = ['generic', 'indian', 'winter', 'sunset', 'body', 'chatgpt']

    # run gpt models
    for run in range(num_runs):

        if condition == 'stai':
            instructions = retrieve_prompt(trauma_cue=None, relax_cue=None, length=None, condition=condition, version=prompt_version)
            action = act(instructions, llm, temperature, max_length)

        if condition=='trauma_stai':
            for trauma_cue in trauma_cues:
                    instructions = retrieve_prompt(trauma_cue=trauma_cue, relax_cue=None, length=length, condition=condition, version=prompt_version)
                    action = act(instructions, llm, temperature, max_length)

        elif condition == 'trauma_relaxation_stai':
            for trauma_cue in trauma_cues:
                for relaxation_cue in relaxation_cues:
                    instructions = retrieve_prompt(trauma_cue=trauma_cue, relax_cue=relaxation_cue, length=length, condition=condition, version=prompt_version)
                    action = act(instructions, llm, temperature, max_length)
            
