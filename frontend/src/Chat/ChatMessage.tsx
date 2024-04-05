import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import {
  Box,
  FormControl,
  Select,
  MenuItem,
  SelectChangeEvent,
} from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';

type Message = { id: number; text: string; sender: 'user' | 'bot' };

const models = [
  'models/gemini-1.5-pro-latest',
  'models/gemini-1.0-ultra-latest',
];

const ChatMessage = ({ activeSessionId, userId }: { activeSessionId: string; userId: string }) => {
  const [existingMessages, setExistingMessages] = useState<Message[]>([]);

  const [selectModel, setSelectModel] = useState<string | null>(null);

  useEffect(() => {
    const getSessionModel = async () => {
      try {
        const response = await fetch(
          `http://localhost:5000/get_user_session?user_id=${userId}&session_id=${activeSessionId}`
        );
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const { data } = await response.json();
        setSelectModel(data.model);
      } catch (error) {
        console.error('Fetch model error:', error);
      }
    }
    const getChatHistory = async () => {
      try {
        const response = await fetch(
          `http://localhost:5000/chat_history?session_id=${activeSessionId}`
        );
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const {
          data,
        }: {
          data: {
            id: string;
            session_id: string;
            message: string;
            is_bot: boolean;
            timestamp: Date;
          }[];
        } = await response.json();
        data.sort(
          (a, b) =>
            new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
        );
        setExistingMessages(
          data.map((message, index: number) => ({
            id: index,
            text: message.message,
            sender: message.is_bot ? 'bot' : ('user' as const),
          }))
        );
      } catch (error) {
        console.error('Fetch messages error:', error);
      }
    };

    const fetchAll = async () => {
      await Promise.all([getSessionModel(),getChatHistory()])
    }
    if (activeSessionId !== null) {
      fetchAll()
    }
  }, [activeSessionId, userId]);

  const [messages, setMessages] = useState(existingMessages);
  const [newMessage, setNewMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleSendMessage = async () => {
    if (!newMessage.trim()) return;

    const nextId = messages.length;
    const userMessage = {
      id: nextId,
      text: newMessage,
      sender: 'user' as const,
    };
    setMessages([...messages, userMessage]);
    setNewMessage('');

    const botMessageId = messages.length + 1;
    let ongoingMessage = '';
    try {
      const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: newMessage,
          session_id: activeSessionId,
          model: selectModel,
        }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      if (!response.body) {
        throw new Error('Response body is missing');
      }
      // const data = await response.json();
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      const readStream = async () => {
        const { done, value } = await reader.read();
        if (done) {
          console.log('Stream finished.');
          return;
        }

        // Assuming each chunk is a complete JSON object
        const chunk = decoder.decode(value, { stream: true });
        const { response } = JSON.parse(chunk);
        ongoingMessage += response;
        setMessages((prevMessages) => {
          const existingMessages = prevMessages.filter(
            (message) => message.id !== botMessageId
          );
          const updatedBotMessage = {
            id: botMessageId,
            text: ongoingMessage,
            sender: 'bot' as const,
          };
          return [...existingMessages, updatedBotMessage];
        });

        // Read the next chunk
        readStream();
      };
      await readStream();
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setNewMessage(event.target.value);
  };

  const handleModelChange = async (event: SelectChangeEvent<string>) => {
    try{
      const response = await fetch('http://localhost:5000/update_user_session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          session_id: activeSessionId,
          model: event.target.value,
        }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    }catch(error){
      console.error('Failed to change model:', error);
    }
    setSelectModel(event.target.value as string);
  };

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  useEffect(() => {
    setMessages(existingMessages);
  }, [existingMessages]);

  const markdownComponents = {
    // Apply background styling for any code element
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    code({ className, children, ...props }: any) {
      const match = /language-(\w+)/.exec(className || '');
      // Common style for both inline and block code
      const codeStyle = {
        backgroundColor: '#2d2d2d', // Dark background
        color: '#f8f8f2', // Light text
        padding: '0 0',
        fontFamily: 'monospace', // Ensures code font
      };

      // Render block code with additional pre tag styling
      return match ? (
        <pre style={{ ...codeStyle, padding: '10px', overflowX: 'auto' }}>
          <code style={codeStyle} {...props}>
            {children}
          </code>
        </pre>
      ) : (
        <code style={codeStyle} {...props}>
          {children}
        </code>
      );
    },
  };

  const modelSelectTheme = createTheme({
    components: {
      MuiSelect: {
        styleOverrides: {
          select: {
            color: 'white',
          },
          icon: {
            color: 'white',
          },
          iconOpen: {
            color: 'white',
          },
        },
      },
    },
  });

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center', // Center children vertically in the container
        textAlign: 'center',
        padding: '10px',
        margin: 'auto',
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <p
          style={{
            color: '#fff',
          }}
        >
          Chat : {activeSessionId}
        </p>
        <Box sx={{ paddingLeft: '2rem' }}>
          <ThemeProvider theme={modelSelectTheme}>
            <FormControl>
              <Select
                labelId='demo-simple-select-label'
                id='demo-simple-select'
                label='Select an option'
                value={selectModel}
                onChange={(e) => handleModelChange(e as SelectChangeEvent<string>)}
              >
                {models.map((m) => (
                  <MenuItem key={m} value={m}>
                    {m}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </ThemeProvider>
        </Box>
      </div>
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          width: '1000px', // Fixed width of the message box
          height: '700px', // Maximum height of the message box
          overflowY: 'auto', // Scroll overflow content
          border: '1px solid #ddd',
          padding: '5px',
          backgroundColor: '#636363',
          margin: 'auto',
        }}
      >
        {messages.map((message) => (
          <div key={message.id}>
            <div
              style={{
                textAlign: 'left',
                color: message.sender === 'bot' ? '#fff' : '#ADD8E6',
              }}
            >
              <strong>{message.sender === 'bot' ? 'Bot:' : 'Me:'}</strong>{' '}
              <ReactMarkdown components={markdownComponents}>
                {message.text}
              </ReactMarkdown>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div
        style={{
          display: 'flex',
          width: '800px',
          padding: '10px',
          borderTop: '1px solid #ddd',
          margin: 'auto',
        }}
      >
        <textarea
          value={newMessage}
          onChange={handleInputChange}
          onKeyUp={(event) =>
            event.key === 'Enter' && !event.shiftKey
              ? handleSendMessage()
              : null
          }
          style={{
            padding: '10px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            width: 'calc(100% - 100px)',
            height: '80px', // Set an initial height
            overflowY: 'auto', // Allow vertical scrolling
            resize: 'none', // Optional: Prevent manual resizing
          }}
        />
        <button
          onClick={handleSendMessage}
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export { ChatMessage };
