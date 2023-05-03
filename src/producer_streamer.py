import json
import os

from api import get_streamers
from config import BOOTSTRAP_SERVER, TOPIC_ADD_STREAMER
from kafka import KafkaProducer
from time import sleep

# Set up the Kafka producer
producer = KafkaProducer(bootstrap_servers=[BOOTSTRAP_SERVER],
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))

# Fetch data from chess.com server
data = get_streamers()

dir_path = 'streamed_data/streamers'
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# Write data to an output file
with open(f'streamed_data/streamers/{TOPIC_ADD_STREAMER}.json', 'w') as f:
    f.write(json.dumps(data) + '\n')
f.close()

for row in data:
    print('Sending Message (streamers)...')
    sleep(3)
    producer.send(TOPIC_ADD_STREAMER, row)
    print('\n-------\n')
