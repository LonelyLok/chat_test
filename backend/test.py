from cassandra_client import CassandraClient
import datetime

create_keyspace_query = f"""
        CREATE KEYSPACE IF NOT EXISTS {"chat"} 
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1 }};
        """

create_table_query = """
        CREATE TABLE IF NOT EXISTS chat.chat_history (
            id UUID,
            session_id UUID,
            message TEXT,
            is_bot BOOLEAN,
            timestamp TIMESTAMP,
            PRIMARY KEY (session_id, timestamp, id)
        ) WITH CLUSTERING ORDER BY (timestamp ASC);
        """

create_table_2_query = """
        CREATE TABLE chat.user_sessions (
        user_id UUID,
        session_id UUID,
        created_at TIMESTAMP,
        PRIMARY KEY (user_id, session_id)
        ) WITH CLUSTERING ORDER BY (session_id ASC);
        """

drop_table_query = """
        DROP TABLE IF EXISTS chat.user_sessions;
        """

add_model_column_query = """
        ALTER TABLE chat.user_sessions ADD model TEXT;
        """

if __name__ == '__main__':
    client = CassandraClient()  # Initialize the client with your Cassandra cluster's configuration
    client.execute_query(
        add_model_column_query
    )
    print("chat_history table created.")
    client.close() 