export action=$1
export resource_type=$2
export resource_path=$3
export custom_datastore=$4

# Check environment variables for GOOGLE_APPLICATION_CREDENTIALS, which should be the path to credentials file; stops process running script otherwise
[ -z "$GOOGLE_APPLICATION_CREDENTIALS" ] && echo "Must have GOOGLE_APPLICATION_CREDENTIALS environment variable set to path of your credentials file!" && exit 1

# Check if gcloud project is set, if not lets user know and exits
export project_id=$(gcloud config get-value project)
[ -z "$project_id" ] && echo "Must have gcloud project config variable set, please run: gcloud init" && exit 1
echo "Project ID that is being used: $project_id"

# Check if gcloud region is set, if not lets user know and exits
export cloud_region=$(gcloud config get-value compute/region)
[ -z "$cloud_region" ] && echo "Must have gcloud compute/region config variable set, please run: gcloud init and set a default region and zone"  && exit 1
echo "Project Region that is being used: $cloud_region"

# Check if a FHIR Dataset exists
export fhir_dataset=$(gcloud healthcare datasets list --location=$cloud_region --format="value(name)" | head -n 1)
[ -z "$fhir_dataset" ] && echo "No FHIR datasets were found, please ensure that you have created a FHIR dataset and it is in the region mentioned above" && exit 1
echo "FHIR dataset that is being used: $fhir_dataset"

# Check if a FHIR Datastore exists [within above dataset]
export fhir_datastore=$(gcloud healthcare fhir-stores list --dataset=$fhir_dataset --location=$cloud_region --format="value(name)" | head -n 1)
[ -z "$fhir_datastore" ] && echo "No FHIR datastore were found, please ensure that you have created a FHIR datastore within the FHIR dataset mentioned above" && exit 1
[ ! -z "$custom_datastore" ] && export fhir_datastore=$custom_datastore

# Executes main code
python code.py \
--action=$action \
--resource_type=$resource_type \
--resource_path=$resource_path \
--credentials=$GOOGLE_APPLICATION_CREDENTIALS \
--project_id=$project_id \
--region=$cloud_region \
--fhir_dataset=$fhir_dataset \
--fhir_datastore=$fhir_datastore