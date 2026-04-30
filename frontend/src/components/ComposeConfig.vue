<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
      <Settings class="w-5 h-5" />
      组卷配置
    </h3>

    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">试卷标题</label>
        <input
          v-model="config.title"
          type="text"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
          placeholder="请输入试卷标题"
        />
      </div>

      <div class="p-3 bg-blue-50 rounded-lg">
        <div class="flex items-center gap-2 text-blue-700">
          <Info class="w-4 h-4" />
          <span class="text-sm">
            已选择 <strong>{{ selectedCount }}</strong> 道题目
          </span>
        </div>
      </div>

      <button
        class="w-full py-3 px-4 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="selectedCount === 0 || loading"
        @click="handleCompose"
      >
        <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
        <FileCheck v-else class="w-5 h-5" />
        {{ loading ? '组卷中...' : '生成试卷' }}
      </button>
    </div>

    <div v-if="error" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { Settings, Info, Loader2, FileCheck } from 'lucide-vue-next'
import { composeDocuments } from '../utils/api'

const props = defineProps({
  sessionId: {
    type: String,
    required: true
  },
  selectedIds: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['compose-success'])

const config = reactive({
  title: '试卷'
})

const loading = ref(false)
const error = ref('')

const selectedCount = () => props.selectedIds.length

const handleCompose = async () => {
  if (selectedCount() === 0) return

  loading.value = true
  error.value = ''

  try {
    await composeDocuments(
      props.sessionId,
      props.selectedIds,
      config.title
    )
    emit('compose-success')
  } catch (err) {
    error.value = err.response?.data?.detail || '组卷失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>