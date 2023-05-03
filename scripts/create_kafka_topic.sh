#!/bin/bash

# Take in argument for the topic name when executing script
if [ $# -ne 1 ]; then
  echo "Usage: $0 <topic_name>"
  exit 1
fi

kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic $1


