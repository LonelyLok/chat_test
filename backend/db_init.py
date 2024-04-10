import random
import time
from cassandra_client import CassandraClient

def db_init():
    connected = False
    retry_count = 0
    max_retries = 5
    base_delay = 2  # seconds
    max_delay = 60  # seconds

    while not connected and retry_count < max_retries:
        try:
            client = CassandraClient()
            connected = True
            print("Connected to Cassandra.")
        except Exception as e:
            retry_count += 1
            delay = min(base_delay * (2 ** (retry_count - 1)), max_delay)
            jitter = random.uniform(0, delay * 0.1)  # Add jitter to the delay
            total_delay = delay + jitter
            print(f"Error connecting to Cassandra: {str(e)}")
            print(f"Cassandra is not ready. Retrying in {total_delay:.2f} seconds... (Attempt {retry_count}/{max_retries})")
            time.sleep(total_delay)

    if not connected:
        print("Failed to connect to Cassandra after multiple retries. Exiting.")
        return
    
    chat_keyspace_results = client.execute_query("SELECT keyspace_name FROM system_schema.keyspaces WHERE keyspace_name = 'chat'")

    if chat_keyspace_results != None and len(list(chat_keyspace_results)) > 0:
        print("Keyspace already exists. Skipping creation.")
        client.close()
        return
    
    create_keyspace_query = f"""
        CREATE KEYSPACE IF NOT EXISTS {"chat"} 
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1 }};
        """
    client.execute_query(create_keyspace_query)

    print("Keyspace created.")

    create_chat_history_table_query = """
        CREATE TABLE IF NOT EXISTS chat.chat_history (
            id UUID,
            session_id UUID,
            message TEXT,
            is_bot BOOLEAN,
            timestamp TIMESTAMP,
            PRIMARY KEY (session_id, timestamp, id)
        ) WITH CLUSTERING ORDER BY (timestamp ASC);
        """
    
    client.execute_query(create_chat_history_table_query)

    print("Chat history table created.")

    create_user_sessions_table_query = """
        CREATE TABLE chat.user_sessions (
        user_id UUID,
        session_id UUID,
        model TEXT,
        created_at TIMESTAMP,
        PRIMARY KEY (user_id, session_id)
        ) WITH CLUSTERING ORDER BY (session_id ASC);
        """
    client.execute_query(create_user_sessions_table_query)

    print("User sessions table created.")
    print("Database initialized.")
    client.close()

if __name__ == '__main__':
    db_init()