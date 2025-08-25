'use client';
import React from 'react';

export default function ChatWindow({ messages }) {
  return (
    <div className="h-96 overflow-y-auto border rounded p-4 mb-4 bg-gray-50">
      {messages.map((msg, i) => (
        <div key={i} className="mb-2">
          <strong>{msg.sender}: </strong>
          <span>{msg.text}</span>
        </div>
      ))}
    </div>
  );
}
