import { useState, useCallback, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { sendMessage as apiSendMessage, getHistory } from '@janus/shared';
import type { Message } from '@janus/shared';

const SESSION_KEY = 'janus_session_id';

function generateSessionId(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

export function useChat() {
  const [sessionId, setSessionId] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const saved = await AsyncStorage.getItem(SESSION_KEY);
        if (saved) {
          setSessionId(saved);
          const history = await getHistory(saved);
          if (history?.messages?.length) {
            setMessages(history.messages);
          }
        } else {
          const newId = generateSessionId();
          setSessionId(newId);
          await AsyncStorage.setItem(SESSION_KEY, newId);
        }
      } catch {
        const newId = generateSessionId();
        setSessionId(newId);
        await AsyncStorage.setItem(SESSION_KEY, newId);
      } finally {
        setIsInitialized(true);
      }
    })();
  }, []);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    const userMsg: Message = {
      role: 'user',
      content: content.trim(),
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const res = await apiSendMessage(sessionId || null, content.trim());
      setSessionId(res.session_id);
      await AsyncStorage.setItem(SESSION_KEY, res.session_id);

      const assistantMsg: Message = {
        role: 'assistant',
        content: res.response,
        timestamp: new Date().toISOString(),
      };
      if (res.sources?.length) {
        assistantMsg.sources = res.sources;
      }
      setMessages((prev) => [...prev, assistantMsg]);
    } catch {
      const errorMsg: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error communicating with the server.',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId]);

  return {
    sessionId,
    messages,
    isLoading,
    isInitialized,
    sendMessage,
  };
}
