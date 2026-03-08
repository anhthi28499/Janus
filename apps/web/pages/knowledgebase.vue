<template>
  <div class="page-container">
    <!-- Sidebar: Docs -->
    <div class="sidebar p-4">
      <h2 class="text-xl font-bold mb-4 gradient-text">Documents</h2>
      
      <div class="upload-section glass-panel p-4 rounded-lg mb-6">
        <h3 class="text-sm font-semibold mb-2">Upload File</h3>
        <input type="file" class="form-input text-sm mb-2" @change="onFileChange" >
        <button class="btn btn-primary w-full" :disabled="!selectedFile || isUploading" @click="uploadFile">
          {{ isUploading ? 'Uploading...' : 'Upload' }}
        </button>
      </div>
      
      <div class="list-section">
        <h3 class="text-sm font-semibold mb-2">Current Documents</h3>
        <div v-if="documents.length === 0" class="text-sm text-gray-400 italic">
          No documents uploaded yet.
        </div>
        <ul class="space-y-2">
          <li v-for="doc in documents" :key="doc.id" class="doc-item glass-panel p-3 rounded">
            <div class="flex items-center justify-between">
              <span class="text-sm truncate mr-2">{{ doc.filename }}</span>
              <span :class="statusClass(doc.status)">{{ doc.status }}</span>
            </div>
            <div class="text-xs text-gray-500 mt-1">{{ formatDate(doc.created_at) }}</div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content flex flex-col items-center justify-center relative">
      <div class="training-card glass-panel p-8 rounded-xl max-w-lg w-full text-center animate-fade-in">
        <div class="icon-container mx-auto mb-6">
          <svg class="w-16 h-16 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
          </svg>
        </div>
        
        <h2 class="text-2xl font-bold mb-2">Knowledge Base Core</h2>
        <p class="text-gray-400 mb-8">Process uploaded documents and update the vector database to make them searchable by Janus.</p>
        
        <button 
          class="btn btn-primary pulse-btn w-full py-3 text-lg font-semibold rounded-lg" 
          :disabled="isTraining"
          @click="startTraining"
        >
          <span v-if="!isTraining">🎯 Train VectorDB</span>
          <span v-else class="flex items-center justify-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
            </svg>
            Processing...
          </span>
        </button>
        
        <div v-if="trainResult" class="mt-4 p-3 rounded bg-green-900/30 text-green-400 text-sm border border-green-800/50">
          {{ trainResult.message }}
        </div>
      </div>
    </div>

    <!-- Sidebar: System -->
    <div class="sidebar p-4 border-l border-r-0 border-gray-800">
      <h2 class="text-xl font-bold mb-4 gradient-text">System config</h2>
      
      <div class="form-group mb-6">
        <label class="form-label">Vector Database</label>
        <select v-model="systemConfig.vectorDb" class="form-select">
          <option value="pinecone">Pinecone</option>
          <option value="chroma">ChromaDB</option>
          <option value="qdrant">Qdrant</option>
        </select>
        <div class="text-xs text-gray-500 mt-1">Currently active: {{ systemConfig.vectorDb }}</div>
      </div>
      
      <div class="form-group mb-6">
        <label class="form-label">Embedding Model</label>
        <select v-model="systemConfig.embeddingModel" class="form-select">
          <option value="text-embedding-3-small">OpenAI text-embedding-3-small</option>
          <option value="text-embedding-3-large">OpenAI text-embedding-3-large</option>
          <option value="bge-large-en-v1.5">BAAI/bge-large-en-v1.5</option>
        </select>
      </div>
      
      <div class="glass-panel p-4 rounded-lg bg-indigo-900/10 border-indigo-500/20">
        <h3 class="text-sm font-semibold text-indigo-400 mb-2">Auto-Switching</h3>
        <p class="text-xs text-gray-400">Settings are automatically applied to the next training session.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const config = useRuntimeConfig()

// State
const documents = ref([])
const selectedFile = ref(null)
const isUploading = ref(false)
const isTraining = ref(false)
const trainResult = ref(null)

const systemConfig = ref({
  vectorDb: 'pinecone',
  embeddingModel: 'text-embedding-3-small'
})

// Methods
const fetchDocuments = async () => {
  try {
    const res = await $fetch(`${config.public.apiBase}/knowledgebase/documents`)
    documents.value = res.documents
  } catch (error) {
    console.error('Error fetching docs:', error)
  }
}

const onFileChange = (e) => {
  selectedFile.value = e.target.files[0]
}

const uploadFile = async () => {
  if (!selectedFile.value) return
  
  isUploading.value = true
  const formData = new FormData()
  formData.append('file', selectedFile.value)
  
  try {
    await $fetch(`${config.public.apiBase}/knowledgebase/upload`, {
      method: 'POST',
      body: formData
    })
    selectedFile.value = null
    // reset input
    document.querySelector('input[type="file"]').value = ''
    await fetchDocuments()
  } catch (error) {
    console.error('Upload failed:', error)
  } finally {
    isUploading.value = false
  }
}

const startTraining = async () => {
  isTraining.value = true
  trainResult.value = null
  
  try {
    const res = await $fetch(`${config.public.apiBase}/knowledgebase/train`, {
      method: 'POST',
      body: {
        vectorDb: systemConfig.value.vectorDb,
        embeddingModel: systemConfig.value.embeddingModel
      }
    })
    trainResult.value = res
    await fetchDocuments() // Refresh statuses
  } catch (error) {
    console.error('Training failed:', error)
    trainResult.value = { message: 'Training failed. See console for details.' }
  } finally {
    setTimeout(() => {
      isTraining.value = false
    }, 1000) // Artificial delay for better UX
  }
}

// Utils
const statusClass = (status) => {
  const base = 'text-xs px-2 py-1 rounded-full '
  if (status === 'indexed') return base + 'bg-green-900/50 text-green-400 border border-green-800'
  if (status === 'failed') return base + 'bg-red-900/50 text-red-400 border border-red-800'
  return base + 'bg-blue-900/50 text-blue-400 border border-blue-800' // uploaded
}

const formatDate = (isoString) => {
  const d = new Date(isoString)
  return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  fetchDocuments()
})
</script>

<style scoped>
.gradient-text {
  background: linear-gradient(90deg, #f3f4f6, #9ca3af);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.text-primary {
  color: var(--color-primary);
}

.bg-indigo-900\/10 { background-color: rgba(49, 46, 129, 0.1); }
.border-indigo-500\/20 { border-color: rgba(99, 102, 241, 0.2); }
.bg-green-900\/50 { background-color: rgba(20, 83, 45, 0.5); }
.text-green-400 { color: #4ade80; }
.border-green-800 { border-color: rgb(22, 101, 52); }
.bg-blue-900\/50 { background-color: rgba(30, 58, 138, 0.5); }
.text-blue-400 { color: #60a5fa; }
.border-blue-800 { border-color: rgb(30, 64, 175); }
.bg-red-900\/50 { background-color: rgba(127, 29, 29, 0.5); }
.text-red-400 { color: #f87171; }
.border-red-800 { border-color: rgb(153, 27, 27); }

.pulse-btn {
  box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.7);
  animation: pulse-ring 2s infinite;
}

@keyframes pulse-ring {
  0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.7); }
  70% { transform: scale(1.02); box-shadow: 0 0 0 10px rgba(99, 102, 241, 0); }
  100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }
}
</style>
