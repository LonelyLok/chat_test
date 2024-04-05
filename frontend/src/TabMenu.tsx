import React, { useState } from 'react';
import { IconButton, Menu, MenuItem } from '@mui/material';
import MoreVertIcon from '@mui/icons-material/MoreVert';

interface TabMenuProps {
  sessionId: string;
  userId: string;
  handleUpdateSessionsFromDelete: (sessionId: string) => void;
  setActiveSessionId: (sessionId: string | null) => void;
}

const TabMenu: React.FC<TabMenuProps> = ({ sessionId, userId, handleUpdateSessionsFromDelete, setActiveSessionId }) => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleDelete = async () => {
    try {
      const response = await fetch('http://localhost:5000/delete_session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          session_id: sessionId,
        }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      // Add any other logic you need to update the UI after deleting the session
      setAnchorEl(null);
      handleUpdateSessionsFromDelete(sessionId);
      setActiveSessionId(null);
    } catch (error) {
      console.error('delete session error:', error);
    }
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <div>
      <IconButton size='small' onClick={handleClick}>
        <MoreVertIcon fontSize='small' sx={{ color: 'white' }} />
      </IconButton>
      <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleClose}>
        <MenuItem onClick={handleDelete}>Delete</MenuItem>
      </Menu>
    </div>
  );
};

export { TabMenu };
