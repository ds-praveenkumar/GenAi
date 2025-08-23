import { Inter } from "next/font/google";
import "./globals.css";
import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";
import ThemeRegistry from './theme-provider';

const inter = Inter({ subsets: ["latin"] });
const theme = createTheme();

export const metadata = {
  title: "Next.js Chatbot with MUI",
  description: "AI Chatbot built with Next.js and Material UI",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <ThemeRegistry>{children}</ThemeRegistry>
      </body>
    </html>
  );
}
