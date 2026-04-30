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
        <nav class="flex gap-2">
          <button
            :class="[
              'px-4 py-2 rounded-lg transition flex items-center gap-2',
              currentPage === 'upload' 
                ? 'bg-blue-600 text-white' 
                : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
            ]"
            @click="currentPage = 'upload'"
          >
            <Upload class="w-4 h-4" />
            题目上传
          </button>
          <button
            :class="[
              'px-4 py-2 rounded-lg transition flex items-center gap-2',
              currentPage === 'compose' 
                ? 'bg-blue-600 text-white' 
                : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
            ]"
            @click="currentPage = 'compose'"
          >
            <Edit3 class="w-4 h-4" />
            试卷组建
          </button>
        </nav>
      </div>
    </header>

    <main class="flex-1 overflow-auto">
      <UploadPage 
        v-if="currentPage === 'upload'" 
        @switch="handlePageSwitch"
      />
      <ComposePage 
        v-else 
        @switch="handlePageSwitch"
      />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FileText, Upload, Edit3 } from 'lucide-vue-next'
import UploadPage from './components/UploadPage.vue'
import ComposePage from './components/ComposePage.vue'

const currentPage = ref('upload')

const handlePageSwitch = (page) => {
  currentPage.value = page
}
</script>
