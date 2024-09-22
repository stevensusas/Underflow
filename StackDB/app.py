import os
from collections import defaultdict
from enum import Enum
from typing import Any, Dict, List

import uvicorn
import requests
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from mysql.connector import Error, connect
from openai import OpenAI, OpenAIError
from pydantic import BaseModel

load_dotenv()

# Database Configuration
DB_HOST = "stackunderflow.cha8ies4obs2.us-east-1.rds.amazonaws.com"  # Replace with your RDS endpoint
DB_PORT = "3306"  # MySQL default port
DB_USER = "admin"  # Replace with your MySQL username
DB_PASSWORD = "12345678"  # Replace with your MySQL password
DB_NAME = "StackUnderflow"


client = OpenAI(api_key=os.getenv("X_OPENAI_API_KEY"))
cerebras_client = Cerebras(
    # This is the default and can be omitted
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)


class LocalState:
    def __init__(self):
        self.original_service = None
        self.optimal_service = None
        self.tech_report = None
        self.repository_name = None

    def update_original_service(self, data):
        self.original_service = data

    def update_optimal_service(self, data):
        self.optimal_service = data

    def update_tech_report(self, data):
        self.tech_report = data

    def update_repository_name(self, data):
        self.repository_name = data


def summarize(text):
    chat_completion = cerebras_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following text in 20 words or less: {text}",
            }
        ],
        model="llama3.1-8b",
    )
    return chat_completion.choices[0].message.content


local_state = LocalState()


# Define the ServiceType Enum
class ServiceType(Enum):
    COMPUTE = "Compute"
    STORAGE = "Storage"
    DATABASE = "Database"
    CONTAINERIZATION = "Containerization"
    ANALYTICS = "Analytics"
    AI = "AI"
    AUTHENTICATION = "Authentication"
    CI_CD = "CI/CD"
    PACKAGE_MANAGEMENT = "Package Management"
    CONTAINER_REGISTRY = "Container Registry"
    DEPLOYMENT = "Deployment"
    SERVERLESS = "Serverless"
    MONITORING = "Monitoring"
    LOGGING = "Logging"
    ALERTING = "Alerting"
    INCIDENT_MANAGEMENT = "Incident Management"
    SCHEDULING = "Scheduling"
    MESSAGING = "Messaging"
    VOICE = "Voice"
    EMAIL = "Email"
    MARKETING = "Marketing"
    PLUGINS = "Plugins"
    AUTOMATION = "Automation"
    FIREWALL = "Firewall"
    IDENTITY_MANAGEMENT = "Identity Management"
    PAYMENTS = "Payments"
    BILLING = "Billing"
    E_COMMERCE = "E-commerce"
    WEBSITE_BUILDER = "Website Builder"
    SEO = "SEO"
    CONTENT_MANAGEMENT = "Content Management"
    COMMUNICATION = "Communication"
    INTEGRATION = "Integration"
    WEBINARS = "Webinars"
    WORKFLOW = "Workflow"
    PRODUCTIVITY = "Productivity"
    ENHANCEMENTS = "Enhancements"
    REGISTRY = "Registry"
    VISUALIZATION = "Visualization"
    SECURITY = "Security"
    CDN = "CDN"
    DNS = "DNS"
    OPTIMIZATION = "Optimization"
    PERFORMANCE = "Performance"


# Define the Service Pydantic Model
class Service(BaseModel):
    name: str
    cost: float
    type: ServiceType
    description: str
    traffic: float


# Define the Request Model
class ServiceRequest(BaseModel):
    services: List[str]
    traffic: float


# Define the Response Model
class ServiceResponse(BaseModel):
    name: str
    type: ServiceType
    cost: float
    description: str
    traffic: float


# Define the Report Response Model
class ReportResponse(BaseModel):
    report: str


# API Class to handle database operations
class API:
    def __init__(self):
        self.connection = self.get_db_connection()
        self.original_services = None
        self.optimized_services = None
        self.technical_report = None

    def get_db_connection(self):
        try:
            connection = connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                autocommit=False,  # Manage transactions manually
            )
            print("Successfully connected to the database.")
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise

    def get_services(self, services_names: List[str]) -> List[Service]:
        """
        Fetches services from the database based on provided service names.

        :param services_names: List of service names to fetch.
        :return: List of Service instances.
        """
        services = []

        if not self.connection:
            print("No database connection.")
            return services

        if not services_names:
            print("No services provided.")
            return services

        try:
            cursor = self.connection.cursor(dictionary=True)
            # Prepare the SQL query with placeholders
            format_strings = ",".join(["%s"] * len(services_names))
            query = f"""
                SELECT name, cost_per_user_per_hour, detailed_description, traffic_upperbound, type 
                FROM services 
                WHERE name IN ({format_strings});
            """
            cursor.execute(query, tuple(services_names))
            results = cursor.fetchall()

            for row in results:
                try:
                    service = Service(
                        name=row["name"],
                        cost=float(row["cost_per_user_per_hour"]),
                        type=ServiceType(row["type"]),
                        description=row.get("detailed_description", ""),
                        traffic=float(row.get("traffic_upperbound", 0)),
                    )
                    services.append(service)
                except ValueError as ve:
                    print(f"Data conversion error for service {row['name']}: {ve}")
                except KeyError as ke:
                    print(f"Missing expected field {ke} in database response.")

            print(f"Fetched {len(services)} services from the database.")

        except Error as e:
            print(f"Error: '{e}' occurred while fetching services.")
            raise
        finally:
            if cursor:
                cursor.close()

        return services

    def find_cheapest_highest_traffic_per_type(
        self, services: List[Service]
    ) -> List[Service]:
        """
        Identifies the cheapest service with the highest traffic for each service type.

        :param services: List of Service instances.
        :return: List of optimal Service instances.
        """
        # Group services by type
        services_by_type = defaultdict(list)
        for service in services:
            services_by_type[service.type].append(service)

        optimal_services = []

        for service_type, service_list in services_by_type.items():
            if service_type is None:
                print(
                    f"Warning: Service type for services {[s.name for s in service_list]} is unknown."
                )
                continue  # Skip unknown types

            # Sort services first by cost (ascending), then by traffic (descending)
            sorted_services = sorted(service_list, key=lambda s: (s.cost, -s.traffic))
            # The first service is the cheapest with the highest traffic
            optimal_service = sorted_services[0]
            optimal_services.append(optimal_service)

        print(
            f"Identified {len(optimal_services)} optimal services across service types."
        )
        return optimal_services

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")

    def update_original_services(self, services: List[ServiceResponse]):
        self.original_services = services

    def update_optimized_services(self, services: List[ServiceResponse]):
        self.optimized_services = services

    def update_technical_report(self, report: ReportResponse):
        self.technical_report = report


# Initialize FastAPI
app = FastAPI(title="StackUnderflow Service Optimizer")

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize the API handler
api_handler = API()


# Define the Endpoint
@app.post("/original-services", response_model=List[ServiceResponse])
def get_original_services(request: ServiceRequest):
    """
    Endpoint to find the cheapest services with the highest traffic per service type.

    :param request: ServiceRequest containing service names and traffic.
    :return: List of optimal services.
    """
    try:
        # Fetch services from the database
        services = api_handler.get_services(request.services)
        if not services:
            raise HTTPException(
                status_code=404, detail="No services found for the provided names."
            )
        api_handler.update_original_services(
            [ServiceResponse(**service.dict()) for service in services]
        )
        return [ServiceResponse(**service.dict()) for service in services]

    except Error as db_error:
        print(f"Database error: {db_error}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while accessing the database.",
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# Define the Endpoint
@app.post("/optimal-services", response_model=List[ServiceResponse])
def get_optimal_services(request: ServiceRequest):
    """
    Endpoint to find the cheapest services with the highest traffic per service type.

    :param request: ServiceRequest containing service names and traffic.
    :return: List of optimal services.
    """
    try:
        # Fetch services from the database
        services = api_handler.get_services(request.services)
        if not services:
            raise HTTPException(
                status_code=404, detail="No services found for the provided names."
            )

        # Identify optimal services
        optimal_services = api_handler.find_cheapest_highest_traffic_per_type(services)
        if not optimal_services:
            raise HTTPException(
                status_code=404, detail="No optimal services could be identified."
            )
        api_handler.update_optimized_services(
            [ServiceResponse(**service.dict()) for service in optimal_services]
        )
        return [ServiceResponse(**service.dict()) for service in optimal_services]

    except Error as db_error:
        print(f"Database error: {db_error}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while accessing the database.",
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# Define the Endpoint to Generate Technical Report
@app.post("/generate-report", response_model=ReportResponse)
def generate_technical_report(request: ServiceRequest):
    """
    Endpoint to generate a technical report explaining the optimization.

    :param request: ServiceRequest containing service names and traffic.
    :return: Technical report as a string.
    """
    try:
        # Fetch original services from the database
        original_services = api_handler.get_services(request.services)
        if not original_services:
            raise HTTPException(
                status_code=404, detail="No services found for the provided names."
            )

        # Identify optimal services
        optimal_services = api_handler.find_cheapest_highest_traffic_per_type(
            original_services
        )
        if not optimal_services:
            raise HTTPException(
                status_code=404, detail="No optimal services could be identified."
            )

        # Prepare the context for the report
        original_services_data = "\n".join(
            [
                f"- **{service.name}** (Type: {service.type.value})\n  - Cost: ${service.cost}/user/hour\n  - Traffic Upperbound: {service.traffic} units\n  - Description: {service.description}"
                for service in original_services
            ]
        )

        optimal_services_data = "\n".join(
            [
                f"- **{service.name}** (Type: {service.type.value})\n  - Cost: ${service.cost}/user/hour\n  - Traffic Upperbound: {service.traffic} units\n  - Description: {service.description}"
                for service in optimal_services
            ]
        )

        # Define the prompt for OpenAI
        prompt = f"""
        Given the following original services and the optimized services, generate a detailed technical report explaining why the optimized services were chosen over the original ones and how this selection reduces costs while maintaining or improving traffic handling capabilities.

        **Original Services:**
        {original_services_data}

        **Optimized Services:**
        {optimal_services_data}

        **Requirements:**
        - Explain the criteria used for optimization.
        - Highlight cost reductions achieved.
        - Discuss any improvements in traffic handling or other relevant metrics.
        - Provide a clear comparison between original and optimized services.
        - Use a professional and technical tone suitable for stakeholders.
        """

        # Call OpenAI API to generate the report
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a technical analyst."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        # Extract the report from OpenAI's response
        report = response.choices[0].message.content.strip()
        print(f"Generated technical report: {report}")
        api_handler.update_technical_report(report)
        return ReportResponse(report=report)

    except OpenAIError as oe:
        print(f"OpenAI API error: {oe}")
        raise HTTPException(
            status_code=502, detail="Error communicating with OpenAI API."
        )
    except Error as db_error:
        print(f"Database error: {db_error}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while accessing the database.",
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# Define a Root Endpoint for Health Check
@app.get("/")
def read_root():
    return {"message": "Welcome to the StackUnderflow Service Optimizer API!"}


@app.post("/api/set_info")
async def api_set_info(request: Request):
    global local_state

    resp = await request.json()
    local_state.update_original_service(resp["original_service"])
    local_state.update_optimal_service(resp["optimal_service"])
    local_state.update_tech_report(resp["tech_report"])
    local_state.update_repository_name(resp["repository_name"])
    return {"data": resp}


def get_url_for(service_name):
    stream = False
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": os.getenv("TUNE_KEY"),
        "Content-Type": "application/json",
    }
    data = {
        "temperature": 0.8,
        "messages": [
            {
                "role": "system",
                "content": "Only return the project URL of what the user sends you. Only return HTTP URL, nothing else. ",
            },
            {"role": "user", "content": service_name},
            # {"role": "assistant", "content": "https://aws.amazon.com/s3/"},
        ],
        "model": "anthropic/claude-3-haiku",
        "stream": stream,
        "frequency_penalty": 0,
        "max_tokens": 900,
    }
    response = requests.post(url, headers=headers, json=data)
    url = response.json()["choices"][0]["message"]["content"]
    return url


@app.get("/api/current_state")
def api_current_state():
    global local_state

    print(local_state.optimal_service)
    original_cost = sum([tmp["cost"] for tmp in local_state.original_service])
    optimal_cost = sum([tmp["cost"] for tmp in local_state.optimal_service])

    traffic_cost = [
        {"label": tmp["cost"], "new": tmp["traffic"], "original": tmp["traffic"]}
        for tmp in local_state.original_service
    ]

    unique_types = []
    for i in range(len(local_state.original_service)):
        tmp = local_state.original_service[i]
        if tmp["type"] not in unique_types:
            unique_types.append(tmp["type"])

    for i in range(len(local_state.optimal_service)):
        tmp = local_state.optimal_service[i]
        if tmp["type"] not in unique_types:
            unique_types.append(tmp["type"])

    cost_comparison = []
    for i in range(len(unique_types)):
        curr_dict = {"label": unique_types[i], "original": 0, "new": 0}
        for j in range(len(local_state.original_service)):
            if local_state.original_service[j]["type"] == unique_types[i]:
                curr_dict["original"] += 1
        for j in range(len(local_state.optimal_service)):
            if local_state.optimal_service[j]["type"] == unique_types[i]:
                curr_dict["new"] += 1
        cost_comparison.append(curr_dict)

    print(traffic_cost)
    print("cost comparison:")
    print(cost_comparison)

    return {
        "content": {
            "oldServices": [
                {
                    "name": tmp["name"],
                    "type": tmp["type"],
                    "cost": f"$ {tmp['cost']}",
                    "url": get_url_for(tmp["name"]),
                }
                for tmp in local_state.original_service
            ],
            "newServices": [
                {
                    "name": tmp["name"],
                    "type": tmp["type"],
                    "cost": f"$ {round(tmp['cost'],2)}",
                    "url": get_url_for(tmp["name"]),
                }
                for tmp in local_state.optimal_service
            ],
            "currentMonthlyCost": {"value": f"${round(original_cost,2)}"},
            "newMonthlyCost": {"value": f"${round(optimal_cost, 2)}"},
            "estimatedSavings": {
                "value": f"{round(100*(original_cost-optimal_cost)/original_cost,1)}%"
            },
            "serverUptime": {"value": "0%"},
            "currentTraffic": {
                "value": f"{local_state.original_service[0]['traffic']}"
            },
            "summary": {"value": summarize(local_state.tech_report["report"])},
            "aiAssistantResp": {"value": local_state.tech_report["report"]},
            "costComparison": [
                {"label": "Cloud", "original": original_cost, "new": optimal_cost},
                # {"label": "Storage", "original": 305, "new": 200},
                # {"label": "Distribution", "original": 237, "new": 120},
            ],
            "costComparisonV2": cost_comparison,
            "revenueComparison": [
                {"label": "Sep", "original": 0, "new": 0},
                # {"label": "Oct", "original": 305, "new": 200},
                # {"label": "Nov", "original": 237, "new": 150},
            ],
            "trafficCostComparison": traffic_cost,
            "repositoryName": local_state.repository_name,
            # [
            #     {"label": "1", "new": 0},
            #     # {"label": "2", "new": 180},
            #     # {"label": "3", "new": 120},
            # ],
        }
    }


@app.get("/cached-original-services")
def cached_original_services():
    return api_handler.original_services


@app.get("/cached-optimized-services")
def cached_optimized_services():
    return api_handler.optimized_services


@app.get("/cached-technical-report")
def cached_optimized_services():
    return api_handler.technical_report


# Shutdown Event to close the DB connection
@app.on_event("shutdown")
def shutdown_event():
    api_handler.close_connection()


# Main function to run the app using Uvicorn
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
