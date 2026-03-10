export interface ChatSource {
  content: string;
  score?: number;
  filename?: string;
  file_path?: string;
}

export interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp?: string;
  sources?: ChatSource[];
}

export interface ChatResponse {
  response: string;
  session_id: string;
  sources?: ChatSource[];
}

export interface ChatHistoryResponse {
  session_id: string;
  messages: Message[];
}
