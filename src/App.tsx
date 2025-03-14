import { Outlet } from "@tanstack/react-router"
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Switch } from "@mui/material";
import { useState, useMemo } from "react";


function App() {
  const [mode, setMode] = useState<"light" | "dark">("dark");

  const theme = useMemo(() => 
    createTheme({
      palette: {
        mode: mode,
      },
    }), [mode]
  );

  const handleThemeChange = () => {
    setMode((prevMode) => prevMode === "dark" ? "light": "dark");
  }

  return (
    <>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <nav>
           <Switch onChange={handleThemeChange} checked={mode === "dark"}/>
        </nav>
        <Outlet />
      </ThemeProvider>
    </>
  )
}
export default App
