cd /usr/local/Cellar/kafka/3.4.0

bin/zookeeper-server-start.sh config/zookeeper.properties

# Install Kafka 

Follow these docs: https://kafka.apache.org/quickstart

# Start Zookeeper

`zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties & kafka-server-start /usr/local/etc/kafka/server.properties`

# Create topic

kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic leaderboard

# Running The Project

1. Start Zookeeper: `./scripts/start_zookeeper.sh`

2. Start Kafka Server: `./scripts/start_kafka_server.sh`

3. Web UI: `docker run -it -p 8080:8080 -e DYNAMIC_CONFIG_ENABLED=true provectuslabs/kafka-ui`

4. Run the producer python files

5. Run the consumers
