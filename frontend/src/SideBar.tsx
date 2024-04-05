import React from 'react';
import { Tabs, Tab, Box, TabProps } from '@mui/material';
import { TabMenu } from './TabMenu';
import type { Sessions } from './MainPage';

interface SideBarProps {
  setActiveSessionId: (sessionId: string | null) => void;
  handleUpdateSessionsFromDelete: (sessionId: string) => void;
  sessions: Sessions;
  activeSessionId: string | null;
  userId: string;
}

const SideBar: React.FC<SideBarProps> = ({
  setActiveSessionId,
  handleUpdateSessionsFromDelete,
  sessions,
  activeSessionId,
  userId,
}) => {
  const handleChange = (event: React.SyntheticEvent, newValue: string) => {
    setActiveSessionId(newValue);
  };

  const tabsStyle = {
    '& .MuiTabs-indicator': {
      backgroundColor: '#999999', // Change the color of the selected tab indicator
    },
    '& .Mui-selected': {
      color: '#999999', // Change the color of the selected tab label
      backgroundColor: '#999999', // Change the background color of the selected tab
    },
    '& .MuiTab-root': {
      color: 'white', // Change the color of unselected tab labels
      '& .Mui-selected': {
        color: '#999999', // Change the color of the selected tab label
        backgroundColor: '#999999', // Change the background color of the selected tab
      },
    },
  };

  const CustomTab = (props: TabProps, session: Sessions[number], userId: string) => {
    return (
      <Box {...props}>
        <div
          style={{
            display: 'flex', // Enable flex layout
            alignItems: 'center', // Align items vertically
            justifyContent: 'space-between', // Space between label and menu
            width: 200,
            color: 'white',
          }}
        >
          <span
            style={{
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap',
              marginRight: '10px', // Ensure some space between the label and the menu
            }}
          >
            {session.name}
          </span>
          <TabMenu sessionId={session.id} userId={userId} handleUpdateSessionsFromDelete={handleUpdateSessionsFromDelete} setActiveSessionId={setActiveSessionId} />
        </div>
      </Box>
    );
  };
  return (
    <Box sx={{ flexGrow: 1, display: 'flex', width: '200px' }}>
      <Tabs
        orientation='vertical'
        variant='scrollable'
        value={activeSessionId}
        onChange={handleChange}
        aria-label='Vertical tabs example'
        sx={{ borderRight: 1, borderColor: 'white', ...tabsStyle }}
      >
        {sessions.map((session) => (
          <Tab
            label={session.name}
            value={session.id}
            component={(props: TabProps) => CustomTab(props, session, userId)}
          ></Tab>
        ))}
      </Tabs>
    </Box>
  );
};

export { SideBar };
