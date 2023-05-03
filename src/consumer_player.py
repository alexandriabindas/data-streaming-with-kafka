import json
import psycopg2

from api import get_player_by_username
from config import (default_consumer_config,
                    BOOTSTRAP_SERVER,
                    GROUP_ID_PLAYER,
                    TOPIC_ADD_PLAYER,
                    TOPIC_ADD_STREAMER
                    )
from kafka import KafkaConsumer


from kafka import KafkaProducer

# Set up the Kafka producer
producer = KafkaProducer(bootstrap_servers=[BOOTSTRAP_SERVER],
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))

player_topics = [TOPIC_ADD_PLAYER, TOPIC_ADD_STREAMER]


# Initalize the Kafka consumers
player_consumer = KafkaConsumer(**default_consumer_config,
                                group_id=GROUP_ID_PLAYER,
                                value_deserializer=lambda m: json.loads(m.decode('utf-8')))


# Convert the topic to a set
player_topic_set = set(player_topics)

# Subscribe each consumer to a set of topics
player_consumer.subscribe(player_topic_set)
print(
    f'Player consumer is successfully subscribed to: {player_topic_set}')

# Initalize the postgres database connection
conn = psycopg2.connect(host="localhost", database="chess.com",
                        user="postgres", password="password")
cursor = conn.cursor()


# Cache usernames to prevent uneeded requests
usernames_cache = set()
for message in player_consumer:
    print(f'Message recieved from {message.topic}.')
    print(message)
    # message_dict = json.loads(message.value)
    username = message.value['username']
    username = username.lower()
    # TODO: Fix this because its broken
    # if username not in usernames_cache:
    #     usernames_cache.add(username)

    # Execute the SQL query to see if player exists
    cursor.execute(
        "SELECT * FROM Player WHERE username = %s", (str(username),))
    # Fetch all the matching records
    matching_records = cursor.fetchall()
    if not matching_records:
        print(
            f'Player with username ({username}) is being inserted into the DB...')
        print('\n')
        try:
            data = get_player_by_username(username)
            cursor.execute("""
                INSERT INTO Player
                (player_id, username, player_title, player_status, player_name, player_location,
                 player_country, joined_on, last_online, followers, is_streamer)
                VALUES (%s, %s, %s, %s, %s, %s, %s, to_timestamp(%s), to_timestamp(%s), %s, %s)
            """, (
                data.get('player_id'),
                data.get('username'),
                data.get('title'),
                data.get('status'),
                data.get('name'),
                data.get('location'),
                data.get('country'),
                data.get('joined'),
                data.get('last_online'),
                data.get('followers'),
                data.get('is_streamer')
            ))
        except Exception as e:
            print(e)
        # Commit the transaction and close the database connection
        conn.commit()
    else:
        print(f'User {username} already in DB')
    if message.topic != TOPIC_ADD_STREAMER:
        # Send the data to the corresponding leaderboard consumer
        producer.send(message.value['game_type'], value=message.value)

conn.close()
