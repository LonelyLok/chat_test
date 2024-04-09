# Chat test

A simple chat bot web application that allows users to interact with an AI-powered conversational agent.

## Features

- Real-time chat interface for seamless communication with the chat bot
- Integration with a google gemini for intelligent and context-aware conversations
- User-friendly and intuitive interface for easy navigation and interaction

## Technologies Used

- Fronted: Typescript, React.js
- Backend: Python, Flask
- Database: Cassandra
- AI: Google Gemini


## Getting Started

To use the chatbot, you will need a Google Gemini API key. Follow these steps to set up the necessary environment variables:

1. Create a .env file inside the backend folder
2. Add the following line to the .env file:
```
GEMINI_API_KEY=<your_api_key>
CASSANDRA_DB_HOST=127.0.0.1
```

There are three services in the docker-compose.yml file that you will need to start:
- cassandra: A container for running the Cassandra database
- backend: A container for running the Flask server
- frontend: A container for running the React.js frontend

Run `docker-compose up` to start all the services.

or

You can only run docker-compose up cassandra to start only the cassandra service. Then, you can run `python3 app.py` inside backend folder to start the Flask server and `npm run dev` inside frontend folder to start the React.js frontend.