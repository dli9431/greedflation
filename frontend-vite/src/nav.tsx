import React from 'react';
import { AppBar, Toolbar, IconButton, Typography, Drawer, List, ListItem, ListItemText, ListItemIcon, Divider, useTheme } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';
import styled from '@mui/material/styles/styled';

const drawerWidth = 240;

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  [theme.breakpoints.up('md')]: {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: drawerWidth,
  },
}));

const StyledMenuButton = styled(IconButton)(({ theme }) => ({
  marginRight: theme.spacing(2),
  [theme.breakpoints.up('md')]: {
    display: 'none',
  },
}));

const StyledDrawer = styled(Drawer)(({ theme }) => ({
  [theme.breakpoints.up('md')]: {
    width: drawerWidth,
    flexShrink: 0,
  },
}));

const StyledDrawerPaper = styled(Drawer)(({ theme }) => ({
  width: drawerWidth,
}));

const StyledToolbar = styled(Toolbar)(({ theme }) => ({
  flexGrow: 1,
}));

const ResponsiveNavBar: React.FC = () => {
  const theme = useTheme();
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
    <div>
      <div className="toolbar" />
      <Divider />
      <List>
        <ListItem button key="Inbox">
          <ListItemIcon>
            <InboxIcon />
          </ListItemIcon>
          <ListItemText primary="Inbox" />
        </ListItem>
        <ListItem button key="Mail">
          <ListItemIcon>
            <MailIcon />
          </ListItemIcon>
          <ListItemText primary="Mail" />
        </ListItem>
      </List>
    </div>
  );

  return (
    <div>
      <StyledAppBar position="fixed">
        <StyledToolbar>
          <StyledMenuButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
          >
            <MenuIcon />
          </StyledMenuButton>
          <Typography variant="h6" noWrap>
            Responsive Nav Bar
          </Typography>
        </StyledToolbar>
      </StyledAppBar>
      <StyledDrawer
        variant="temporary"
        anchor={theme.direction === 'rtl' ? 'right' : 'left'}
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile.
        }}
      >
        <StyledDrawerPaper>
          {drawer}
        </StyledDrawerPaper>
      </StyledDrawer>
    </div>
  );
};

export default ResponsiveNavBar;