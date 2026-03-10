def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy", "message": "Janus API is running"}


def test_kb_upload_no_file(client):
    """Test knowledgebase upload endpoint with missing file"""
    response = client.post("/api/v1/knowledgebase/upload")
    assert response.status_code == 400
    assert response.json == {"error": "No file part"}


def test_kb_upload_with_file(client):
    """Test knowledgebase upload with a valid file"""
    from io import BytesIO

    data = {"file": (BytesIO(b"test content"), "test.txt")}
    response = client.post(
        "/api/v1/knowledgebase/upload",
        data=data,
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    data = response.json
    assert "message" in data
    assert "id" in data


def test_kb_documents_list(client):
    """Test knowledgebase documents list returns expected structure"""
    response = client.get("/api/v1/knowledgebase/documents")
    assert response.status_code == 200
    data = response.json
    assert "documents" in data
    assert isinstance(data["documents"], list)


def test_kb_train_returns_structure(client):
    """Test knowledgebase train returns message and config"""
    response = client.post(
        "/api/v1/knowledgebase/train",
        json={"vectorDb": "pinecone", "embeddingModel": "text-embedding-3-small"},
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.json
    assert "message" in data
    assert "config_used" in data
    assert "processed" in data
    assert "failed" in data


def test_chat_returns_sources_when_available(client, monkeypatch):
    """Test chat response includes sources when retrieval returns them"""
    from unittest.mock import MagicMock

    from langchain_core.messages import AIMessage

    def mock_invoke(state):
        return {
            "messages": state["messages"]
            + [AIMessage(content="Based on the docs, here is the answer.")],
            "retrieval_sources": [
                {"content": "Relevant chunk", "score": 0.9, "metadata": {"filename": "doc.pdf"}},
            ],
        }

    mock_graph = MagicMock()
    mock_graph.invoke = mock_invoke

    from services import chat_service

    monkeypatch.setattr(chat_service, "janus_graph", mock_graph)

    response = client.post(
        "/api/v1/chat/",
        json={"message": "What does the document say?"},
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.json
    assert "response" in data
    assert "session_id" in data
    assert "sources" in data
    assert len(data["sources"]) == 1
    assert data["sources"][0]["filename"] == "doc.pdf"
