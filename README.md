# GCP Healthcare API - FHIR Datastore Interaction

## How to use

- Clone repo
- Set up python virtual environment
- Source virtual environment, install requirements `pip install -r requirements.txt`
- Make sure gcloud healthcare API is enabled, and that a dataset with a FHIR datastore is created (R4 spec is recommended)
- Run main script with needed variables: 
    ```
    python code.py \
    --action=[Get or Create] \
    --resource_type=[FHIR resource type e.g., Patient or Organization or Claim] \
    --resource_path=[Path to JSON that has resource definition, examples in resources] \
    --credentials=[/path/to/credentials] \
    --project_id=[Project_ID] \
    --cloud_region=[Preferred_Region] \
    --fhir_dataset=[FHIR_Dataset_ID] \
    --fhir_datastore=[FHIR_Datastore_ID]
    ```

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