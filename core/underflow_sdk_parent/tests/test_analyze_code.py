import pytest
import requests
from underflow_sdk.analyze_code import check_for_external_services


def test_detect_aws():
    URL = "https://raw.githubusercontent.com/awsdocs/aws-doc-sdk-examples/refs/heads/main/python/example_code/s3/s3_basics/object_wrapper.py"
    resp = requests.get(URL)
    user_code = resp.text
    result = check_for_external_services(code_str=user_code).choices[0].message.content
    result = eval(result)
    print(result)
    assert "Amazon S3" in result
