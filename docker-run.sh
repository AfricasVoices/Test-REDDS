#!/bin/bash

set -e

IMAGE_NAME=test-redds

while [[ $# -gt 0 ]]; do
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

# Check that the correct number of arguments were provided.
if [[ $# -ne 13 ]]; then 
    echo "Usage: ./docker-run.sh 
    [--profile-cpu <profile-output-path>] 
    [--drive-upload <drive-auth-file> <messages-drive-path> <individuals-drive-path> <production-drive-path>]
    <user> <phone-number-uuid-table-path> 
    <internet-working-poll-input-path> <water-filter-poll-input-path> <waste-disposal-input-path> <demog-input-path> <prev-coded-dir>
    <json-output-path> <icr-output-dir> <coded-output-dir> <messages-output-csv> <individuals-output-csv> <production-output-csv>"
    exit
fi

# Assign the program arguments to bash variables
USER=$1
INPUT_PHONE_UUID_TABLE=$2
INPUT_INTERNET=$3
INPUT_WATER=$4
INPUT_WASTE=$5
INPUT_DEMOG=$6
PREV_CODED_DIR=$7
OUTPUT_JSON=${8}
OUTPUT_ICR_DIR=${9}
OUTPUT_AUTO_CODED_CODA_DATASETS=${10}
OUTPUT_MESSAGES_CSV=${11}
OUTPUT_INDIVIDUALS_CSV=${12}
OUTPUT_PRODUCTION_CSV=${13}

# Build an image for this pipeline stage.
docker build --build-arg INSTALL_CPU_PROFILE="$PROFILE_CPU" -t "$IMAGE_NAME" .

# Create a container from the image that was just built.
# When run, the container will:
#  - Copy the service account credentials from the google cloud storage url 'SERVICE_ACCOUNT_CREDENTIALS_URL',
#    if the --drive-upload flag has been set.
#    The google cloud storage access is authorised via volume mounting (-v in the docker container create command).
#  - Run the pipeline.
# The gcloud bucket access is authorised via volume mounting (-v in the docker container create command)
if [[ "$PROFILE_CPU" = true ]]; then
    PROFILE_CPU_CMD="pyflame -o /data/cpu.prof -t"
    SYS_PTRACE_CAPABILITY="--cap-add SYS_PTRACE"
fi
if [[ "$DRIVE_UPLOAD" = true ]]; then
    GSUTIL_CP_CMD="gsutil cp \"$DRIVE_SERVICE_ACCOUNT_CREDENTIALS_URL\" /root/.config/drive-service-account-credentials.json &&"
    DRIVE_UPLOAD_ARG="--drive-upload /root/.config/drive-service-account-credentials.json \"$MESSAGES_DRIVE_PATH\" \"$INDIVIDUALS_DRIVE_PATH\" \"$PRODUCTION_DRIVE_PATH\""
fi

CMD="
    $GSUTIL_CP_CMD \

    pipenv run $PROFILE_CPU_CMD python -u test_pipeline.py $DRIVE_UPLOAD_ARG \
    \"$USER\" /data/phone-number-uuid-table-input.json \
    /data/internet-working-input.json /data/water-filter-input.json /data/waste-disposal-input.json \
    /data/demog-input.json /data/prev-coded /data/output.json /data/output-icr /data/coded \
    /data/output-messages.csv /data/output-individuals.csv /data/output-production.csv \
"

container="$(docker container create ${SYS_PTRACE_CAPABILITY} -v=$HOME/.config/gcloud:/root/.config/gcloud -w /app "$IMAGE_NAME" /bin/bash -c "$CMD")"

function finish {
    # Tear down the container when done.
    docker container rm "$container" >/dev/null
}
trap finish EXIT 

# Copy input data into the container
docker cp "$INPUT_PHONE_UUID_TABLE" "$container:/data/phone-number-uuid-table-input.json"
docker cp "$INPUT_INTERNET" "$container:/data/internet-working-input.json"
docker cp "$INPUT_WATER" "$container:/data/water-filter-input.json"
docker cp "$INPUT_WASTE" "$container:/data/waste-disposal-input.json"
docker cp "$INPUT_DEMOG" "$container:/data/demog-input.json"
if [[ -d "$PREV_CODED_DIR" ]]; then
    docker cp "$PREV_CODED_DIR" "$container:/data/prev-coded"
fi 

# Run the container
docker start -a -i "$container"

# Copy the output data back out of the container
mkdir -p "$(dirname "$OUTPUT_JSON")"
docker cp "$container:/data/output.json" "$OUTPUT_JSON"

mkdir -p "$OUTPUT_ICR_DIR"
docker cp "$container:/data/output-icr/." "$OUTPUT_ICR_DIR"

mkdir -p "$OUTPUT_AUTO_CODED_CODA_DATASETS"
docker cp "$container:/data/coded/." "$OUTPUT_AUTO_CODED_CODA_DATASETS"

mkdir -p "$(dirname "$OUTPUT_MESSAGES_CSV")"
docker cp "$container:/data/output-messages.csv" "$OUTPUT_MESSAGES_CSV"

mkdir -p "$(dirname "$OUTPUT_INDIVIDUALS_CSV")"
docker cp "$container:/data/output-individuals.csv" "$OUTPUT_INDIVIDUALS_CSV"

mkdir -p "$(dirname "$OUTPUT_PRODUCTION_CSV")"
docker cp "$container:/data/output-production.csv" "$OUTPUT_PRODUCTION_CSV"

if [[ "$PROFILE_CPU" = true ]]; then
    mkdir -p "$(dirname "$CPU_PROFILE_OUTPUT_PATH")"
    docker cp "$container:/data/cpu.prof" "$CPU_PROFILE_OUTPUT_PATH"
fi
