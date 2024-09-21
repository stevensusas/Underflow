import click
import requests
from underflow_sdk.analyze_code import check_for_external_services


@click.command
@click.argument("uri")
def cli(uri: str):
    code_str = requests.get(uri).text
    resp = check_for_external_services(code_str=code_str)
    print(resp.choices[0].message.content)
