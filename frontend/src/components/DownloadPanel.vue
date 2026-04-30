<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
      <Download class="w-5 h-5" />
      下载试卷
    </h3>

    <div class="space-y-3">
      <button
        class="w-full py-3 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="loading"
        @click="downloadPaper"
      >
        <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
        <FileText v-else class="w-5 h-5" />
        {{ loading ? '下载中...' : '下载试卷' }}
      </button>

      <button
        class="w-full py-3 px-4 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="loading"
        @click="downloadAnswer"
      >
        <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
        <FileText v-else class="w-5 h-5" />
        {{ loading ? '下载中...' : '下载答案' }}
      </button>
    </div>

    <div class="mt-4 p-3 bg-gray-50 rounded-lg">
      <p class="text-sm text-gray-600">
        生成的试卷和答案文档将保持原始格式，包含所有公式、表格和图片。
      </p>
    </div>

    <div v-if="error" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Download, FileText, Loader2 } from 'lucide-vue-next'
import { downloadDocument } from '../utils/api'

const props = defineProps({
  sessionId: {
    type: String,
    required: true
  }
})

const loading = ref(false)
const error = ref('')

const downloadFile = async (docType, filename) => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await downloadDocument(props.sessionId, docType)
    
    const blob = new Blob([response.data], { 
      type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' 
    })
    
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (err) {
    error.value = err.response?.data?.detail || '下载失败，请重试'
  } finally {
    loading.value = false
  }
}

const downloadPaper = () => downloadFile('paper', '试卷.docx')
const downloadAnswer = () => downloadFile('answer', '答案.docx')
</script>