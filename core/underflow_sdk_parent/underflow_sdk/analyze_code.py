import os

from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv
from pprint import pprint
import requests

load_dotenv()

cerebras_client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

def get_hello_world():
    resp = cerebras_client.chat.completions.create(
        messages=[{"role": "user", "content": "Say hello world!"}], model="llama3.1-8b"
    )
    return resp


def check_for_external_services(code_str: str, traffic: int):
    resp = cerebras_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Detect which external services are used in the following code. Return a list of of the services only. Only return a list, separated by a comma. Do not return any other text.",
            },
            {"role": "user", "content": code_str},
        ],
        model="llama3.1-8b",
        temperature=0.0,
    )

    url_original_service = "http://localhost:8000/original-services"
    url_optimal_service = "http://localhost:8000/optimal-services"
    url_tech_report = "http://localhost:8000/generate-report"

    services = resp.choices[0].message.content.split(", ")

    payload = {
    "services": services,
    "traffic": traffic
}

    original_service = requests.post(url_original_service, json = payload).json()
    optimal_service = requests.post(url_optimal_service, json = payload).json()
    tech_report = requests.post(url_tech_report, json = payload).json()

    return (original_service, optimal_service, tech_report)

if __name__ == "__main__":
    pprint(get_hello_world().choices[0].message.content)
