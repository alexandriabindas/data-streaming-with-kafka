import json
import psycopg2

from config import (default_consumer_config,
                    GROUP_ID_LEADERBOARD,
                    TOPIC_RAPID,
                    TOPIC_BLITZ,
                    TOPIC_DAILY)
from kafka import KafkaConsumer

leaderboard_topics = [TOPIC_RAPID, TOPIC_BLITZ, TOPIC_DAILY]

# Initalize the Kafka consumer
consumer = KafkaConsumer(**default_consumer_config,
                         group_id=GROUP_ID_LEADERBOARD)

topic_set = set(leaderboard_topics)

# Subscribe to a set of topics
consumer.subscribe(topic_set)
print(
    f'Leaderboard consumer is successfully subscribed to: {leaderboard_topics}')

conn = psycopg2.connect(host="localhost", database="chess.com",
                        user="postgres", password="password")
cursor = conn.cursor()

# Store aggregated data in a dictionary
aggregated_data = {}
for message in consumer:
    print(f'Leaderboard message received ({message.topic})!')
    data = json.loads(message.value)
    username = data['username'].lower()
    print(username)

    # for data in data:
    # print(data)
    player_id = data['player_id']
    player_rank = data['rank']
    player_name = data.get('name')
    # print(player_rank)
    # print(player_name)
    cursor.execute(
        "SELECT * FROM Player WHERE username = %s", (str(username),))
    # Fetch all the matching player record in the postgres DB
    player_record = cursor.fetchone()
    if player_record:
        player_id = player_record[0]
        print('found player record in DB')
        print(player_record)
        query = "INSERT INTO Leaderboard (player_id, gametype, playerRank, score, winCount, lossCount, drawCount) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        cursor.execute(query, (player_id, data.get('game_type'), data.get(
            'rank'), data.get('score'), data.get('win_count'), data.get('loss_count'), data.get('draw_count')))
        # Commit the transaction and close the database connection
        conn.commit()
conn.close()
