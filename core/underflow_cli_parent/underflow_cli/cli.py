import click
import requests
from underflow_sdk.analyze_code import check_for_external_services
import json
import subprocess
import os
import webbrowser
import time
import request

@click.command
@click.argument("uri")
@click.argument("traffic")

def cli(uri: str, traffic: int):
    code_str = requests.get(uri).text
    resp = check_for_external_services(code_str=code_str, traffic=traffic)

    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")

    shell_command = f"cd ../../frontend/my-app && npm run dev"
    
    subprocess.Popen(shell_command, shell=True)

    time.sleep(3)

    

    try:
        webbrowser.open("http://localhost:3000")
        print("Browser launched successfully.")
    except Exception as e:
        print(f"Failed to launch browser: {e}")

    # print("Your Optimized Tech Stack:" + json.dumps(resp[1], indent=4))
    # print("Technical Report:" + json.dumps(resp[2], indent=4))
