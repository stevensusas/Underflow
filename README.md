# Underflow
**PennApps 2024 Best Use of Defang Challenge Winner 🏆** <br>
Minimize your tech stack's developmental cost

![Stack Underflow-1](https://github.com/user-attachments/assets/ecaf0379-86c2-492f-b9ef-79fd9a5e29de)
![Blank board (6)](https://github.com/user-attachments/assets/f94681f3-4716-465b-b155-c8f0c13e2b02)

https://github.com/user-attachments/assets/d75a332f-8644-428d-b918-cf5b7dcd94f0

## How to use

### Starting up backend

Navigate to FastAPI application directory:
``` cd StackDB ```

Set API keys:
```set CEREBRAS_API_KEY=<API KEY>```
```set OPENAI_API_KEY=<API KEY>```

Start backend server:

```python app.py```

### Launching commandline tool

There is a three-step process to get the CLI `underflow` tool running.

#### (1) Configure the Environment Variables

1. Set up the Cerebras API key:

```bash
set CEREBRAS_API_KEY=<API KEY>
```

#### (2) Install the SDK

1. Go to the `underflow_sdk_parent` folder
2. create virtual environment with  `python3 -m venv underflow-env`
3. activate virtual environemtnw with  `source underflow-env/bin/activate `
4. Run `pip install -e .`

#### (3) Set up the CLI

1. Go to the `underflow_cli_parent` folder
2. Run `poetry install`
3. To test if it works, run the following command in cmd or terminal:

```
underflow semgrep/semgrep-vscode 20000
```


## Inspiration 

Building and maintaining software is complex, time-consuming, and can quickly become expensive, especially as your application scales. Developers, particularly those in startups, often overspend on tools, cloud services, and server infrastructure without realizing it. In fact, nearly 40% of server costs are wasted due to inefficient resource allocation, and servers often remain idle for up to 80% of their runtime. 

As your traffic and data grow, so do your expenses. Managing these rising costs while ensuring your application's performance is critical—but it's not easy. This is where Underflow comes in. It automates the process of evaluating your tech stack and provides data-driven recommendations for cost-effective services and infrastructure. By analyzing your codebase and optimizing for traffic, Underflow helps you save money while maintaining the same performance and scaling capabilities.

## What it does

Underflow is a command-line tool that helps developers optimize their tech stack by analyzing the codebase and identifying opportunities to reduce costs while maintaining performance. With a single command, developers can input a GitHub repository and the number of monthly active users, and Underflow generates a detailed report comparing the current tech stack with an optimized version. The report highlights potential cost savings, performance improvements, and suggests more efficient external services. The tool also provides a clear breakdown of why certain services were recommended, making it easier for developers to make informed decisions about their infrastructure.

## How we built it 

![Blank board (6)](https://github.com/user-attachments/assets/f94681f3-4716-465b-b155-c8f0c13e2b02)

Underflow is a command-line tool designed for optimizing software architecture and minimizing costs based on projected user traffic. It is executed with a single command and two arguments:

```
underflow <github-repository-url> <monthly-active-users>
```

Upon execution, Underflow leverages the OpenAI API to analyze the provided codebase, identifying key third-party services integrated into the project. The extracted service list and the number of monthly active users are then sent to a FastAPI backend for further processing.

The backend queries an AWS RDS-hosted MySQL database, which contains a comprehensive inventory of external service providers, including cloud infrastructure, CI/CD platforms, container orchestration tools, distributed computing services, and more. The database stores detailed information such as pricing tiers, traffic limits, service categories, and performance characteristics. The backend uses this data to identify alternative services that provide equivalent functionality at a lower cost while supporting the required user traffic.

The results of this optimization process are cached, and a comparison report is generated using the OpenAI API. This report highlights the cost and performance differences between the original tech stack and the proposed optimized stack, along with a rationale for selecting the new services.

Finally, Underflow launches a GUI that presents a detailed analytics report comparing the original and optimized tech stacks. The report provides key insights into cost savings, performance improvements, and the reasoning behind service provider selections.

This technical solution offers developers a streamlined way to evaluate and optimize their tech stacks based on real-world cost and performance considerations.

## Accomplishments that we're proud of   
We’re proud of creating a tool that simplifies the complex task of optimizing tech stacks while reducing costs for developers. Successfully integrating multiple components, such as the OpenAI API for codebase analysis, a FastAPI backend for processing, and an AWS-hosted MySQL database for querying external services, was a significant achievement. Additionally, building a user-friendly command-line interface that provides clear, data-driven reports about tech stack performance and cost optimization is something we're excited about. We also managed to create a streamlined workflow that allows developers to assess cost-saving opportunities without needing deep knowledge of infrastructure or services.

## What's next for Underflow 
- Generating a better database containing more comprehensive list of available external services and dependencies
- Migrate traffic determination from user manual input to be based on server-level architecture, such as using elastic search on server logs to determine the true amount of third party service usages
