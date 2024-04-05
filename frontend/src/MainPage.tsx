import React, { useState, useEffect } from 'react';
import { ChatApp } from './Chat/ChatApp';
import { SideBar } from './SideBar';
import { v4 as uuidv4 } from 'uuid';

const fakeUserId = 'e42be349-0224-4ff0-843e-8705914a150c';

export type Sessions = { id: string; name: string }[];

const MainPage = () => {
  const [sessions, setSessions] = useState<Sessions>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);

  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const response = await fetch(
          `http://localhost:5000/get_user_sessions?user_id=${fakeUserId}`,
          {
            cache: 'no-store', // This tells the browser not to store any part of the response in the cache.
          }
        );
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const {
          data,
        }: {
          data: { user_id: string; session_id: string; created_at: Date; model: string; }[];
        } = await response.json();
        setSessions(
          data.map((session) => ({
            id: session.session_id,
            name: `Session ${session.session_id}`,
            model: session.model,
          }))
        );
      } catch (error) {
        console.error('Fetch sessions error:', error);
      }
    };
    fetchSessions();
  }, [fakeUserId]);

  const handleUpdateSessionsFromDelete = (sessionId: string) => {
    const updatedSessions = sessions.filter(
      (session) => session.id !== sessionId
    );
    setSessions(updatedSessions);
  };

  const handleAddSession = async () => {
    const newId = uuidv4();
    const newSession = { id: newId, name: `Session ${newId}`, model: '' };
    try {
      const response = await fetch('http://localhost:5000/create_session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: fakeUserId,
          session_id: newSession.id,
        }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const {data} = await response.json();
      console.log({data})
      newSession.model = data.model
      setSessions([...sessions, newSession]);
    } catch (error) {
      console.error('create sessions error:', error);
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center' }}>
      <div style={{ textAlign: 'center', height: '100vh', width: 200 }}>
        <button
          style={{ backgroundColor: 'purple' }}
          onClick={handleAddSession}
        >
          Add Session
        </button>
        <SideBar
          setActiveSessionId={setActiveSessionId}
          sessions={sessions}
          handleUpdateSessionsFromDelete={handleUpdateSessionsFromDelete}
          activeSessionId={activeSessionId}
          userId={fakeUserId}
        />
      </div>
      <div style={{ width: '90%' }}>
        <ChatApp activeSessionId={activeSessionId} userId={fakeUserId} />
      </div>
    </div>
  );
};

export { MainPage };
