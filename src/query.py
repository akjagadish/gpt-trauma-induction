import openai
import time
import pandas as pd
import numpy as np
import random
import json
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
                prompt = text,# I take care of the anthorpic.HUMAN_PROMPT etc in the script below
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
    parser.add_argument("--temperature", type=float, required=False, default=1.0, help="temperature for sampling")
    parser.add_argument("--max-length", type=int, required=False, default=1, help="maximum length of response from GPT")
    parser.add_argument("--num-runs", type=int, required=False, default=1, help="number of runs to execute")
    parser.add_argument("--prompt-length", type=str, required=True, choices=['long', 'brief'], help="length of prompt")
    parser.add_argument("--condition", type=str, required=True, choices=['stai', 'trauma_stai', 'trauma_relaxation_stai'], help="condition to run")
    parser.add_argument("--prompt-version", type=str, required=False, default=None, help="version of prompt to use")
    parser.add_argument("--proc-id", type=int, required=False, default=0, help="process id for parallelization")

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

######## Kristin debugging stuff
    # llm = "gpt3"
    # # model parameters
    # temperature = 0
    # max_length = 1
    # # task parameters
    # length = "long"
    # # runtime parameters
    # proc_id = "test"
    # num_runs = 10
    # prompt_version = 0
    # condition = "trauma_relaxation_stai"

    # def act(text):
    #     print(text)
    #     return ["1"]

    # if condition != "stai":
    #     trauma_cues = ['military', 'disaster', 'interpersonal', 'accident', 'ambush']
    #     if condition == "trauma_relaxation_stai":
    #         relaxation_cues = ['generic', 'indian', 'winter', 'sunset', 'body', 'chatgpt']
    #     else:
    #         relaxation_cues = ["none"]
    # else:
    #     trauma_cues = ["none"]
    #     relaxation_cues = ["none"]


    # parameters for formatting the prompt

    if llm == "gpt3" or llm == "gpt4":
        Q_ = "Q:"
        A_ = "A:"
        E_ = " "
    elif llm == "claude":
        Q_ = anthropic.HUMAN_PROMPT
        A_ = "Assistant:" # the two blank lines it requires are always in my code anyway
        E_ = ""# for claude must not end with a space, for GPT must end with a space

    # load questionnaires
    questionnaires = pd.read_json(
                r"src/STAI/questionnaires.json"
            )
    
    # initialize saving (json)
    
    # run gpt models
    
    #TODO: check final text depending on the llms
    data = {}

    for trauma_cue in trauma_cues:
        data[trauma_cue] = {}
        for relaxation_cue in relaxation_cues:
            data[trauma_cue][relaxation_cue] = {}

            if condition=='trauma_stai':
                
                instructions = retrieve_prompt(trauma_cue=trauma_cue, relaxation_cue=None, length=length, condition=condition, version=prompt_version)
                instructions += "\n"
                        #action = act(instructions, llm, temperature, max_length)

            elif condition == 'trauma_relaxation_stai':
                instructions = retrieve_prompt(trauma_cue=trauma_cue, relaxation_cue=relaxation_cue, length=length, condition=condition, version=prompt_version)
                instructions += "\n"
                        #action = act(instructions, llm, temperature, max_length)

            elif condition == 'stai':
                instructions = "" # no preprompt

            # grab the corresponding questionnaire (it's saved as a list)
            questions = questionnaires["STAI"]["questions"] 

            # add preamble of STAI
            instructions += f"{Q_} " + questionnaires["STAI"]["preamble"] + "\n"   

            counter = 0

            for run in range(num_runs): # loop through several runs of the questionnaire if desired
                data[trauma_cue][relaxation_cue][run] = {}

                for item in range(len(questions)): # loop through questionnaire items

                # get answer options (scramble their order independently at each questionnaire item)
                    options = questions[0]["labels"]
                    optionText = ""
                    
                    # scramble the order of the labels (e.g. "never", "sometimes") and the numbers associated with them
                    order = [i for i in range(len(options))]
                    random.shuffle(order)
                    num = [i for i in range(1,len(options)+1)]
                    random.shuffle(num)
                    
                    j = 0
                    # concatinate the option text
                    for i in order:
                        optionText += "Option "+ str(num[j]) + ": " + str(options[i]) + ".\n"
                        j+=1
                    
                    
                    
                        # get question
                    prompt = "'" +str(questions[item]["prompt"]) + "'"
                    
                    # concatinate the full prompt
        
                    text = instructions +  prompt + "\n"+ optionText + "\n" + "\n" + f"{A_} Option{E_}"

                        #print(text)
                        ######### this is where I actually interact with gpt-3!
                        for k in range (50):# try 50 times before breaking (sometimes the server is overloaded so try again then)
                            try:
                                action = act(text)
                                data[trauma_cue][relaxation_cue][run][item] = order[num.index(pd.to_numeric(action[0]))]+1
                                break
                            except:# try again if it fails
                                # Print the error message
                                exc_type, exc_value, exc_traceback = sys.exc_info()
                                print(exc_value)
                                print("retry")
                                pass
                        ############
                counter += 1
                if counter % 5 == 0 & counter > 0:
                    # save temp data
                    with open(f"src/temp_{llm}_{length}__{condition}_{proc_id}.json", 'w') as outfile:
                        json.dump(data, outfile)

    # save data
    with open(f"src/{llm}_{length}_{proc_id}.json", 'w') as outfile: #TODO: check if this is the correct file naming
        json.dump(data, outfile)