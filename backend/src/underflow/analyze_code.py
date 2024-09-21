import os

from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

cerebras_client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))


def get_hello_world():
    resp = cerebras_client.chat.completions.create(
        messages=[{"role": "user", "content": "Say hello world!"}], model="llama3.1-8b"
    )
    return resp


def check_for_external_services(code_str: str):
    resp = cerebras_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Detect which external services are used in the following code. Return a list of of the services only. Only return a list, separated by a comma. Do not return any other text.",
            },
            {"role": "user", "content": code_str},
        ],
        model="llama3.1-8b",
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    return resp


if __name__ == "__main__":
    pprint(get_hello_world().choices[0].message.content)
