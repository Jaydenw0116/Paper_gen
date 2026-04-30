<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
      <Upload class="w-5 h-5" />
      上传文档
    </h3>
    
    <div class="space-y-4">
      <div 
        class="border-2 border-dashed rounded-lg p-6 text-center transition-all cursor-pointer"
        :class="questionFile ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'"
        @click="triggerQuestionUpload"
        @drop.prevent="handleQuestionDrop"
        @dragover.prevent
      >
        <FileText class="w-12 h-12 mx-auto mb-3" :class="questionFile ? 'text-blue-500' : 'text-gray-400'" />
        <p class="text-gray-600">{{ questionFile ? questionFile.name : '点击或拖拽上传题目文档' }}</p>
        <p class="text-sm text-gray-400 mt-1">支持 .docx 格式，最大20MB</p>
        <input 
          ref="questionInput"
          type="file" 
          accept=".docx" 
          class="hidden" 
          @change="handleQuestionSelect"
        />
      </div>

      <div 
        class="border-2 border-dashed rounded-lg p-6 text-center transition-all cursor-pointer"
        :class="answerFile ? 'border-green-500 bg-green-50' : 'border-gray-300 hover:border-green-400 hover:bg-gray-50'"
        @click="triggerAnswerUpload"
        @drop.prevent="handleAnswerDrop"
        @dragover.prevent
      >
        <FileText class="w-12 h-12 mx-auto mb-3" :class="answerFile ? 'text-green-500' : 'text-gray-400'" />
        <p class="text-gray-600">{{ answerFile ? answerFile.name : '点击或拖拽上传答案文档' }}</p>
        <p class="text-sm text-gray-400 mt-1">支持 .docx 格式，最大20MB</p>
        <input 
          ref="answerInput"
          type="file" 
          accept=".docx" 
          class="hidden" 
          @change="handleAnswerSelect"
        />
      </div>

      <button
        class="w-full py-3 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="!questionFile || !answerFile || loading"
        @click="handleUpload"
      >
        <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
        <Upload v-else class="w-5 h-5" />
        {{ loading ? '上传中...' : '开始切割' }}
      </button>
    </div>

    <div v-if="error" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Upload, FileText, Loader2 } from 'lucide-vue-next'
import { uploadDocuments } from '../utils/api'

const emit = defineEmits(['upload-success'])

const questionFile = ref(null)
const answerFile = ref(null)
const loading = ref(false)
const error = ref('')
const questionInput = ref(null)
const answerInput = ref(null)

const triggerQuestionUpload = () => questionInput.value?.click()
const triggerAnswerUpload = () => answerInput.value?.click()

const handleQuestionSelect = (e) => {
  const file = e.target.files[0]
  if (file) {
    validateFile(file, 'question')
  }
}

const handleAnswerSelect = (e) => {
  const file = e.target.files[0]
  if (file) {
    validateFile(file, 'answer')
  }
}

const handleQuestionDrop = (e) => {
  const file = e.dataTransfer.files[0]
  if (file) {
    validateFile(file, 'question')
  }
}

const handleAnswerDrop = (e) => {
  const file = e.dataTransfer.files[0]
  if (file) {
    validateFile(file, 'answer')
  }
}

const validateFile = (file, type) => {
  if (file.size > 20 * 1024 * 1024) {
    error.value = '文件大小超过20MB限制'
    return
  }
  
  if (!file.name.endsWith('.docx')) {
    error.value = '仅支持.docx格式'
    return
  }
  
  error.value = ''
  if (type === 'question') {
    questionFile.value = file
  } else {
    answerFile.value = file
  }
}

const handleUpload = async () => {
  if (!questionFile.value || !answerFile.value) return
  
  loading.value = true
  error.value = ''
  
  try {
    const response = await uploadDocuments(questionFile.value, answerFile.value)
    emit('upload-success', response.data)
  } catch (err) {
    error.value = err.response?.data?.detail || '上传失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>