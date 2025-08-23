'use client'; // Important: this makes the page a Client Component
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';

import React, { useState, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { Container, Box, Typography, Card, CardContent, Button, TextField, IconButton } from '@mui/material';
import { motion } from 'framer-motion';
import { PlayArrow, Pause } from '@mui/icons-material';

// Helper: Convert base64 to Blob
const base64ToBlob = (base64, mime) => {
  const byteChars = atob(base64);
  const byteNumbers = new Array(byteChars.length);
  for (let i = 0; i < byteChars.length; i++) {
    byteNumbers[i] = byteChars.charCodeAt(i);
  }
  const byteArray = new Uint8Array(byteNumbers);
  return new Blob([byteArray], { type: mime });
};

export default function Page() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [playingIndex, setPlayingIndex] = useState(null);
  const audioRef = useRef(null);

  const handlePlay = async (msg, idx) => {
    if (playingIndex === idx) {
      audioRef.current.pause();
      setPlayingIndex(null);
      return;
    }

    try {
      const soundRes = await fetch('http://localhost:8080/api/v1/speak', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: msg.text }),
      });
      const soundData = await soundRes.json();

      if (soundData.audio_base64) {
        const audioBlob = base64ToBlob(soundData.audio_base64, soundData.mime_type);
        const audioUrl = URL.createObjectURL(audioBlob);

        if (audioRef.current) {
          audioRef.current.src = audioUrl;
          audioRef.current.play();
          setPlayingIndex(idx);
        }
      }
    } catch (err) {
      console.error('Audio play error:', err);
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    setMessages([...messages, { role: 'user', text: input }]);
    setInput('');

    try {
      const res = await fetch("http://localhost:8080/api/v1/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: input }),
      });
      const data = await res.json();

      setMessages((prev) => [...prev, { role: 'bot', text: data.response || 'Error occurred' }]);
    } catch (err) {
      console.error("Error:", err);
      setMessages((prev) => [...prev, { role: 'bot', text: 'Error occurred' }]);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom textAlign="center">
        Chatbot with Sound
      </Typography>

      <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
        {messages.map((msg, idx) => (
          <motion.div key={idx} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
            <Card
              sx={{
                alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
                backgroundColor: msg.role === "user" ? "#1976d2" : "#e0e0e0",
                color: msg.role === "user" ? "#fff" : "#000",
                maxWidth: "80%",
                borderRadius: 2,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}
            >
              <CardContent sx={{ flex: 1 }}>
                <ReactMarkdown>{msg.text}</ReactMarkdown>
              </CardContent>
              {msg.role === 'bot' && (
                <IconButton onClick={() => handlePlay(msg, idx)}>
                  {playingIndex === idx ? <Pause /> : <PlayArrow />}
                </IconButton>
              )}
            </Card>
          </motion.div>
        ))}
      </Box>

      <Box sx={{ display: "flex", mt: 3, gap: 1 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <Button variant="contained" onClick={sendMessage}>
          Send
        </Button>
      </Box>

      <audio ref={audioRef} onEnded={() => setPlayingIndex(null)} />
    </Container>
  );
}
