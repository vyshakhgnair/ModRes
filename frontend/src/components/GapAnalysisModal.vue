<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/75 backdrop-blur-sm transition-opacity duration-300">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl p-8 max-h-[90vh] overflow-y-auto transform transition-all duration-300 scale-100">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-900 tracking-tight">Gap Analysis & Context</h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>
      
      <div v-if="loading" class="flex flex-col justify-center items-center py-12">
        <div class="animate-spin rounded-full h-16 w-16 border-4 border-indigo-100 border-t-primary mb-4"></div>
        <p class="text-gray-500 font-medium">Analyzing your resume...</p>
      </div>

      <div v-else>
        <div v-if="missingKeywords.length > 0" class="mb-8">
          <div class="flex items-center gap-2 mb-3">
            <svg class="w-5 h-5 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            <h3 class="text-lg font-bold text-gray-800">Missing Keywords</h3>
          </div>
          <div class="flex flex-wrap gap-2">
            <span v-for="keyword in missingKeywords" :key="keyword" class="px-4 py-1.5 bg-rose-50 text-rose-700 border border-rose-100 rounded-full text-sm font-medium">
              {{ keyword }}
            </span>
          </div>
        </div>

        <div v-if="questions.length > 0">
          <div class="flex items-center gap-2 mb-4">
            <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <h3 class="text-lg font-bold text-gray-800">Additional Context Needed</h3>
          </div>
          <div v-for="(item, index) in questions" :key="index" class="mb-6 p-5 bg-gray-50 rounded-xl border border-gray-100 hover:border-indigo-100 transition-colors">
            <p class="font-medium text-gray-800 mb-3">{{ item.question }}</p>
            <textarea 
              v-model="answers[item.keyword]" 
              class="w-full p-4 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent bg-white transition-all duration-200"
              rows="3"
              placeholder="Describe your experience..."
            ></textarea>
          </div>
        </div>

        <div v-else-if="missingKeywords.length === 0 && questions.length === 0" class="text-center py-8">
          <div class="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
          </div>
          <h3 class="text-xl font-bold text-gray-900 mb-2">Perfect Match!</h3>
          <p class="text-gray-500">We couldn't find any significant gaps in your resume for this job description.</p>
        </div>

        <div class="flex justify-end gap-4 mt-8 pt-6 border-t border-gray-100">
          <button @click="$emit('close')" class="px-6 py-2.5 text-gray-600 hover:text-gray-900 font-medium transition-colors">
            Cancel
          </button>
          <button @click="submitAnswers" class="px-8 py-2.5 bg-primary text-white rounded-xl hover:bg-indigo-700 shadow-lg hover:shadow-indigo-500/30 transition-all duration-200 font-bold">
            Update Resume
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  isOpen: Boolean,
  analysisData: Object,
  loading: Boolean
});

const emit = defineEmits(['close', 'submit']);

const missingKeywords = ref([]);
const questions = ref([]);
const answers = ref({});

watch(() => props.analysisData, (newData) => {
  if (newData) {
    missingKeywords.value = newData.missing_keywords || [];
    questions.value = newData.context_questions || [];
    // Initialize answers
    questions.value.forEach(q => {
      answers.value[q.keyword] = '';
    });
  }
});

const submitAnswers = () => {
  emit('submit', answers.value);
};
</script>
