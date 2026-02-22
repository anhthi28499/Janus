<template>
  <div class="page-container bg-surface flex flex-col items-center">
    <div class="chat-wrapper w-full max-w-4xl h-full flex flex-col shadow-2xl bg-background border-l border-r border-gray-800">
      
      <!-- Chat Header -->
      <div class="chat-header p-4 border-b border-gray-800 flex justify-between items-center bg-surface-light">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-primary to-purple-600 flex items-center justify-center text-white font-bold shadow-lg shadow-primary/30">
            J
          </div>
          <div>
            <h2 class="text-lg font-bold text-white leading-tight">Janus Agent</h2>
            <div class="text-xs text-green-400 flex items-center gap-1">
              <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"/> Online
            </div>
          </div>
        </div>
        <div class="text-xs text-gray-500 bg-surface px-3 py-1 rounded-full border border-gray-700">
          Session ID: {{ sessionId.slice(0, 8) || 'New' }}...
        </div>
      </div>

      <!-- Messages Area -->
      <div ref="messagesContainer" class="messages-area flex-1 overflow-y-auto p-6 space-y-6">
        <div v-if="messages.length === 0" class="h-full flex flex-col items-center justify-center text-gray-500 opacity-70">
          <svg class="w-16 h-16 mb-4 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
          <p>Start a conversation with Janus.</p>
          <p class="text-xs mt-2">Try asking about the weather, time, or search the knowledge base.</p>
        </div>

        <div 
          v-for="(msg, idx) in messages" 
          :key="idx" 
          class="message-row flex w-full"
          :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div 
            class="message-bubble max-w-[80%] rounded-2xl p-4 shadow-sm"
            :class="msg.role === 'user' 
              ? 'bg-primary text-white rounded-tr-sm' 
              : 'bg-surface-light text-gray-200 border border-gray-700 rounded-tl-sm'"
          >
            <div class="whitespace-pre-wrap">{{ msg.content }}</div>
            <div class="text-[10px] mt-2 text-right opacity-60">
              {{ formatTime(msg.timestamp || new Date().toISOString()) }}
            </div>
          </div>
        </div>

        <div v-if="isLoading" class="message-row flex w-full justify-start">
          <div class="message-bubble bg-surface-light border border-gray-700 rounded-2xl rounded-tl-sm p-4 w-24">
            <div class="flex space-x-2 justify-center items-center h-4">
              <div class="h-2 w-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0s"/>
              <div class="h-2 w-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"/>
              <div class="h-2 w-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"/>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="input-area p-4 border-t border-gray-800 bg-surface">
        <form class="flex gap-2 relative" @submit.prevent="sendMessage">
          <input 
            v-model="inputQuery" 
            type="text" 
            class="flex-1 bg-background border border-gray-700 text-white rounded-full py-3 pl-6 pr-12 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary shadow-inner"
            placeholder="Ask Janus anything..."
            :disabled="isLoading"
          >
          <button 
            type="submit" 
            class="absolute right-2 top-1/2 transform -translate-y-1/2 w-10 h-10 rounded-full bg-primary hover:bg-primary-hover flex items-center justify-center text-white transition-colors"
            :disabled="!inputQuery.trim() || isLoading"
            :class="{'opacity-50 cursor-not-allowed': !inputQuery.trim() || isLoading}"
          >
            <svg class="w-5 h-5 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </form>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
const config = useRuntimeConfig()

const sessionId = ref('')
const messages = ref([])
const inputQuery = ref('')
const isLoading = ref(false)
const messagesContainer = ref(null)

// Initialize Session
onMounted(() => {
  // Load session from local storage if exists
  const savedSession = localStorage.getItem('janus_session_id')
  if (savedSession) {
    sessionId.value = savedSession
    fetchHistory()
  } else {
    sessionId.value = crypto.randomUUID()
    localStorage.setItem('janus_session_id', sessionId.value)
  }
})

const fetchHistory = async () => {
  try {
    const res = await $fetch(`${config.public.apiBase}/chat/history/${sessionId.value}`)
    if (res && res.messages) {
      messages.value = res.messages
      scrollToBottom()
    }
  } catch (error) {
    console.error('Failed to load history', error)
  }
}

const sendMessage = async () => {
  const q = inputQuery.value.trim()
  if (!q) return

  // Optimistic UI update
  messages.value.push({ role: 'user', content: q, timestamp: new Date().toISOString() })
  inputQuery.value = ''
  isLoading.value = true
  scrollToBottom()

  try {
    const res = await $fetch(`${config.public.apiBase}/chat/`, {
      method: 'POST',
      body: {
        session_id: sessionId.value,
        message: q
      }
    })
    
    // Server returns the new session ID and the AI response
    sessionId.value = res.session_id
    localStorage.setItem('janus_session_id', sessionId.value)
    
    messages.value.push({
      role: 'assistant',
      content: res.response,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    console.error('Chat error', error)
    messages.value.push({
      role: 'assistant',
      content: 'Sorry, I encountered an error communicating with the server.',
      timestamp: new Date().toISOString()
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const formatTime = (isoString) => {
  const d = new Date(isoString)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.message-bubble {
  word-break: break-word;
}
/* Custom Scrollbar for chat */
.messages-area::-webkit-scrollbar {
  width: 6px;
}
.messages-area::-webkit-scrollbar-track {
  background: transparent;
}
.messages-area::-webkit-scrollbar-thumb {
  background-color: var(--color-border);
  border-radius: 20px;
}
</style>
