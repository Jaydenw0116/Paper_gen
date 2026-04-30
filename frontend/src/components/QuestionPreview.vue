<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
      <Eye class="w-5 h-5" />
      题目预览
    </h3>

    <div v-if="question" class="space-y-4">
      <div class="p-4 bg-gray-50 rounded-lg">
        <div class="flex items-center gap-2 mb-2">
          <span class="font-bold text-gray-800">{{ question.original_no }}</span>
        </div>
        <p class="text-gray-700 whitespace-pre-wrap">{{ question.preview_text }}</p>
      </div>

      <div v-if="question.images?.length" class="space-y-3">
        <h4 class="text-sm font-medium text-gray-700">图片预览</h4>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div 
            v-for="(img, idx) in question.images" 
            :key="idx"
            class="relative group"
          >
            <img 
              :src="`data:image/png;base64,${img}`"
              class="w-full max-h-64 object-contain rounded-lg border border-gray-200"
              :alt="`图片${idx + 1}`"
            />
            <div class="absolute top-2 right-2 bg-black/50 text-white px-2 py-1 rounded text-xs">
              {{ idx + 1 }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12">
      <EyeOff class="w-12 h-12 mx-auto text-gray-300 mb-3" />
      <p class="text-gray-500">请选择一道题目进行预览</p>
    </div>
  </div>
</template>

<script setup>
import { Eye, EyeOff } from 'lucide-vue-next'

defineProps({
  question: {
    type: Object,
    default: null
  }
})
</script>