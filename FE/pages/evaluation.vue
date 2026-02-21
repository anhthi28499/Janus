<template>
  <div class="page-container">
    <!-- Sidebar: Evaluation Types -->
    <div class="sidebar p-4">
      <h2 class="text-xl font-bold mb-4 gradient-text">Eval Modules</h2>
      
      <div class="flex flex-col gap-2">
        <button 
          v-for="mode in evalModes" 
          :key="mode.id"
          class="btn text-left p-3 rounded-lg border border-transparent transition-all"
          :class="activeMode === mode.id ? 'bg-indigo-900/40 border-indigo-500/50 text-indigo-300' : 'bg-surface hover:bg-surface-light'"
          @click="activeMode = mode.id"
        >
          <div class="font-semibold mb-1">{{ mode.name }}</div>
          <div class="text-xs text-gray-500">{{ mode.desc }}</div>
        </button>
      </div>

      <div class="mt-8">
        <h3 class="text-sm font-semibold mb-3 text-gray-400">Recent Results</h3>
        <div v-if="history.length === 0" class="text-xs text-gray-500 italic">No runs yet.</div>
        <ul class="space-y-2">
          <li v-for="item in history" :key="item.id" class="text-xs glass-panel p-2 rounded flex justify-between">
            <span class="text-gray-400">{{ formatDate(item.created_at) }}</span>
            <span class="text-indigo-400">ID: {{ item.id }}</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content flex flex-col pt-8">
      <div class="max-w-3xl w-full mx-auto">
        <div class="mb-8 border-b border-gray-800 pb-4">
          <h2 class="text-2xl font-bold mb-2">{{ currentModeObj?.name }} Evaluation</h2>
          <p class="text-gray-400">{{ currentModeObj?.desc }}</p>
        </div>

        <div class="glass-panel p-6 rounded-xl animate-fade-in">
          <!-- Form based on mode -->
          <div v-if="activeMode === 'retrieval'" class="space-y-4">
            <div class="form-group">
              <label class="form-label">Evaluation Dataset (JSON/CSV)</label>
              <input type="file" class="form-input text-sm" />
            </div>
            <div class="form-group">
              <label class="form-label">Query Sample</label>
              <textarea class="form-input h-24" placeholder="Enter a sample query to test retrieval logic..."></textarea>
            </div>
          </div>

          <div v-else-if="activeMode === 'generation'" class="space-y-4">
            <div class="form-group">
              <label class="form-label">Context</label>
              <textarea class="form-input h-24" placeholder="Paste context here..."></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Question</label>
              <input type="text" class="form-input" placeholder="What is the question?" />
            </div>
            <div class="form-group">
              <label class="form-label">Generated Answer</label>
              <textarea class="form-input h-24" placeholder="Paste the LLM generated answer..."></textarea>
            </div>
          </div>

          <div v-else class="space-y-4">
            <div class="form-group">
              <label class="form-label">Evaluation Name</label>
              <input type="text" class="form-input" placeholder="e.g., Weekly E2E Test" />
            </div>
            <p class="text-sm text-gray-400 mb-4">
              End-to-end evaluation will run the entire graph (Planner -> Searcher -> Doer) using the configured test suite.
            </p>
          </div>

          <!-- Common Actions -->
          <div class="mt-8 flex items-center justify-between">
            <button 
              @click="runEvaluation" 
              class="btn btn-primary px-8 py-2"
              :disabled="isEvaluating"
            >
              {{ isEvaluating ? 'Evaluating...' : 'Run Evaluation' }}
            </button>
          </div>
        </div>

        <!-- Results Area -->
        <div v-if="evalResult" class="mt-8 glass-panel p-6 rounded-xl animate-fade-in border border-indigo-500/30">
          <h3 class="text-lg font-bold mb-4 text-indigo-400">Evaluation Metrics</h3>
          <div class="grid grid-cols-3 gap-4">
            <div v-for="(value, key) in evalResult.metrics" :key="key" class="bg-surface-light p-4 rounded-lg text-center">
              <div class="text-xs text-gray-400 uppercase tracking-wider mb-1">{{ key }}</div>
              <div class="text-2xl font-semibold text-white">{{ (value * 100).toFixed(1) }}%</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
const config = useRuntimeConfig()

const evalModes = [
  { id: 'retrieval', name: 'Retrieval Eval', desc: 'Test vector DB context accuracy (Precision, Recall)' },
  { id: 'generation', name: 'Generation Eval', desc: 'Test LLM response quality (BLEU, Faithfulness)' },
  { id: 'e2e', name: 'End-to-End Eval', desc: 'Test full Agent pipeline performance' }
]

const activeMode = ref('retrieval')
const currentModeObj = computed(() => evalModes.find(m => m.id === activeMode.value))

const isEvaluating = ref(false)
const evalResult = ref(null)
const history = ref([])

const fetchHistory = async () => {
  try {
    const res = await $fetch(`${config.public.apiBase}/evaluation/history/${activeMode.value}`)
    history.value = res.history
  } catch (e) {
    console.error('Fetch history failed', e)
  }
}

watch(activeMode, () => {
  evalResult.value = null
  fetchHistory()
})

onMounted(() => {
  fetchHistory()
})

const runEvaluation = async () => {
  isEvaluating.value = true
  evalResult.value = null
  
  try {
    const res = await $fetch(`${config.public.apiBase}/evaluation/${activeMode.value}`, {
      method: 'POST',
      body: {} // Send actual form data in a real implementation
    })
    evalResult.value = res
    await fetchHistory()
  } catch (error) {
    console.error('Eval failed', error)
  } finally {
    isEvaluating.value = false
  }
}

const formatDate = (isoString) => {
  const d = new Date(isoString)
  return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.gradient-text {
  background: linear-gradient(90deg, #818cf8, #c084fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
