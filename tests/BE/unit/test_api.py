def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'healthy', 'message': 'Janus API is running'}

def test_kb_upload_no_file(client):
    """Test knowledgebase upload endpoint with missing file"""
    response = client.post('/api/v1/knowledgebase/upload')
    assert response.status_code == 400
    assert response.json == {"error": "No file part"}
