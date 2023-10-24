import json
import pandas as pd
import os

print(os.getcwd())

questionnaire_data = pd.read_csv('src/STAI/questionnaires.csv',sep=';', lineterminator='\r')

data = {}

data["STAI"] = dict(questions=[], preamble=questionnaire_data.Preamble[questionnaire_data.Measure == "STAI"].iloc[0],
                name="STAI")
for j in questionnaire_data[questionnaire_data.Measure == "STAI"].iterrows():
    print([i for i in j[1].Options.split(',') if len(i)])
    data["STAI"]['questions'].append(dict(prompt=j[1].Question,
                                        labels=[i for i in j[1].Options.split(',') if len(i)]))

json_data = json.dumps(data)

with open('src/STAI/questionnaires.json', 'w') as outfile:
    json.dump(data, outfile)

