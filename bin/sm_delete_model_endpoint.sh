#!/bin/bash

display_usage() {
	echo -e "Usage: $0 falcon40b|llama2|j2_ultra\n"
}

if [[ $# -lt 1 ]]
then
  display_usage
  exit 1
fi

MODEL_NAME=$1
ENDPOINT_NAME="hf-llm-falcon-40b-instruct-bf16-2023-08-01-09-12-18-671"

if [[ $MODEL_NAME == "falcon40b" ]]; then
     ENDPOINT_NAME="hf-llm-falcon-40b-instruct-bf16-2023-08-01-09-12-18-671"
elif [[ $MODEL_NAME == "llama2" ]]; then
     ENDPOINT_NAME="jumpstart-dft-meta-textgeneration-llama-2-70b-f"
elif [[ $MODEL_NAME == "j2_ultra" ]]; then
     ENDPOINT_NAME="j2-ultra"
fi

echo "Deleting endpoint: $ENDPOINT_NAME"

aws sagemaker delete-endpoint --endpoint-name "$ENDPOINT_NAME" --region us-east-1