export type DocumentStatus = "uploaded" | "processing" | "indexed" | "failed";

export interface Document {
  id: number;
  filename: string;
  status: DocumentStatus;
  storage_path?: string;
  chunk_count?: number;
  created_at: string;
  indexed_at?: string | null;
  last_error?: string | null;
}

export interface KnowledgebaseDocumentsResponse {
  documents: Document[];
}

export interface UploadDocumentResponse {
  message: string;
  id: number;
}

export interface TrainKnowledgebaseRequest {
  vectorDb?: string;
  embeddingModel?: string;
  namespace?: string;
}

export interface TrainKnowledgebaseResponse {
  message: string;
  config_used: Record<string, unknown>;
  processed?: number;
  failed?: number;
}
