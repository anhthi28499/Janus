<template>
  <div class="page-container relative flex h-screen w-full flex-col items-center justify-center bg-background overflow-hidden font-sans">
    
    <!-- Background Accents -->
    <div class="absolute -top-[20%] -left-[10%] h-[70vw] w-[70vw] rounded-full bg-primary/10 blur-[120px] pointer-events-none"></div>
    <div class="absolute -bottom-[20%] -right-[10%] h-[60vw] w-[60vw] rounded-full bg-purple-600/10 blur-[120px] pointer-events-none"></div>

    <div class="z-10 flex w-full max-w-5xl flex-col h-[90vh] md:my-6 md:rounded-3xl border border-white/5 bg-surface/80 backdrop-blur-2xl shadow-2xl shadow-black/50 overflow-hidden transform transition-all">
      
      <!-- Chat Header -->
      <div class="chat-header relative flex items-center justify-between border-b border-white/5 bg-surface/40 px-6 py-4 backdrop-blur-md">
        <div class="flex items-center gap-4">
          <div class="relative flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-purple-600 font-bold text-white shadow-lg shadow-primary/20 ring-1 ring-white/10 overflow-hidden">
            <span class="text-xl tracking-tight relative z-10">J</span>
            <div class="absolute inset-0 bg-white/20 opacity-0 hover:opacity-100 transition-opacity duration-300"></div>
          </div>
          <div>
            <h2 class="text-lg font-semibold tracking-wide text-white">Janus AI</h2>
            <div class="flex items-center gap-2 text-xs font-medium text-emerald-400">
              <span class="relative flex h-2 w-2">
                <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span>
                <span class="relative inline-flex h-2 w-2 rounded-full bg-emerald-500"></span>
              </span>
              Connected
            </div>
          </div>
        </div>
        <div class="flex items-center gap-2 rounded-full border border-white/5 bg-black/20 px-4 py-1.5 text-xs font-medium text-gray-400 shadow-inner backdrop-blur-sm">
          <span>Session</span>
          <span class="font-mono text-gray-300">{{ sessionId.slice(0, 8) || 'New' }}</span>
        </div>
      </div>

      <!-- Messages Area -->
      <div ref="messagesContainer" class="messages-area flex-1 overflow-y-auto p-6 md:p-8 space-y-8 scroll-smooth">
        <div v-if="messages.length === 0" class="flex h-full flex-col items-center justify-center text-center animate-fade-in">
          <div class="mb-6 flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-tr from-surface-light to-surface border border-white/5 shadow-2xl">
            <svg class="h-10 w-10 text-primary/70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <h3 class="mb-2 text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">Welcome to Janus</h3>
          <p class="max-w-sm text-sm text-gray-400 leading-relaxed">I am your intelligent assistant. Let's explore ideas, solve problems, or chat about anything.</p>
        </div>

        <div 
          v-for="(msg, idx) in messages" 
          :key="idx" 
          class="message-row flex w-full animate-fade-in"
          :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
          :style="{ animationDelay: `${idx * 50}ms` }"
        >
          <div 
            class="group relative max-w-[85%] md:max-w-[75%] px-5 py-4 text-[15px] leading-relaxed shadow-xl transition-all duration-300 hover:shadow-2xl"
            :class="msg.role === 'user' 
              ? 'bg-gradient-to-br from-primary to-primary-hover text-white rounded-3xl rounded-tr-sm shadow-primary/20' 
              : 'bg-surface-light/80 backdrop-blur-sm text-gray-100 border border-white/5 rounded-3xl rounded-tl-sm shadow-black/20'"
          >
            <div class="whitespace-pre-wrap">{{ msg.content }}</div>
            <div 
              class="mt-2 text-[11px] font-medium tracking-wide opacity-50 group-hover:opacity-100 transition-opacity"
              :class="msg.role === 'user' ? 'text-right text-primary-100' : 'text-left text-gray-500'"
            >
              {{ formatTime(msg.timestamp || new Date().toISOString()) }}
            </div>
          </div>
        </div>

        <div v-if="isLoading" class="message-row flex w-full justify-start animate-fade-in">
          <div class="flex items-center gap-1.5 rounded-3xl rounded-tl-sm border border-white/5 bg-surface-light/50 backdrop-blur-sm px-5 py-4 shadow-xl">
            <div class="h-2 w-2 animate-bounce rounded-full bg-primary/60" style="animation-delay: 0s"></div>
            <div class="h-2 w-2 animate-bounce rounded-full bg-primary/60" style="animation-delay: 0.2s"></div>
            <div class="h-2 w-2 animate-bounce rounded-full bg-primary/60" style="animation-delay: 0.4s"></div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="relative border-t border-white/5 bg-surface/60 p-4 md:p-6 backdrop-blur-xl">
        <form class="relative flex items-end gap-3" @submit.prevent="sendMessage">
          <div class="relative flex-1 group">
            <div class="absolute -inset-0.5 rounded-3xl bg-gradient-to-r from-primary to-purple-600 opacity-20 blur transition duration-500 group-hover:opacity-50 group-focus-within:opacity-100" v-if="!isLoading"></div>
            <textarea 
              v-model="inputQuery" 
              rows="1"
              @keydown.enter.prevent="sendMessage"
              class="relative w-full resize-none rounded-3xl border border-white/10 bg-background/80 px-6 py-4 pr-14 text-[15px] text-white placeholder-gray-500 shadow-inner backdrop-blur-sm focus:border-white/20 focus:outline-none focus:ring-0 transition-all custom-scrollbar"
              placeholder="Message Janus..."
              :disabled="isLoading"
              style="min-height: 56px; max-height: 150px;"
            ></textarea>
          </div>
          <button 
            type="submit" 
            class="relative mb-0.5 flex h-13 w-13 flex-shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-primary to-purple-600 text-white shadow-lg shadow-primary/30 transition-all duration-300 transform"
            :class="!inputQuery.trim() || isLoading ? 'opacity-50 cursor-not-allowed scale-95 grayscale-[50%]' : 'hover:scale-105 hover:shadow-primary/50 active:scale-95'"
            :disabled="!inputQuery.trim() || isLoading"
            style="width: 52px; height: 52px;"
          >
            <svg class="h-5 w-5 ml-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </form>
        <div class="mt-3 text-center text-[11px] font-medium text-gray-600">
          Janus may produce inaccurate information about people, places, or facts.
        </div>
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
