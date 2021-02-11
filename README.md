# GCP Healthcare API - FHIR Datastore Interaction

## Execution Guide

- Clone this repo 
- Set up Python 3 (must be Python 3) virtual environment `python3 -m virtualenv venv`
- Source virtual environment `source venv/bin/activate`
- Install python requirements `pip install -r requirements.txt`
- Make sure gcloud healthcare API is enabled, and that a dataset with a FHIR datastore is created (R4 spec is recommended)

*Ensure the following (these are checked during the shell script init anyways, but saves you some time upfront if you confirm all is in order)*
1. GOOGLE_APPLICATION_CREDENTIALS environment variable is set to your service account credentials file (not sure? `echo $GOOGLE_APPLICATION_CREDENTIALS`)
2. Ensure that you have ran `gcloud init` and set a default region and project
3. Ensure that you have created a FHIR dataset within the default region and project in (3) [GCP Healthcare Browser](https://console.cloud.google.com/healthcare)
4. Ensure that you have created a FHIR datastore within the dataset mentioned in (4) [GCP Healthcare Browser](https://console.cloud.google.com/healthcare)

Finally - execute the run.sh file with arguments for:
- action (either Create or Get)
- resource_type (Claim/Coverage/Patient etc. just make sure you have a corresponding resource JSON) 
- resource_path (resources/Claim.json)
- Example: `bash run.sh Create Patient resources/Patient.json`

## FHIR

Resource Examples (in resources folder) are sourced from respective FHIR example pages: 
- Claim: https://www.hl7.org/fhir/r4/claim-examples.html
- Patient: https://www.hl7.org/fhir/r4/patient-examples.html

FHIR R4 Overview https://www.hl7.org/fhir/r4/

FHIR Specifications: R4, STU3, DSTU1 (R4 being newest)

## Potential Improvements

- Web UI POC (browse datasets/datastores/resources)
- Pub/Sub Integration (Out-of-Box Support)
- BigQuery Integration (Out-of-Box Support)

## Overview

All Cloud Healthcare API usage occurs within the context of a Google Cloud project. A project organizes all your Google Cloud resources. A project consists of a set of users; a set of APIs; and billing, authentication, and monitoring settings for those APIs. So, for example, all of your Cloud Healthcare API data and resources, along with user permissions for accessing them, reside in a project. You can have one project, or you can create multiple projects and use them to organize your Google Cloud resources, including your Cloud Healthcare API data, into logical groups.

## Datasets and data stores
A dataset is a container in your Google Cloud project that holds modality-specific healthcare data. Datasets contain other data stores, such as FHIR stores, DICOM stores, and HL7v2 stores, which in turn hold their own types of healthcare data.

A single dataset can contain one or many data stores, and those stores can all service the same modality or different modalities as application needs dictate. Using multiple stores in the same dataset might be appropriate in various situations, such as:

- If an application processes different types of data, such as a DICOM store used for CT scans and a FHIR store for patient data related to the CT scans.
- To separate data according to its source hospital, clinic, department, and so forth.

An application can access as many datasets or stores as its requirements dictate with no performance penalty. You can design your overall dataset and store architecture to meet your goals for locality, partitioning, access control, and so forth.

The following diagram shows a single Google Cloud project containing two datasets. Each dataset contains multiple data stores, and each data store contains healthcare data:

<img src="https://cloud.google.com/healthcare/images/chc_api_diagram.svg" width="700" />