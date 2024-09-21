from fastapi import FastAPI
from pydantic import BaseModel
from mysql.connector import connect
from mysql.connector.errors import Error
from typing import List, Dict, Any, Optional
from collections import defaultdict
from enum import Enum

DB_HOST = 'stackunderflow.cha8ies4obs2.us-east-1.rds.amazonaws.com'  # Replace with your RDS endpoint
DB_PORT = 3306  # MySQL default port
DB_USER = 'admin'  # Replace with your MySQL username
DB_PASSWORD = '12345678'  # Replace with your MySQL password
DB_NAME = 'StackUnderflow'


# app = FastAPI()

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

class Service(BaseModel):
    name: str
    cost: float
    type: ServiceType
    description: str
    traffic: float

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
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise
    
    def get_services(self, json_obj: Dict[str, Any]) -> List[Service]:
        """
        Unpacks the JSON object to fetch the specified services from the database.

        :param json_obj: A JSON object with 'services' and 'traffic' fields.
        :return: A list of Service models.
        """
        services_names = json_obj.get('services', [])
        services = []

        if not self.connection:
            print("No database connection.")
            return services

        if not services_names:
            print("No services provided in the JSON object.")
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
                service = Service(
                name=row['name'],
                cost=float(row['cost_per_user_per_hour']),
                type=ServiceType(row['type']),  # Ensure this matches your Enum
                description=row.get('detailed_description', ''),
                traffic=float(row.get('traffic_upperbound', 0))
                )
                services.append(service)

            print(f"Fetched {len(services)} services from the database.")

        except Error as e:
            print(f"Error: '{e}' occurred while fetching services.")
        finally:
            if cursor:
                cursor.close()

        return services

    def find_cheapest_highest_traffic_per_type(self, json_obj: Dict[str, Any]) -> List[Service]:
        services = self.get_services(json_obj)
        # Group services by type
        services_by_type = defaultdict(list)
        for service in services:
            services_by_type[service.type].append(service)

        optimal_services = []

        for service_type, service_list in services_by_type.items():
            if service_type is None:
                print(f"Warning: Service type for services {', '.join([s.name for s in service_list])} is unknown.")
                continue  # Skip unknown types

            # Sort services first by cost (ascending), then by traffic (descending)
            sorted_services = sorted(service_list, key=lambda s: (s.cost, -s.traffic))
            # The first service is the cheapest with the highest traffic
            optimal_service = sorted_services[0]
            optimal_services.append(optimal_service)

        print(f"Identified {len(optimal_services)} optimal services across service types.")
        return optimal_services



# Main Function
def main():
    db_handler = API()
    # Example: Fetch all services
    input_json = {
        "services": ["IBM Watson",
    "Zscaler Cloud Firewall",
    "Ping Identity Adaptive MFA",
    "Oracle Autonomous Database",
    "Puppet Enterprise",
    "TravisCI Builds",
    "New Relic Insights",
    "Datadog APM",
    "Azure SQL Database",
    "Fastly Edge Compute"],
        "traffic": 1000
    }
    services = db_handler.get_services(input_json)
    print("Available Services:")
    for service in services:
        print(f"- {service.name} ({service.type.value}): ${service.cost}/hour, {service.traffic} users")

    for service in services:
        print(f"- {service.name}: ${service.cost}/hour")

    # Example: Calculate current cost
    optimal_services = db_handler.find_cheapest_highest_traffic_per_type(input_json)
    print("Optimal Services:")
    for service in optimal_services:
        print(f"- {service.name} ({service.type.value}): ${service.cost}/hour, {service.traffic} users")
    
    # Close the database connection when done
    if db_handler.connection and db_handler.connection.is_connected():
        db_handler.connection.close()
        print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()


