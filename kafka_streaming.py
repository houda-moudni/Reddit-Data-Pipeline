import logging
import json
import time
from confluent_kafka import Producer
import praw
from confluent_kafka.admin import AdminClient, NewTopic
import logging
import datetime

client_id = 'client_id'
client_secret = 'client_secret'
user_agent = 'reddit_data_pipeline'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

admin_config = {
    'bootstrap.servers': 'kafka1:29092,kafka2:29093,kafka3:29094', 
    'client.id': 'kafka_admin_client'
}

admin_client = AdminClient(admin_config)

def kafka_create_topic_main():

    topic_name = 'reddit_topic'

    existing_topics = admin_client.list_topics().topics
    if topic_name in existing_topics:
        return "Exists"
    
    # Create a new topic
    new_topic = NewTopic(topic_name, num_partitions=1, replication_factor=3)
    admin_client.create_topics([new_topic])
    return "Created"


def get_reddit_data(client_id, client_secret, user_agent):
    # Create a Reddit instance
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    reddit_post_data = []

    subreddit = reddit.subreddit('all')
    for post in subreddit.new(limit=50):
        post_data = {
            "id": post.id,
            "title": str(post.title),
            "author": str(post.author), 
            "subreddit": str(post.subreddit),  
            "score": int(post.score),
            "url": post.url,
            "over_18": bool(post.over_18),
            "created_date": datetime.datetime.fromtimestamp(post.created_utc).strftime('%Y/%m/%d'),
            "is_video": bool(post.is_video),
            "num_comments": int(post.num_comments),           
        }
        reddit_post_data.append(post_data)  

    return reddit_post_data  


class KafkaProducerWrapper:
    def __init__(self, bootstrap_servers):
        """
        Initializes the Kafka producer with the given bootstrap servers.
        """
        self.producer_config = {
            'bootstrap.servers': bootstrap_servers
        }
        self.producer = Producer(self.producer_config)

    def produce_message(self, topic, value):
        """
        Produces a message to the specified Kafka topic with the given key and value.
        """
        self.producer.produce(topic, value=value)
        self.producer.flush()


def kafka_producer_main():
    bootstrap_servers = 'kafka1:29092,kafka2:29093,kafka3:29094'
    kafka_producer = KafkaProducerWrapper(bootstrap_servers)

    topic = "reddit_topic"
    
    reddit_data = get_reddit_data(client_id, client_secret, user_agent)
    

    start_time = time.time()

    try:
            reddit_data = get_reddit_data(client_id, client_secret, user_agent)
            for post in reddit_data:
                # Serialize each post to JSON and encode it to bytes
                value_bytes = json.dumps(post).encode('utf-8')  # Convert dict to JSON string and then to bytes
                kafka_producer.produce_message(topic, value_bytes)
                logger.info(f"Produced message for post ID : {post['id']}")

                elapsed_time = time.time() - start_time
                if elapsed_time >= 10:  # Stop after 20 seconds
                    break
                
            time.sleep(5) 
            print("Waiting for 5 seconds...")
    except KeyboardInterrupt:
        logger.info("Received KeyboardInterrupt. Stopping producer.")
    finally:
        kafka_producer.producer.flush()
        logger.info("Producer flushed.")


if __name__ == "__main__":
    result = kafka_create_topic_main()
    logger.info(result)
    kafka_producer_main()











