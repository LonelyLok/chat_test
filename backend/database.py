from cassandra_client import CassandraClient

# Initialize a global variable for the Cassandra client, set to None initially
_cassandra_client = None

def get_session():
    global _cassandra_client
    # Initialize the CassandraClient if it hasn't been already
    if _cassandra_client is None:
        _cassandra_client = CassandraClient()
    return _cassandra_client

def close_session():
    global _cassandra_client
    # Close the client if it exists
    if _cassandra_client:
        _cassandra_client.close()
        _cassandra_client = None 