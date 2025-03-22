// components/IconSwitch.tsx
import { styled } from '@mui/material/styles';
import Switch from '@mui/material/Switch';

const IconSwitch = styled(Switch)(({ theme }) => ({
  width: 60,
  height: 34,
  padding: 7,
  '& .MuiSwitch-switchBase': {
    padding: 0,
    margin: 1,
    transitionDuration: '300ms',
    '&.Mui-checked': {
      transform: 'translateX(26px)',
      color: '#fff',
      '& .MuiSwitch-thumb:before': {
        content: '"\\1F319"', // Crescent moon (Unicode)
      },
      '& + .MuiSwitch-track': {
        backgroundColor: theme.palette.mode === 'dark' ? '#8796A5' : '#aab4be',
        opacity: 1,
      },
    },
  },
  '& .MuiSwitch-thumb': {
    backgroundColor: theme.palette.mode === 'dark' ? '#003892' : '#001e3c',
    width: 32,
    height: 32,
    '&:before': {
      content: '"\\2600"', // Sun (Unicode)
      position: 'absolute',
      width: '100%',
      height: '100%',
      left: 0,
      top: 0,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: 18,
    },
  },
  '& .MuiSwitch-track': {
    borderRadius: 20 / 2,
    opacity: 1,
    backgroundColor: theme.palette.mode === 'dark' ? '#8796A5' : '#aab4be',
  },
}));

export default IconSwitch;