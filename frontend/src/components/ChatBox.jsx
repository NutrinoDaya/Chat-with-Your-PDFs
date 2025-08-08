import React, { useState } from "react";
import axios from "axios";
import Message from "./Message";

export default function ChatBox({ docId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    setError(null);

    try {
      const res = await axios.post("/api/chat/", {
        question: input,
        document_id: docId
      });
      const botMsg = { sender: "bot", text: res.data.answer };
      setMessages((prev) => [...prev, botMsg]);
      setInput("");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to get answer");
    } finally {
      setLoading(false);
    }
  };

  const onKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chatbox-container">
      <div className="messages">
        {messages.length === 0 && <p>Ask something about your PDF!</p>}
        {messages.map((msg, idx) => (
          <Message key={idx} sender={msg.sender} text={msg.text} />
        ))}
      </div>
      {error && <p className="error-text">{error}</p>}
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={onKeyDown}
        placeholder="Type your question..."
        rows={3}
        disabled={loading}
      />
      <button onClick={sendMessage} disabled={loading || !input.trim()}>
        {loading ? "Thinking..." : "Send"}
      </button>
    </div>
  );
}
