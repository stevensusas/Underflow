from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mysql.connector import connect, Error
from typing import List, Dict, Any
from collections import defaultdict
from enum import Enum
import uvicorn
from openai import OpenAI
from openai import OpenAIError
import os
from dotenv import load_dotenv


# Database Configuration
DB_HOST = "stackunderflow.cha8ies4obs2.us-east-1.rds.amazonaws.com"# Replace with your RDS endpoint
DB_PORT = "3306"# MySQL default port
DB_USER = "admin"   # Replace with your MySQL username
DB_PASSWORD = "12345678" # Replace with your MySQL password
DB_NAME = "StackUnderflow"


client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

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

    def get_db_connection(self):
        try:
            connection = connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                autocommit=False  # Manage transactions manually
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
            format_strings = ','.join(['%s'] * len(services_names))
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
                        name=row['name'],
                        cost=float(row['cost_per_user_per_hour']),
                        type=ServiceType(row['type']),
                        description=row.get('detailed_description', ''),
                        traffic=float(row.get('traffic_upperbound', 0))
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

    def find_cheapest_highest_traffic_per_type(self, services: List[Service]) -> List[Service]:
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
                print(f"Warning: Service type for services {[s.name for s in service_list]} is unknown.")
                continue  # Skip unknown types

            # Sort services first by cost (ascending), then by traffic (descending)
            sorted_services = sorted(service_list, key=lambda s: (s.cost, -s.traffic))
            # The first service is the cheapest with the highest traffic
            optimal_service = sorted_services[0]
            optimal_services.append(optimal_service)

        print(f"Identified {len(optimal_services)} optimal services across service types.")
        return optimal_services

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")


# Initialize FastAPI
app = FastAPI(title="StackUnderflow Service Optimizer")

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
            raise HTTPException(status_code=404, detail="No services found for the provided names.")
        return [ServiceResponse(**service.dict()) for service in services]

    except Error as db_error:
        print(f"Database error: {db_error}")
        raise HTTPException(status_code=500, detail="Internal server error while accessing the database.")
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
            raise HTTPException(status_code=404, detail="No services found for the provided names.")

        # Identify optimal services
        optimal_services = api_handler.find_cheapest_highest_traffic_per_type(services)
        if not optimal_services:
            raise HTTPException(status_code=404, detail="No optimal services could be identified.")

        return [ServiceResponse(**service.dict()) for service in optimal_services]

    except Error as db_error:
        print(f"Database error: {db_error}")
        raise HTTPException(status_code=500, detail="Internal server error while accessing the database.")
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
            raise HTTPException(status_code=404, detail="No services found for the provided names.")

        # Identify optimal services
        optimal_services = api_handler.find_cheapest_highest_traffic_per_type(original_services)
        if not optimal_services:
            raise HTTPException(status_code=404, detail="No optimal services could be identified.")

        # Prepare the context for the report
        original_services_data = "\n".join([
            f"- **{service.name}** (Type: {service.type.value})\n  - Cost: ${service.cost}/user/hour\n  - Traffic Upperbound: {service.traffic} units\n  - Description: {service.description}"
            for service in original_services
        ])

        optimal_services_data = "\n".join([
            f"- **{service.name}** (Type: {service.type.value})\n  - Cost: ${service.cost}/user/hour\n  - Traffic Upperbound: {service.traffic} units\n  - Description: {service.description}"
            for service in optimal_services
        ])

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
        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a technical analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7)

        # Extract the report from OpenAI's response
        report = response.choices[0].message.content.strip()
        print(f"Generated technical report: {report}")
        return ReportResponse(report=report)


    except OpenAIError as oe:
        print(f"OpenAI API error: {oe}")
        raise HTTPException(status_code=502, detail="Error communicating with OpenAI API.")
    except Error as db_error:
        print(f"Database error: {db_error}")
        raise HTTPException(status_code=500, detail="Internal server error while accessing the database.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# Define a Root Endpoint for Health Check
@app.get("/")
def read_root():
    return {"message": "Welcome to the StackUnderflow Service Optimizer API!"}


# Shutdown Event to close the DB connection
@app.on_event("shutdown")
def shutdown_event():
    api_handler.close_connection()


# Main function to run the app using Uvicorn
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
