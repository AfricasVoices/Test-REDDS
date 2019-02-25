#!usr/bin/env bash

set -e

if [ $# -ne 5 ]; then
    echo "usage: ./2_fetch_raw_data.sh <user> <rapid-pro-root> <rapid-pro-server> <rapid-pro-token> <data-root>"
    echo "Downloads the radio show answers from each show, as well as all the contacts data"
    exit
fi 

USER=$1
RP_DIR=$2
RP_SERVER=$3
RP_TOKEN=$4
DATA_ROOT=$5

TEST_CONTACTS_PATH="$(pwd)/configurations/test_contacts.json"

SHOWS=(
    "internet_working_poll"
    "water_filter_poll"
    "waste_disposal_satisfaction"
    
)

SURVEY=(
  "demogs"
)

./checkout_rapid_pro_tools.sh "$RP_DIR"

mkdir -p "$DATA_ROOT/Raw Data"

# Export radio show messages_datasets
cd "$RP_DIR/fetch_runs"
for SHOW in ${SHOWS[@]}
do 
    echo "Exporting show $SHOW"

    ./docker-run.sh --flow-name "$SHOW" --test-contacts-path "$TEST_CONTACTS_PATH" \
        "$RP_SERVER" "$RP_TOKEN" "$USER" all \
        "$DATA_ROOT/UUIDs/phone_uuids.json" "$DATA_ROOT/Raw Data/$SHOW.JSON"
done

# Export surveys
cd "$RP_DIR/fetch_runs"
for SURVEY in ${SURVEYS[@]}
do
    echo "Exporting surveys $SURVEY"

    .docker-run.sh --flow-name "$SURVEY" --test-contact-path "$TEST_CONTACTS_PATH" \
        "$RP_SERVER" "$RP_TOKEN" "$USER" latest-only \
        "$DATA_ROOT/UUIDs/phone_uuids.json" "$DATA_ROOT/Raw Data/$SURVEY.json"
done

