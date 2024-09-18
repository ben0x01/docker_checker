#!/bin/bash

if [ $# -eq 0 ]; then
  echo "No container ID provided."
  exit 1
fi

for container_id in "$@"
do
  container_status=$(docker inspect -f '{{.State.Status}}' $container_id)

  if [ "$container_status" == "exited" ]; then
    echo "Starting container with ID: $container_id"
    docker start $container_id

    sleep 5

    container_status=$(docker inspect -f '{{.State.Status}}' $container_id)

    if [ "$container_status" == "running" ]; then
      echo "Container with ID: $container_id successfully restarted."
    else
      echo "Failed to restart container with ID: $container_id."
    fi
  else
    echo "Container with ID: $container_id is already running or in another state."
  fi
done
