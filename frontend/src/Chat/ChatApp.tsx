import React from 'react';
import { ChatMessage } from './ChatMessage';

interface ChatAppProps {
  activeSessionId: string | null;
  userId: string;
}

const ChatApp: React.FC<ChatAppProps> = ({ activeSessionId, userId }) => {

  return (
    <div>
      {activeSessionId !== null ? (
        <ChatMessage
          activeSessionId={activeSessionId}
          userId={userId}
        />
      ) : (
        <div>Select a session to start chatting</div>
      )}
    </div>
  );
};

export { ChatApp };
