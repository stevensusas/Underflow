import click
import requests
from underflow_sdk.analyze_code import check_for_external_services
import json

@click.command
@click.argument("uri")
@click.argument("traffic")
def cli(uri: str, traffic: int):
    code_str = requests.get(uri).text
    resp = check_for_external_services(code_str=code_str, traffic=traffic)
    print("Your Optimized Tech Stack:" + json.dumps(resp[1], indent=4))
    print("Technical Report:" + json.dumps(resp[2], indent=4))
