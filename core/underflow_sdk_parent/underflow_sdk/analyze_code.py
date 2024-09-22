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

PROMPT = "EC2, S3, Lambda, RDS, Azure Virtual Machines, Azure Blob Storage, Azure Functions, Azure SQL Database, Google Compute Engine, Google Cloud Storage, Google Kubernetes Engine, Google BigQuery, IBM Watson, IBM Cloud Functions, Oracle Autonomous Database, Oracle Cloud Infrastructure Compute, DigitalOcean Droplets, DigitalOcean Spaces, Heroku Dynos, Heroku Postgres, Netlify Build, Netlify Functions, Vercel Deployments, Vercel Serverless Functions, Firebase Realtime Database, Firebase Authentication, GitHub Actions, GitHub Packages, GitLab CI/CD, GitLab Container Registry, Bitbucket Pipelines, Bitbucket Deployments, CircleCI Orbs, CircleCI Workflows, TravisCI Builds, TravisCI Deployments, Docker Containers, Docker Hub, Kubernetes Clusters, Kubernetes Helm, Jenkins Pipelines, Jenkins Plugins, Ansible Playbooks, Ansible Galaxy, Puppet Modules, Puppet Enterprise, Chef Recipes, Chef Automate, Datadog APM, Datadog Logs, New Relic Insights, New Relic Alerts, Splunk Enterprise, Splunk Cloud, Prometheus Metrics, Prometheus Alertmanager, Grafana Dashboards, Grafana Loki, Sentry Error Tracking, Sentry Performance, PagerDuty Incident Response, PagerDuty On-Call Scheduling, Twilio SMS API, Twilio Voice API, SendGrid Email API, SendGrid Marketing Campaigns, Mailgun SMTP, Mailgun Validation, Cloudflare CDN, Cloudflare DNS, Fastly Edge Compute, Fastly Image Optimization, Akamai Edge Security, Akamai CDN, Zscaler Secure Web Gateway, Zscaler Cloud Firewall, Okta Single Sign-On, Okta Multi-Factor Authentication, Auth0 Universal Login, Auth0 Rules, OneLogin Single Sign-On, OneLogin Multi-Factor Authentication, Ping Identity Single Sign-On, Ping Identity Adaptive MFA, Stripe Payments, Stripe Billing, PayPal Checkout, PayPal Payouts, Square POS, Square Online Checkout, Braintree Gateway, Braintree Marketplace, Shopify Payments, Shopify Plus, Magento Commerce, Magento Cloud, Wix Editor, Wix SEO Tools, Weebly Drag-and-Drop Builder, Weebly E-commerce, WordPress Themes, WordPress Plugins, Contentful Content Delivery API, Contentful Content Management API, Strapi API Builder, Strapi Content Types, Slack Channels, Slack Integrations, Zoom Meetings, Zoom Webinars, Microsoft Teams Channels, Microsoft Teams Apps, Discord Servers, Discord Bots, Trello Boards, Trello Power-Ups, Asana Projects, Asana Timelines, Jira Issues, Jira Workflows, Notion Pages, Notion Databases, Evernote Notebooks, Evernote Templates, Dropbox File Sync, Dropbox Paper, Box Content Management, Box Integrations, OneDrive File Sync, OneDrive for Business. Detect which external services in the given list are used in the following code. Return a list of of the exact same service names only. Only return a list, separated by a comma. Do not return any other text."

def check_for_external_services(code_str: str, traffic: int):
    resp = cerebras_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": PROMPT,
            },
            {"role": "user", "content": code_str},
        ],
        model="llama3.1-70b",
        temperature=0.0,
    )

    url_original_service = "http://localhost:8000/original-services"
    url_optimal_service = "http://localhost:8000/optimal-services"
    url_tech_report = "http://localhost:8000/generate-report"

    services = resp.choices[0].message.content.split(", ")
    print(services)
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
