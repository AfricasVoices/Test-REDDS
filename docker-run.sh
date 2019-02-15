#!/bin/bash

set -e

IMAGE_NAME=test-redds

while [[ $# -gt 0]]; do
    case "$1" in 
        --profile-cpu)
            PROFILE_CPU=true
            CPU_PROFILE_OUTPUT_PATH="$2"
            shift 2;;
        --drive-upload)
            DRIVE_UPLOAD=true 

            DRIVE_SERVICE_ACCOUNT_CREDENTIALS_URL=$2
            MESSAGES_DRIVE_PATH=$3
            INDIVIDUALS_DRIVE_PATH=$4
            PRODUCTION_DRIVE_PATH=$5
            shift 5;;
        --)
            shift
            break;;
        *)
            break;;      
        esac
    done 

#Check that the correct number of arguments were provided
if [[ $# -ne 17 ]]; then 
    echo "Usage: ./docker-run.sh 
    [--profile-cpu <profile-output-path>] 
    [--drive-upload <drive-auth-file> <messages-drive-path> <individuals-drive-path> <production-drive-path>]
    <user> <phone-number-uuid-table-path> 
    <internet_working_poll-input-path> <water_filter_poll-input-path> <waste_disposal-input-path> <demog-input-path> <prev-coded-dir>
    <json-output-path> <icr-output-dir> <coded-output-dir> <messages-output-csv> <individuals-output-csv> <production-output-csv>"
    exit
fi

# Assign the program arguments to bash variables
USER=$1
INPUT_PHONE_UUID_TABLE=$2
INPUT_INTERNET=$3
INPUT_WATER=$4
INPUT_WASTE=$5
INPUT_DEMOGS=$6
PREV_CODED_DIR=$7
OUTPUT_JSON=${8}
OUTPUT_ICR_DIR=${9}
OUTPUT_CODED_DIR=${10}
OUTPUT_MESSAGES_CSV=${11}
OUTPUT_PRODUCTION_CSV=${13}

# Build an image for this pipeline stage
docker build --build-arg INSTALL_CPU_PROFILER="$PROFILER_CPU" -t "$IMAGE_NAME" .

# Create a container from the image that was just built
# when run,the container will:
# - Copy the service account credentials from the gcloud bucket url 'SERVICE_ACCOUNT_CREDENTIALS_URL'.
# - Run the pipeline
# The gcloud bucket access is authorised via volume mounting (-v in the docker container create command)
if [[ "$PROFILE_CPU" = true ]]; then
    PROFILER_CPU_CMD="pyflame -o /data/cpu.prof -t"
    SYS_PTRACE_CAPABILITY="--cap-add SYS_PTRACE"
fi
if [[ "$DRIVE_UPLOAD" = true ]]; then
    GSUTIL_CP_CMD="gsutil cp \"$SERVICE_ACCOUNT_CREDENTIALS_URL\" /root/.config/drive-service-account-credentials.json &&"
    DRIVE_UPLOAD_ARG="--drive-upload /root/.config/drive-service-account-credentials.json \"$MESSAGES_DRIVE_PATH\" \"$INDIVIDUALS_DRIVE_PATH\" \"$PRODUCTION_DRIVE_PATH\""

fi

CMD="
    $GSUTIL_CP_CMD \

    pipenv run $PROFILE_CPU_CMD python -u test_pipeline.py $DRIVE_UPLOAD_ARG \
    \"$USER\" /data/phone-number-uuid-table-input.json \
    /data/internet_working-input.json /data/water_filter-input.json /data/waste_disposal-input.json \
    /data/demog-input.json /data/prev-coded \ /data/output.json /data/ouput-icr /data/coded
    /data/output-messages.csv /data/output-indivuals.csv /data/output-production-csv \
"

container="$(docker container create ${SYS_PTRACE_CAPABILITY} -v=$HOME/.config/gcloud:root/.config/gcloud -w /app "$IMAGE_NAME" /bin/bash -c "$CMD")"

function finish {
    #Tear down the container when done.
    docker container rm "$container">/dev/null

}
trap finish EXIT 

#Copy input data into the container
docker cp "$INPUT_PHONE_UUID_TABLE" "$container:/data/phone-number-uuid-table-input.json"
docker cp "$INPUT_INTERNET" "$container:/data/internet_working-input.json"
docker cp "$INPUT_WATER" "$container:/data/water_filter-input.json"
docker cp "$INPUT_WASTE" "$container:/data/waste_disposal-input.json"
docker cp "$INPUT_DEMOG" "$container:/data/demog-input.json"

if [ -d "$PREV_CODED_DIR" ]; then
    docker cp "$PREV_CODED_DIR" "$container:/data/prev-coded"
fi 

# Run the container
docker start -a -i "$container"

#Copy the output data back out of the container
mkdir -p "$(dirname "$OUTPUT_JSON")"
docker cp "$container:/data/output.json" "$OUTPUT_JSON"

mkdir -p "$OUTPUT_ICR_DIR"
docker cp "$container:/data/output-icr/." "$OUTPUT_ICR_DIR"

mkdir -p "$OUTPUT_CODED_DIR"
docker cp "$container:/data/output-messages-csv" "$OUTPUT_MESSAGES_CSV"

mkdir -p "$(dirname "$OUTPUT_MESSAGES_CSV")"
docker cp "$container:/data/output-messages.csv" "$OUTPUT_MESSAGES_CSV"

mkdir -p "$(dirname "$OUTPUT_INDIVIDUALS_CSV")"
docker cp "$container:/data/output-individuals.csv" "$OUTPUT_INDIVIDUALS_CSV"

mkdir -p "$(dirname "$OUTPUT_PRODUCTION_CSV")"
docker cp "$container:/data/output-production.csv" "$OUTPUT_PRODUCTION_CSV"
