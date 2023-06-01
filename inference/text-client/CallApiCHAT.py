import requests
import json
import colorama

colorama.init()

SERVER_IP = "10.0.0.18"
URL = f"http://{SERVER_IP}:5000/generate"
ASSISTANT_TOKEN = "classistanti"

def prompt(context):
    data = {"text": context}
    headers = {
        "Content-Type": 'application/json',
        "Accept": 'text/plain'
    }
    response = requests.post(URL, data=json.dumps(data), headers=headers)
    return response.json()["generated text"]

history = ""

while True:
    inp = input(">>> ")
    context = history + ASSISTANT_TOKEN + inp
    output = prompt(context)
    just_latest_asst_output = output.split(ASSISTANT_TOKEN)[-1]
    history += just_latest_asst_output
    print(colorama.Fore.GREEN + just_latest_asst_output + colorama.Style.RESET_ALL)
