<template>
  <div class="h-screen bg-gray-100 flex flex-col">
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
            <FileText class="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 class="text-xl font-bold text-gray-800">智能组卷系统</h1>
            <p class="text-sm text-gray-500">基于Word底层XML的精准切割与缝合技术</p>
          </div>
        </div>
        <button
          v-if="sessionId"
          class="px-4 py-2 text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors flex items-center gap-2"
          @click="handleReset"
        >
          <RotateCcw class="w-4 h-4" />
          重新开始
        </button>
      </div>
    </header>

    <main class="flex-1 flex">
      <div 
        v-if="!sessionId"
        class="flex-1 flex items-center justify-center p-8"
      >
        <div class="w-full max-w-md">
          <FileUploader @upload-success="handleUploadSuccess" />
        </div>
      </div>

      <div v-else class="flex-1 flex overflow-hidden">
        <div 
          class="flex-1 flex flex-col overflow-hidden border-r border-gray-200"
          :style="{ width: leftPanelWidth + '%' }"
        >
          <div class="flex-1 overflow-hidden p-4">
            <QuestionList 
              :questions="questions" 
              :selected-ids="selectedIds"
              @update:selected-ids="handleSelectedIdsChange"
              @reorder="handleReorder"
            />
          </div>
        </div>

        <div 
          class="w-1 bg-gray-300 cursor-col-resize hover:bg-gray-400 transition-colors flex items-center justify-center"
          @mousedown="startResize"
        >
          <GripVertical class="w-4 h-4 text-gray-500" />
        </div>

        <div 
          class="flex-1 flex flex-col overflow-hidden p-4"
          :style="{ width: (100 - leftPanelWidth) + '%' }"
        >
          <div class="flex-1 overflow-y-auto space-y-4">
            <QuestionPreview :question="selectedQuestion" />
            <ComposeConfig 
              :session-id="sessionId" 
              :selected-ids="selectedIds"
              @compose-success="handleComposeSuccess"
            />
            <DownloadPanel 
              v-if="composed"
              :session-id="sessionId"
            />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { FileText, RotateCcw, GripVertical } from 'lucide-vue-next'
import FileUploader from './components/FileUploader.vue'
import QuestionList from './components/QuestionList.vue'
import QuestionPreview from './components/QuestionPreview.vue'
import ComposeConfig from './components/ComposeConfig.vue'
import DownloadPanel from './components/DownloadPanel.vue'

const sessionId = ref('')
const questions = ref([])
const selectedIds = ref([])
const leftPanelWidth = ref(50)
const composed = ref(false)

const selectedQuestion = computed(() => {
  if (selectedIds.value.length === 1) {
    return questions.value.find(q => q.id === selectedIds.value[0]) || null
  }
  return null
})

const handleUploadSuccess = (data) => {
  sessionId.value = data.session_id
  questions.value = data.questions
  selectedIds.value = []
  composed.value = false
}

const handleSelectedIdsChange = (ids) => {
  selectedIds.value = ids
}

const handleReorder = (orderedIds) => {
  questions.value = orderedIds.map(id => questions.value.find(q => q.id === id)).filter(Boolean)
}

const handleComposeSuccess = () => {
  composed.value = true
}

const handleReset = () => {
  sessionId.value = ''
  questions.value = []
  selectedIds.value = []
  composed.value = false
}

let isResizing = false

const startResize = (e) => {
  isResizing = true
  document.addEventListener('mousemove', handleResize)
  document.addEventListener('mouseup', stopResize)
}

const handleResize = (e) => {
  if (!isResizing) return
  
  const container = e.currentTarget.parentElement
  const rect = container.getBoundingClientRect()
  const x = e.clientX - rect.left
  const percentage = (x / rect.width) * 100
  
  leftPanelWidth.value = Math.max(20, Math.min(80, percentage))
}

const stopResize = () => {
  isResizing = false
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', stopResize)
}

onMounted(() => {
  document.addEventListener('mousemove', handleResize)
  document.addEventListener('mouseup', stopResize)
})

onUnmounted(() => {
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', stopResize)
})
</script>