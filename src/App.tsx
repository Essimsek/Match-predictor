import { Outlet } from "@tanstack/react-router"
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { useState, useMemo } from "react";
import Navbar, { Seperator } from "./components/Navbar";


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
        <Navbar onThemeChange={handleThemeChange} mode={mode}/>
        <Seperator />
        <Outlet />
      </ThemeProvider>
    </>
  )
}
export default App
