import { getApiBase } from "../constants";
import type {
  KnowledgebaseDocumentsResponse,
  TrainKnowledgebaseRequest,
  TrainKnowledgebaseResponse,
  UploadDocumentResponse,
} from "../types/knowledgebase";

const base = () => getApiBase();

export async function listDocuments(): Promise<KnowledgebaseDocumentsResponse> {
  const res = await fetch(`${base()}/knowledgebase/documents`);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function uploadDocument(
  file: File,
): Promise<UploadDocumentResponse> {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${base()}/knowledgebase/upload`, {
    method: "POST",
    body: formData,
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || `HTTP ${res.status}`);
  }
  return data;
}

export async function trainKnowledgebase(
  config: TrainKnowledgebaseRequest = {},
): Promise<TrainKnowledgebaseResponse> {
  const res = await fetch(`${base()}/knowledgebase/train`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      vectorDb: config.vectorDb ?? "pinecone",
      embeddingModel: config.embeddingModel ?? "text-embedding-3-small",
      namespace: config.namespace,
    }),
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || `HTTP ${res.status}`);
  }
  return data;
}
