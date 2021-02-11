import json
import os
import argparse

from google.auth.transport import requests
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.errors import HttpError

def parse_command_line_args():
    """Parses command line arguments."""

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--credentials",
        default=None,
        help="Path to your service account credentials",
    )

    parser.add_argument(
        "--project_id",
        default=None,
        help="Google cloud project id (not fully qualified)",
    )

    parser.add_argument(
        "--cloud_region",
        default="us-west2",
        help="Cloud region to use",
    )

    parser.add_argument(
        "--fhir_dataset",
        default="us-west2",
        help="FHIR dataset to target",
    )

    parser.add_argument(
        "--fhir_datastore",
        default="us-west2",
        help="FHIR datastore to target",
    )

    parser.add_argument(
        "--resource_type",
        default=None,
        help="The type of resource. First letter must be capitalized",
    )

    parser.add_argument(
        "--resource_path",
        default=None,
        help="The path to JSON that has resource definition, examples in resources",
    )

    parser.add_argument(
        "--action",
        default=None,
        help="Action performed by script, either Get or Create [a resource]",
    )

    return parser.parse_args()

def get_client(service_account_json):
    """Returns an authorized API client by discovering the Healthcare API and
    creating a service object using the service account credentials JSON."""
    api_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    api_version = "v1beta1"
    discovery_api = "https://healthcare.googleapis.com/$discovery/rest"
    service_name = "healthcare"

    credentials = service_account.Credentials.from_service_account_file(
        service_account_json
    )
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = "{}?labels=CHC_BETA&version={}".format(discovery_api, api_version)

    return discovery.build(
        service_name,
        api_version,
        discoveryServiceUrl=discovery_url,
        credentials=scoped_credentials,
    )

def get_session(service_account_json):
    """
    Returns an authorized Requests Session class using the service account
    credentials JSON. This class is used to perform requests to the
    Healthcare API endpoint.
    """

    # Pass in the credentials and project ID. If none supplied, get them
    # from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        service_account_json
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )

    # Create a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    return session

def create_resource(resource_type, claim_path):
    url = f"{base_url}/projects/{project_id}/locations/{cloud_region}"
    fhir_store_path = f"{url}/datasets/{dataset_id}/fhirStores/{fhir_store_id}/fhir/{resource_type}"
    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}
    with open(claim_path) as f: 
        resource_content = json.load(f)
    response = session.post(fhir_store_path, headers=headers, json=resource_content)
    response.raise_for_status()
    resource = response.json()
    resource_id = resource['id']

    with open("resource_id.txt", "a") as f:
        f.write(f"New {resource_type} has been created with {resource_id}\n")

    print(f"Created {resource_type} resource with ID {resource_id}")

def create_dataset(dataset_id):
    """Creates a dataset."""
    dataset_parent = "projects/{}/locations/{}".format(project_id, cloud_region)

    body = {}

    request = (
        client.projects()
        .locations()
        .datasets()
        .create(parent=dataset_parent, body=body, datasetId=dataset_id)
    )

    try:
        response = request.execute()
        print("Created dataset: {}".format(dataset_id))
        return response
    except HttpError as e:
        print("Error, dataset not created: {}".format(e))
        return ""

def search_resources_get(resource_type):
    """
    Searches resources in the given FHIR store.

    It uses the searchResources GET method.
    """
    url = "{}/projects/{}/locations/{}".format(base_url, project_id, cloud_region)

    resource_path = "{}/datasets/{}/fhirStores/{}/fhir/{}".format(
        url, dataset_id, fhir_store_id, resource_type
    )

    response = session.get(resource_path)
    response.raise_for_status()

    resources = response.json()

    print(
        "Using GET request, found a total of {} {} resources:".format(
            resources["total"], resource_type
        )
    )
    print(json.dumps(resources, indent=2))

    return resources

def get_resource(resource_type, resource_id):

# Parse arguments
parser = parse_command_line_args()
credentials = parser.credentials
project_id = parser.project_id
cloud_region = parser.region
dataset_id = parser.fhir_dataset
fhir_store_id = parser.fhir_datastore

# Initialize session and client
base_url = "https://healthcare.googleapis.com/v1"
session = get_session(credentials)
client = get_client(credentials)

if parser.action == "Create":
    create_resource(parser.resource_type, parser.resource_path)

if parser.action == "Get":
    get_resource(parser.resource_type, parser.resource_id)

# search_response = search_resources_get("Patient")

# with open("output.json", "w") as f:
#     json.dump(search_response, f, indent=4, ensure_ascii=False)