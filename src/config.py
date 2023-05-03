
import json

BOOTSTRAP_SERVER = 'localhost:9092'

GROUP_ID_LEADERBOARD = 'leaderboard'
GROUP_ID_PLAYER = 'player'

# Topics available for subscription
TOPIC_BLITZ = 'live_blitz'
TOPIC_RAPID = 'live_rapid'
TOPIC_DAILY = 'daily'
TOPIC_ADD_PLAYER = 'add-player'
TOPIC_ADD_STREAMER = 'add-streamer'

# Default Kafka producer config
default_producer_config = {
    'bootstrap_servers': [BOOTSTRAP_SERVER]
}


# Default Kafka consumer config
default_consumer_config = {
    'bootstrap_servers': 'localhost:9092',
    'auto_offset_reset': 'earliest',
    'enable_auto_commit': True
}
