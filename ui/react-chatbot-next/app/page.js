'use client'; // Important: this makes the page a Client Component
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';

import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Container, Box, Typography, Card, CardContent, Button, TextField } from '@mui/material';
import { motion } from 'framer-motion';

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
  const [audioSrc, setAudioSrc] = useState(null);
  const [currentPlaying, setCurrentPlaying] = useState(null);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { role: 'user', text: input };
    setMessages([...messages, userMessage]);
    setInput('');

    try {
      const startTime = Date.now();
      // call chat API
      const res = await fetch("http://localhost:8080/api/v1/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: input }),
      });
      const data = await res.json();
      const endTime = Date.now();
      const completionTime = ((endTime - startTime) / 1000).toFixed(2);

      setMessages((prev) => [
        ...prev,
        { role: 'bot', text: data.response || 'Error occurred', time: completionTime }
      ]);
    } catch (err) {
      setMessages((prev) => [...prev, { role: 'bot', text: 'Error occurred' }]);
      console.error("Error:", err);
    }
  };

  const toggleAudio = async (msg, idx) => {
    if (currentPlaying === idx) {
      setAudioSrc(null);
      setCurrentPlaying(null);
      return;
    }

    try {
      const soundRes = await fetch("http://localhost:8080/api/v1/speak", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: msg.text }),
      });
      const soundData = await soundRes.json();

      if (soundData.audio_base64) {
        const audioBlob = base64ToBlob(soundData.audio_base64, soundData.mime_type);
        const audioUrl = URL.createObjectURL(audioBlob);
        setAudioSrc(audioUrl);
        setCurrentPlaying(idx);
      }
    } catch (err) {
      console.error("Audio error:", err);
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom textAlign="center">
        Chatbot with Sound
      </Typography>

      <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
        {messages.map((msg, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <Card
              sx={{
                alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
                backgroundColor: msg.role === "user" ? "#1976d2" : "#e0e0e0",
                color: msg.role === "user" ? "#fff" : "#000",
                maxWidth: "80%",
                borderRadius: 2,
              }}
            >
              <CardContent>
                <Box sx={{ maxHeight: 200, overflow: "auto" }}>
                  <ReactMarkdown>{msg.text}</ReactMarkdown>
                </Box>
                {msg.role === "bot" && (
                  <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mt: 1 }}>
                    <Button
                      size="small"
                      onClick={() => toggleAudio(msg, idx)}
                    >
                      {currentPlaying === idx ? '⏸ Pause' : '🔊 Play'}
                    </Button>
                    {msg.time && (
                      <Typography variant="caption" sx={{ color: "text.secondary" }}>
                        {msg.time}s
                      </Typography>
                    )}
                  </Box>
                )}
              </CardContent>
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

      {audioSrc && (
        <audio
          src={audioSrc}
          autoPlay
          onEnded={() => {
            setAudioSrc(null);
            setCurrentPlaying(null);
          }}
          style={{ marginTop: "16px", width: "100%" }}
        />
      )}
    </Container>
  );
}
