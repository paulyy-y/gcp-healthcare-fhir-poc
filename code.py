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
        "--resource_id",
        default=None,
        help="Google cloud project id (not fully qualified)",
    )

    parser.add_argument(
        "--region",
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
    # Generate URL
    fhir_store_path = f"{base_url}/datasets/{dataset_id}/fhirStores/{fhir_store_id}/fhir/{resource_type}"
    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    # Deserialize resource definition
    with open(claim_path) as f: 
        resource_content = json.load(f)

    # Execute request
    response = session.post(fhir_store_path, headers=headers, json=resource_content)
    response.raise_for_status()
    resource = response.json()

    # Catalog and display result
    resource_id = resource['id']
    with open("resource_id.txt", "a") as f:
        f.write(f"New {resource_type} has been created with {resource_id}\n")
    print(f"Created {resource_type} resource with ID {resource_id}")

def create_dataset(dataset_id):
    """Creates a dataset."""

    body = {}

    request = (
        client.projects()
        .locations()
        .datasets()
        .create(parent=base_url, body=body, datasetId=dataset_id)
    )

    try:
        response = request.execute()
        print(f"Created dataset: {dataset_id}")
        return response
    except HttpError as e:
        print(f"Error, dataset not created: {e}")
        return ""

def search_resources_get(resource_type):
    """
    Searches resources in the given FHIR store.

    It uses the searchResources GET method.
    """
    resource_path = f"{base_url}/datasets/{dataset_id}/fhirStores/{fhir_store_id}/fhir/{resource_type}"

    response = session.get(resource_path)
    response.raise_for_status()

    resources = response.json()
    total_resources = resources["total"]

    print(f"Using GET request, found a total of {total_resources} {resource_type} resources:")
    print(json.dumps(resources, indent=4))

    return resources

def get_resource(resource_type, resource_id):
    # Prepare request
    resource_path = f"{base_url}/datasets/{dataset_id}/fhirStores/{fhir_store_id}/fhir/{resource_type}/{resource_id}"
    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    # Execute request
    response = session.get(resource_path, headers=headers)
    response.raise_for_status()
    resource = response.json()
    resourceType = resource["resourceType"]

    # Print results
    print(f"Got {resourceType} resource:")
    print(json.dumps(resource, indent=2))

    # Return results
    return resource

# Parse arguments
parser = parse_command_line_args()
credentials = parser.credentials
project_id = parser.project_id
cloud_region = parser.region
dataset_id = parser.fhir_dataset
fhir_store_id = parser.fhir_datastore
resource_type = parser.resource_type
resource_path = parser.resource_path
resource_id = parser.resource_id


# Initialize session and client
api_url = "https://healthcare.googleapis.com/v1"
base_url = f"{api_url}/projects/{project_id}/locations/{cloud_region}"

session = get_session(credentials)
client = get_client(credentials)

if parser.action == "Create":
    create_resource(resource_type, resource_path)

if parser.action == "Get":
    get_resource(resource_type, resource_id)

# search_response = search_resources_get("Patient")

# with open("output.json", "w") as f:
#     json.dump(search_response, f, indent=4, ensure_ascii=False)