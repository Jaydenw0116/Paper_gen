<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto p-6">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">试卷组建</h2>
        <div class="flex gap-3">
          <button
            v-if="composeSuccess"
            @click="downloadFile('paper')"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            下载试卷
          </button>
          <button
            v-if="composeSuccess"
            @click="downloadFile('answer')"
            class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition"
          >
            下载答案
          </button>
          <button
            @click="composePaper"
            :disabled="selectedQuestions.length === 0 || composing"
            class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ composing ? '组卷中...' : '生成试卷' }}
          </button>
          <button
            @click="switchToUpload"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            切换到上传
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white rounded-xl shadow-md p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold text-gray-700">题库题目</h3>
            <div class="flex gap-2">
              <button
                @click="selectAll"
                :disabled="bankQuestions.length === 0"
                class="px-3 py-1 bg-blue-100 text-blue-600 rounded hover:bg-blue-200 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
              >
                全选
              </button>
              <button
                @click="deselectAll"
                :disabled="selectedQuestions.length === 0"
                class="px-3 py-1 bg-gray-100 text-gray-600 rounded hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
              >
                全不选
              </button>
            </div>
          </div>
          <div v-if="loading" class="text-center py-8 text-gray-500">
            加载中...
          </div>
          <div v-else-if="bankQuestions.length === 0" class="text-center py-8 text-gray-500">
            题库为空，请先前往上传页面添加题目
          </div>
          <div v-else class="space-y-3">
            <div
              v-for="q in bankQuestions"
              :key="q.id"
              class="border rounded-lg p-3 hover:bg-gray-50"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="text-sm font-medium text-gray-800 mb-1">
                    [{{ q.source_file || '未知来源' }}]-{{ q.original_no || '第题' }}
                  </div>
                  <div class="text-sm text-gray-600 line-clamp-2">{{ q.preview_text }}</div>
                </div>
                <button
                  @click="addToSelected(q)"
                  :disabled="selectedQuestions.some(sq => sq.id === q.id)"
                  class="ml-2 px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                >
                  添加
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-md p-6">
          <h3 class="text-lg font-semibold text-gray-700 mb-4">已选题目</h3>
          <div v-if="selectedQuestions.length === 0" class="text-center py-8 text-gray-500">
            请从左侧题库添加题目
          </div>
          <div v-else class="space-y-3">
            <div
              v-for="(q, index) in selectedQuestions"
              :key="q.id"
              class="border border-blue-200 bg-blue-50 rounded-lg p-3 cursor-move hover:border-blue-400 transition-colors"
              draggable="true"
              @dragstart="dragStart(index)"
              @dragover.prevent
              @drop="drop(index)"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-1">
                    <span class="bg-blue-500 text-white rounded px-2 py-0.5 text-sm font-medium">
                      {{ index + 1 }}
                    </span>
                    <span class="text-sm font-medium text-gray-800">
                      [{{ q.source_file || '未知来源' }}]-{{ q.original_no || '第题' }}
                    </span>
                  </div>
                  <div class="text-sm text-gray-600 line-clamp-2">{{ q.preview_text }}</div>
                </div>
              </div>
              <div class="flex justify-end items-center mt-2 pt-2 border-t border-blue-200">
                <button
                  @click="removeFromSelected(q.id)"
                  class="px-2 py-1 bg-red-100 text-red-600 rounded hover:bg-red-200 text-xs"
                >
                  移除
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="error" class="mt-4 p-3 bg-red-50 rounded-lg text-red-600 text-sm">
        ❌ {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { getQuestionBank, composeDocuments, downloadDocument } from '../utils/api.js'

const emit = defineEmits(['switch'])

const loading = ref(false)
const composing = ref(false)
const composeSuccess = ref(false)
const error = ref('')
const bankQuestions = ref([])
const selectedQuestions = ref([])
const downloadSessionId = ref('')
const draggedIndex = ref(-1)

const config = reactive({
  title: '试卷'
})

const addToSelected = (question) => {
  if (!selectedQuestions.value.some(sq => sq.id === question.id)) {
    selectedQuestions.value.push(question)
  }
}

const removeFromSelected = (questionId) => {
  const index = selectedQuestions.value.findIndex(sq => sq.id === questionId)
  if (index > -1) {
    selectedQuestions.value.splice(index, 1)
  }
}

const selectAll = () => {
  selectedQuestions.value = [...bankQuestions.value]
}

const deselectAll = () => {
  selectedQuestions.value = []
}

const dragStart = (index) => {
  draggedIndex.value = index
}

const drop = (index) => {
  if (draggedIndex.value === -1 || draggedIndex.value === index) {
    draggedIndex.value = -1
    return
  }

  const draggedItem = selectedQuestions.value.splice(draggedIndex.value, 1)[0]
  selectedQuestions.value.splice(index, 0, draggedItem)
  draggedIndex.value = -1
}

const loadBank = async () => {
  loading.value = true
  try {
    const response = await getQuestionBank()
    bankQuestions.value = response.data
  } catch (err) {
    console.error('Load bank error:', err)
  } finally {
    loading.value = false
  }
}

const composePaper = async () => {
  if (selectedQuestions.value.length === 0) return

  composing.value = true
  error.value = ''
  composeSuccess.value = false

  try {
    const questionIds = selectedQuestions.value.map(q => q.id)
    const response = await composeDocuments(questionIds, config.title)
    downloadSessionId.value = response.data.session_id
    composeSuccess.value = true
  } catch (err) {
    console.error('Compose error:', err)
    error.value = err.response?.data?.detail || err.message || '组卷失败'
  } finally {
    composing.value = false
  }
}

const downloadFile = async (docType) => {
  try {
    const response = await downloadDocument(downloadSessionId.value, docType)
    const filename = docType === 'paper' ? '试卷.docx' : '答案.docx'
    const blob = new Blob([response.data], { type: response.headers['content-type'] })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (err) {
    console.error('Download error:', err)
    alert('下载失败')
  }
}

const switchToUpload = () => {
  emit('switch', 'upload')
}

loadBank()
</script>
