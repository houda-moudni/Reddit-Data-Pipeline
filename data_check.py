from cassandra.cluster import Cluster
import logging
from cassandra.policies import DCAwareRoundRobinPolicy

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CassandraConnector:
    def __init__(self, contact_points):
        self.cluster = Cluster(contact_points, load_balancing_policy=DCAwareRoundRobinPolicy())
        self.session = self.cluster.connect()


    def select_all_data(self):
        
        query = "SELECT * FROM reddit_posts_namespace.reddit_table" 
        result = self.session.execute(query)
        if result == None:
            print("No data found")
        else:
            for row in result: 
                print(f"ID: {row.id}, Author: {row.author}, Subreddit: {row.subreddit}, Title: {row.title}, URL: {row.url}, Score: {row.score}, Created UTC: {row.created_utc}, Is Video: {row.is_video}")

    def delete_data(self, id):
        query = 'SELECT * FROM reddit_posts_namespace.reddit_table where id = %s'
        result = self.session.execute(query,(id,))
        if result == None:
            print("No data with this ID {{id}} found")
        else:
            query = 'DELETE FROM reddit_posts_namespace.reddit_table WHERE "id" = %s'
            self.session.execute(query, (id,))

    def count_data(self):
        query = 'SELECT COUNT(*) FROM reddit_posts_namespace.reddit_table;'
        result = self.session.execute(query)
        if result:
            row = result.one()  # Get the first row
            print(f"Count: {row[0]}")
        else:
            print("No data found")

    def close(self):
        self.cluster.shutdown()


def check_cassandra_main():
    cassandra_connector = CassandraConnector(['cassandra'])
    print("Selecting all data ...")
    cassandra_connector.select_all_data()
    print("Counting data ...")
    cassandra_connector.count_data()
    print("Shutting down ...")
    cassandra_connector.close()


if __name__ == '__main__':
    check_cassandra_main()
