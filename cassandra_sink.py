from confluent_kafka import Consumer, KafkaError, KafkaException, TopicPartition
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy
import time
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

class CassandraConnector:
    def __init__(self, contact_points):
        self.cluster = Cluster(contact_points, load_balancing_policy=DCAwareRoundRobinPolicy())
        self.session = self.cluster.connect()
        self.create_keyspace()
        self.create_table()

    def create_keyspace(self):
        self.session.execute("""
            CREATE KEYSPACE IF NOT EXISTS reddit_posts_namespace
            WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1}
        """)

    def create_table(self):
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS reddit_posts_namespace.reddit_table (
                id text PRIMARY KEY,
                title text,
                author text,
                subreddit text,
                score int,
                url text,
                over_18 boolean,
                created_utc text,
                is_video boolean,
                num_comments int
                        )"""
                )

    def insert_data(self, id, title, author, subreddit, score, url, over_18, created_utc, is_video, num_comments):
        
        # Use a parameterized query with Cassandra's prepared statements
        insert_query = """
            INSERT INTO reddit_posts_namespace.reddit_table 
            ("id", "title", "author", "subreddit", "score", "url", "over_18", "created_utc", "is_video", "num_comments") 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Execute the query with parameters to ensure proper formatting and escaping
        self.session.execute(insert_query, (id, title, author, subreddit, score, url, over_18, created_utc, is_video, num_comments))

    def shutdown(self):
        self.cluster.shutdown()



def fetch_and_insert_messages(kafka_config, cassandra_connector, topic, run_duration_secs):
    time.sleep(10)
    
    consumer = Consumer(kafka_config)
    consumer.subscribe([topic])

    start_time = time.time()
    try:
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time >= run_duration_secs:
                break
            
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print('Reached end of partition')
                else:
                    logger.error('Error: {}'.format(msg.error()))
            else:
                
                record = json.loads(msg.value().decode('utf-8'))

                query = 'SELECT * FROM reddit_posts_namespace.reddit_table WHERE id = %s'
                
                existing_id = cassandra_connector.session.execute(query, (record['id'],)).one()

                if existing_id:
                    logger.warning(f'Skipped existing id: id={existing_id}')
                else:

                    cassandra_connector.insert_data(record['id'], record['title'], record['author'], record['subreddit'],
                                                        int(record['score']), record['url'], bool(record['over_18']),
                                                        str(record['created_utc']), bool(record['is_video']),
                                                        int(record.get('num_comments', 0)))



                logger.info(f"Received and inserted: id={record['id']}")
                
                           
    except KeyboardInterrupt:
        print("Received KeyboardInterrupt. Closing consumer.")
    finally:
        consumer.close()



def kafka_consumer_cassandra_main():
    cassandra_connector = CassandraConnector(['cassandra'])
    print("Creating KEYSPACE reddit_posts_namespace ...")
    cassandra_connector.create_keyspace()
    print("Creating TABLE reddit_table ...")
    cassandra_connector.create_table()

    kafka_config = {
        'bootstrap.servers': 'kafka1:29092, kafka2:29093,kafka3:29094',
        # 'bootstrap.servers': 'localhost:9092, localhost:9093, localhost:9094',
        'group.id': 'cassandra_consumer_group',
        'auto.offset.reset': 'earliest'
    }

    topic = 'reddit_topic'
    run_duration_secs = 30

    
    print("Fetching and inserting messages ...")
    fetch_and_insert_messages(kafka_config, cassandra_connector, topic, run_duration_secs)
    print("Shutting down ...")
    cassandra_connector.shutdown()



if __name__ == '__main__':
    kafka_consumer_cassandra_main()