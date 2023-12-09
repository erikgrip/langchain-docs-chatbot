#!/usr/bin/env bash

build=false
while [[ $# -gt 0 ]]
do
    case $1 in
        --build)
            build=true
            shift  # Past key
            ;;
        -f|--force_data_download)
            force_data_download="$2"
            shift 2  # Past key and value to next argument
            ;;
        -d|--delete_persisted_db)
            delete_persisted_db="$2"
            shift 2
            ;;
        -n|--num_retrieved_docs)
            num_retrieved_docs="$2"
            shift 2
            ;;
        -t|--temperature)
            temperature="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# Build docker image if --build flag is passed or if image doesn't exist
if [ "$build" = true ] || [ ! "$(docker images -q langchain-docs-chatbot 2> /dev/null)" ]; then
    poetry export -f requirements.txt --output docker/requirements.txt --without dev --without-hashes
    docker build -t langchain-docs-chatbot -f ./docker/Dockerfile .  --no-cache
    rm ./docker/requirements.txt
fi

# Concat args to pass to docker run command
if [ -n "$force_data_download" ]; then
    app_args+=" --force_data_download $force_data_download"
fi
if [ -n "$delete_persisted_db" ]; then
    app_args+=" --delete_persisted_db $delete_persisted_db"
fi
if [ -n "$num_retrieved_docs" ]; then
    app_args+=" --num_retrieved_docs $num_retrieved_docs"
fi
if [ -n "$temperature" ]; then
    app_args+=" --temperature $temperature"
fi

# shellcheck disable=SC2086
docker run --rm -p 8501:8501 -v ./data:/data --env-file .env langchain-docs-chatbot $app_args  
