import { getApiBase } from '../constants';
import type { ChatResponse, ChatHistoryResponse } from '../types/chat';

export async function sendMessage(
  sessionId: string | null,
  message: string
): Promise<ChatResponse> {
  const base = getApiBase();
  const res = await fetch(`${base}/chat/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, message }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || `HTTP ${res.status}`);
  }

  return res.json();
}

export async function getHistory(sessionId: string): Promise<ChatHistoryResponse> {
  const base = getApiBase();
  const res = await fetch(`${base}/chat/history/${sessionId}`);

  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }

  return res.json();
}
