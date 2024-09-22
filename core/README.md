# Stack Underflow Backend

There is a three-step process to get the CLI `underflow` tool running.

### (1) Configure the Environment Variables

1. Set up the Cerebras API key:

```bash
set CEREBRAS_API_KEY=<API KEY>
```

### (2) Install the SDK

1. Go to the `underflow_sdk_parent` folder
2. create virtual environment with  `python3 -m venv underflow-env`
3. activate virtual environemtnw with  `source underflow-env/bin/activate `
4. Run `pip install -e .`

### (3) Set up the CLI

1. Go to the `underflow_cli_parent` folder
2. Run `poetry install`
3. To test if it works, run the following command in cmd or terminal:

```bash
underflow https://raw.githubusercontent.com/GoogleCloudPlatform/getting-started-python/refs/heads/main/noxfile.py
```
