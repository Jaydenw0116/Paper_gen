<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-6xl mx-auto p-6">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">题目上传</h2>
        <div class="flex gap-3">
          <button 
            @click="switchToCompose"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            切换到组卷
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white rounded-xl shadow-md p-6">
          <h3 class="text-lg font-semibold text-gray-700 mb-4">上传文档</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-600 mb-2">题目文档 (.docx)</label>
              <input 
                type="file" 
                ref="questionFileRef"
                accept=".docx"
                @change="handleQuestionFileChange"
                class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-blue-50 file:text-blue-600 hover:file:bg-blue-100"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-600 mb-2">答案文档 (.docx)</label>
              <input 
                type="file" 
                ref="answerFileRef"
                accept=".docx"
                @change="handleAnswerFileChange"
                class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-blue-50 file:text-blue-600 hover:file:bg-blue-100"
              />
            </div>
            <button 
              @click="handleUpload"
              :disabled="!questionFile || !answerFile || loading"
              class="w-full py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ loading ? '上传中...' : '开始切割' }}
            </button>
            <div v-if="uploadSuccess" class="text-green-600 text-sm">
              ✅ 上传成功，识别到 {{ uploadedQuestions.length }} 道题目
            </div>
            <div v-if="error" class="text-red-600 text-sm">
              ❌ {{ error }}
            </div>
          </div>
        </div>

        <div v-if="uploadedQuestions.length > 0" class="bg-white rounded-xl shadow-md p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold text-gray-700">识别的题目</h3>
            <button 
              @click="addToBank"
              :disabled="addingToBank"
              class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition disabled:opacity-50"
            >
              {{ addingToBank ? '添加中...' : '全部加入题库' }}
            </button>
          </div>
          <div class="space-y-3 max-h-96 overflow-y-auto">
            <div 
              v-for="(q, index) in uploadedQuestions" 
              :key="q.id"
              class="border rounded-lg p-3 hover:bg-gray-50"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="text-sm font-medium text-gray-800 mb-1">
                    [{{ q.source_file }}]-{{ q.original_no }}
                  </div>
                  <div class="text-sm text-gray-600 line-clamp-2">{{ q.preview_text }}</div>
                </div>
              </div>
            </div>
          </div>
          <button 
            @click="clearUploaded"
            class="mt-4 w-full py-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition"
          >
            清除当前上传
          </button>
        </div>
      </div>

      <div class="mt-6 bg-white rounded-xl shadow-md p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-700">题库管理</h3>
          <button 
            @click="clearBankConfirm"
            class="px-3 py-1 text-red-500 hover:text-red-700 text-sm"
          >
            清空题库
          </button>
        </div>
        <div v-if="bankLoading" class="text-center py-8 text-gray-500">
          加载中...
        </div>
        <div v-else-if="bankQuestions.length === 0" class="text-center py-8 text-gray-500">
          题库为空，请先上传题目
        </div>
        <div v-else class="space-y-3 max-h-96 overflow-y-auto">
          <div 
            v-for="(q, index) in bankQuestions" 
            :key="q.id"
            class="border rounded-lg p-3 hover:bg-gray-50"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="text-sm font-medium text-gray-800 mb-1">
                  [{{ q.source_file || '未知来源' }}]-{{ q.original_no || '第' + (index + 1) + '题' }}
                </div>
                <div class="text-sm text-gray-600 line-clamp-2">{{ q.preview_text }}</div>
              </div>
              <button 
                @click="removeQuestion(q.id)"
                class="ml-4 text-red-500 hover:text-red-700"
              >
                删除
              </button>
            </div>
          </div>
        </div>
        <div v-if="bankQuestions.length > 0" class="mt-4 text-sm text-gray-500">
          题库中共有 {{ bankQuestions.length }} 道题目
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>import { ref } from 'vue';
import { uploadDocuments, uploadToBank, getQuestionBank, removeFromBank, clearBank } from '../utils/api.js';
const emit = defineEmits(['switch']);
const questionFile = ref(null);
const answerFile = ref(null);
const questionFileRef = ref(null);
const answerFileRef = ref(null);
const loading = ref(false);
const addingToBank = ref(false);
const bankLoading = ref(false);
const error = ref('');
const uploadSuccess = ref(false);
const uploadedQuestions = ref([]);
const bankQuestions = ref([]);
const currentSessionId = ref('');
const handleQuestionFileChange = (e) => {
 questionFile.value = e.target.files[0];
};
const handleAnswerFileChange = (e) => {
 answerFile.value = e.target.files[0];
};
const handleUpload = async () => {
 if (!questionFile.value || !answerFile.value)
 return;
 loading.value = true;
 error.value = '';
 uploadSuccess.value = false;
 try {
 const response = await uploadDocuments(questionFile.value, answerFile.value);
 uploadedQuestions.value = response.data.questions;
 currentSessionId.value = response.data.session_id;
 uploadSuccess.value = true;
 }
 catch (err) {
 console.error('Upload error:', err);
 error.value = err.response?.data?.detail || err.message || '上传失败，请重试';
 }
 finally {
 loading.value = false;
 }
};
const addToBank = async () => {
 if (uploadedQuestions.value.length === 0)
 return;
 addingToBank.value = true;
 try {
 await uploadToBank(currentSessionId.value, uploadedQuestions.value.map(q => q.id));
 await loadBank();
 uploadedQuestions.value = [];
 currentSessionId.value = '';
 uploadSuccess.value = false;
 }
 catch (err) {
 console.error('Add to bank error:', err);
 error.value = err.response?.data?.detail || err.message || '添加到题库失败';
 }
 finally {
 addingToBank.value = false;
 }
};
const loadBank = async () => {
 bankLoading.value = true;
 try {
 const response = await getQuestionBank();
 bankQuestions.value = response.data;
 }
 catch (err) {
 console.error('Load bank error:', err);
 }
 finally {
 bankLoading.value = false;
 }
};
const removeQuestion = async (questionId) => {
 try {
 await removeFromBank(questionId);
 bankQuestions.value = bankQuestions.value.filter(q => q.id !== questionId);
 }
 catch (err) {
 console.error('Remove question error:', err);
 alert('删除失败');
 }
};
const clearBankConfirm = async () => {
 if (!confirm('确定要清空题库吗？此操作不可恢复。'))
 return;
 try {
 await clearBank();
 bankQuestions.value = [];
 }
 catch (err) {
 console.error('Clear bank error:', err);
 alert('清空失败');
 }
};
const clearUploaded = () => {
 uploadedQuestions.value = [];
 currentSessionId.value = '';
 uploadSuccess.value = false;
 error.value = '';
 questionFile.value = null;
 answerFile.value = null;
 if (questionFileRef.value)
 questionFileRef.value.value = '';
 if (answerFileRef.value)
 answerFileRef.value.value = '';
};
const switchToCompose = () => {
 emit('switch', 'compose');
};
loadBank();
</script>
