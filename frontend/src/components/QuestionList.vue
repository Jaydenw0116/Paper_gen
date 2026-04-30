<template>
  <div class="bg-white rounded-lg shadow-md p-6 h-full flex flex-col">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-gray-800 flex items-center gap-2">
        <ListOrdered class="w-5 h-5" />
        题目列表
      </h3>
      <span class="text-sm text-gray-500">共 {{ questions.length }} 题</span>
    </div>

    <div class="flex-1 overflow-hidden">
      <draggable
        v-model="localQuestions"
        item-key="id"
        class="h-full overflow-y-auto space-y-3"
        ghost-class="bg-blue-100"
        drag-class="opacity-50"
        animation="200"
        @change="handleReorder"
      >
        <template #item="{ element, index }">
          <div 
            class="p-4 border border-gray-200 rounded-lg cursor-move hover:border-blue-400 hover:shadow-sm transition-all group"
            :class="{ 'border-blue-500 bg-blue-50': selectedIds.includes(element.id) }"
          >
            <div class="flex items-start gap-3">
              <div class="flex flex-col items-center gap-1">
                <GripVertical class="w-4 h-4 text-gray-400 cursor-grab group-hover:text-gray-600" />
                <span class="text-xs text-gray-400">{{ index + 1 }}</span>
              </div>
              
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-2">
                  <span class="font-medium text-gray-800">{{ element.original_no }}</span>
                  <span 
                    class="px-2 py-0.5 text-xs rounded-full"
                    :class="selectedIds.includes(element.id) ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'"
                  >
                    {{ selectedIds.includes(element.id) ? '已选' : '未选' }}
                  </span>
                </div>
                <p class="text-sm text-gray-600 line-clamp-2">{{ element.preview_text }}</p>
                <div v-if="element.images?.length" class="mt-2 flex gap-2">
                  <img 
                    v-for="(img, idx) in element.images.slice(0, 3)" 
                    :key="idx"
                    :src="`data:image/png;base64,${img}`"
                    class="w-12 h-12 object-cover rounded"
                    :alt="`图片${idx + 1}`"
                  />
                  <span v-if="element.images.length > 3" class="w-12 h-12 flex items-center justify-center bg-gray-100 rounded text-xs text-gray-500">
                    +{{ element.images.length - 3 }}
                  </span>
                </div>
              </div>

              <button
                class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                @click="toggleSelect(element.id)"
              >
                <CheckCircle v-if="selectedIds.includes(element.id)" class="w-5 h-5 text-blue-500" />
                <Circle v-else class="w-5 h-5 text-gray-400" />
              </button>
            </div>
          </div>
        </template>
      </draggable>
    </div>

    <div class="mt-4 pt-4 border-t border-gray-200 flex gap-3">
      <button
        class="flex-1 py-2 px-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center justify-center gap-2"
        @click="selectAll"
      >
        <CheckSquare class="w-4 h-4" />
        全选
      </button>
      <button
        class="flex-1 py-2 px-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center justify-center gap-2"
        @click="deselectAll"
      >
        <Square class="w-4 h-4" />
        取消全选
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import draggable from 'vuedraggable'
import { 
  ListOrdered, 
  GripVertical, 
  CheckCircle, 
  Circle, 
  CheckSquare, 
  Square 
} from 'lucide-vue-next'

const props = defineProps({
  questions: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:selected-ids', 'reorder'])

const localQuestions = ref([...props.questions])
const selectedIds = ref([])

watch(() => props.questions, (newVal) => {
  localQuestions.value = [...newVal]
}, { deep: true })

const toggleSelect = (id) => {
  const index = selectedIds.value.indexOf(id)
  if (index > -1) {
    selectedIds.value.splice(index, 1)
  } else {
    selectedIds.value.push(id)
  }
  emit('update:selected-ids', [...selectedIds.value])
}

const selectAll = () => {
  selectedIds.value = localQuestions.value.map(q => q.id)
  emit('update:selected-ids', [...selectedIds.value])
}

const deselectAll = () => {
  selectedIds.value = []
  emit('update:selected-ids', [])
}

const handleReorder = () => {
  const orderedIds = localQuestions.value.map(q => q.id)
  emit('reorder', orderedIds)
}
</script>