from cassandra.cluster import Cluster
import os
import config

class CassandraClient:
    def __init__(self, hosts=[os.getenv('CASSANDRA_DB_HOST')], port=9042):
        self.hosts = hosts
        self.port = port
        self.session = self.connect()

    def connect(self):
        """Connect to the Cassandra cluster and establish a session with connection pooling."""
        cluster = Cluster(
            # self.hosts, 
            # port=self.port,
            Cluster(['cassandra'], port=9042),
        )
        session = cluster.connect()
        print("Connected to Cassandra with connection pooling")
        return session

    def execute_query(self, query, params=None):
        """Execute a CQL query using the established session."""
        try:
            if params is not None:
                return self.session.execute(query, params)
            else:
                return self.session.execute(query)
        except Exception as e:
            print(f"An error occurred while executing the query: {e}")
            raise

    def close(self):
        """Close the session and connection to the cluster."""
        if self.session:
            self.session.cluster.shutdown()
            self.session.shutdown()
            print("Connection to Cassandra closed")