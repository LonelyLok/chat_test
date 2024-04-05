import unittest

from cassandra_client import CassandraClient  # Assume this is your Cassandra client class

class TestCassandraClient(unittest.TestCase):
    def test_connection(self):
        """Test that the Cassandra client can connect successfully."""
        client = CassandraClient()
        self.assertIsNotNone(client.session)  # Assuming your client has a 'session' attribute
        # Optionally, execute a simple query to ensure the connection is working
        result = client.execute_query("SELECT now() FROM system.local;")
        self.assertIsNotNone(result)
        client.close()  # Clean up after the test

if __name__ == '__main__':
    unittest.main()