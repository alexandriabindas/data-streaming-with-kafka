import json
import os

from api import get_leaderboard_data
from config import BOOTSTRAP_SERVER, TOPIC_BLITZ, TOPIC_ADD_PLAYER
from kafka import KafkaProducer
from time import sleep

# Set up the Kafka producer
producer = KafkaProducer(bootstrap_servers=[BOOTSTRAP_SERVER],
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))

# Fetch data from chess.com server
data = get_leaderboard_data(TOPIC_BLITZ)

dir_path = 'streamed_data/leaderboards'
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# Write data to an output file
with open(f'streamed_data/leaderboards/{TOPIC_BLITZ}.json', 'w') as f:
    f.write(json.dumps(data) + '\n')
f.close()

count = 0
for row in data:
    print('Sending Message...')
    sleep(1)
    print(f"username: {row['username']}, Rank: {row['rank']}")
    row['game_type'] = TOPIC_BLITZ
    producer.send(TOPIC_ADD_PLAYER, row)
    print(f'Blitz Message #{count + 1} Sent!')
    print('\n-------\n')
    count += 1
