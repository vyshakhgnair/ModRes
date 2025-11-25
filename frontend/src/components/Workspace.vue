<template>
  <div class="flex flex-col h-screen bg-gray-50 font-sans">
    <NavBar />
    <div class="flex flex-1 overflow-hidden">
    <!-- Left Panel: Input & Form -->
    <div class="w-1/2 flex flex-col border-r border-gray-200 bg-white shadow-xl z-10 overflow-y-auto">
      <div class="p-8 border-b border-gray-100 bg-white">
        <div>
            <div class="flex items-center gap-3 mb-2">
            <div class="w-8 h-8 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            </div>
            <h1 class="text-2xl font-bold text-gray-900 tracking-tight">Resume Workspace</h1>
            </div>
            <p class="text-sm text-gray-500 ml-11">Create tailored resumes for your applications</p>
        </div>
      </div>

      <div class="flex-1 overflow-y-auto p-8 space-y-8">
        <!-- File Upload -->
        <div class="space-y-3">
          <label class="block text-sm font-semibold text-gray-700 uppercase tracking-wider">Resume</label>
          <div class="group relative">
            <label class="relative flex flex-col items-center justify-center w-full h-40 border-2 border-gray-200 border-dashed rounded-xl cursor-pointer bg-gray-50 hover:bg-indigo-50 hover:border-primary transition-all duration-300 ease-in-out">
              <div class="flex flex-col items-center justify-center pt-5 pb-6">
                <div class="mb-3 p-3 rounded-full bg-white shadow-sm group-hover:scale-110 transition-transform duration-300">
                  <svg class="w-6 h-6 text-gray-400 group-hover:text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                </div>
                <p class="mb-1 text-sm text-gray-500 font-medium"><span class="text-primary">Click to upload</span> or drag and drop</p>
                <p class="text-xs text-gray-400">PDF or DOCX (Max 10MB)</p>
                <p v-if="fileName" class="mt-3 text-sm font-semibold text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                  {{ fileName }}
                </p>
              </div>
              <input type="file" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" @change="handleFileUpload" accept=".pdf,.docx" />
            </label>
          </div>
        </div>

        <!-- Job Details -->
        <div class="space-y-3">
          <label class="block text-sm font-semibold text-gray-700 uppercase tracking-wider">Job Details</label>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <input 
                v-model="companyName" 
                type="text" 
                placeholder="Company Name"
                class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
              />
            </div>
            <div>
              <input 
                v-model="jobTitle" 
                type="text" 
                placeholder="Job Title"
                class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
              />
            </div>
          </div>
        </div>

        <!-- Job Description -->
        <div class="space-y-3">
          <label class="block text-sm font-semibold text-gray-700 uppercase tracking-wider">Job Description</label>
          <div class="relative">
            <textarea 
              v-model="jobDescription" 
              class="w-full h-64 p-4 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200 resize-none text-gray-700 leading-relaxed"
              placeholder="Paste the full job description here..."
            ></textarea>
            <div class="absolute bottom-3 right-3 text-xs text-gray-400">
              {{ jobDescription.length }} chars
            </div>
          </div>
        </div>

        <!-- Actions -->
        <button 
          @click="startAnalysis" 
          :disabled="!resumeText || !jobDescription || isAnalyzing"
          class="w-full py-4 bg-gradient-to-r from-primary to-indigo-600 text-white rounded-xl hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:-translate-y-0.5 font-bold text-lg flex items-center justify-center gap-2"
        >
          <svg v-if="isAnalyzing" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span v-else>Analyze & Tailor Resume</span>
        </button>

        <!-- Score Card -->
        <div v-if="scoreData" class="p-6 bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow duration-300">
          <div class="flex justify-between items-center mb-4">
            <h3 class="font-bold text-gray-800 text-lg">Match Score</h3>
            <div class="flex items-center gap-2">
              <span class="text-3xl font-black text-primary">{{ scoreData.score }}</span>
              <span class="text-gray-400 text-sm font-medium">/ 100</span>
            </div>
          </div>
          <div class="w-full bg-gray-100 rounded-full h-3 mb-6 overflow-hidden">
            <div 
              class="bg-gradient-to-r from-primary to-indigo-500 h-full rounded-full transition-all duration-1000 ease-out" 
              :style="{ width: scoreData.score + '%' }"
            ></div>
          </div>
          <div>
            <h4 class="text-sm font-bold text-gray-700 uppercase tracking-wider mb-3">Key Improvements</h4>
            <ul class="space-y-2">
              <li v-for="(suggestion, idx) in scoreData.improvement_suggestions" :key="idx" class="flex items-start gap-2 text-sm text-gray-600 bg-gray-50 p-2 rounded-lg">
                <svg class="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                {{ suggestion }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Panel: Preview & Edit -->
    <div class="w-1/2 bg-gray-900 flex flex-col relative overflow-hidden">
      <!-- Background Pattern -->
      <div class="absolute inset-0 opacity-20 pointer-events-none" 
           style="background-image: radial-gradient(#6366f1 1px, transparent 1px); background-size: 24px 24px;">
      </div>
      
      <!-- Toolbar -->
      <div class="relative z-20 px-6 py-4 bg-gray-800/80 backdrop-blur-md border-b border-gray-700 flex justify-between items-center shadow-lg">
        <div class="flex items-center gap-6">
          <div class="flex items-center gap-3 text-white">
            <div class="p-2 bg-indigo-500/20 rounded-lg">
              <svg class="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
            </div>
            <span class="font-semibold tracking-wide text-lg">Live Preview</span>
          </div>
          
          <!-- View Toggle -->
          <div v-if="latexCode || generatedData" class="flex bg-gray-900/50 rounded-lg p-1 border border-gray-700">
            <button 
              @click="viewMode = 'preview'" 
              :class="{'bg-gray-700 text-white shadow-sm': viewMode === 'preview', 'text-gray-400 hover:text-gray-200': viewMode !== 'preview'}"
              class="px-4 py-1.5 rounded-md text-sm font-medium transition-all duration-200 flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
              PDF
            </button>
            <button 
              @click="viewMode = 'edit'" 
              :class="{'bg-gray-700 text-white shadow-sm': viewMode === 'edit', 'text-gray-400 hover:text-gray-200': viewMode !== 'edit'}"
              class="px-4 py-1.5 rounded-md text-sm font-medium transition-all duration-200 flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path></svg>
              LaTeX
            </button>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <button v-if="viewMode === 'edit'" @click="updatePreview" class="group flex items-center gap-2 text-sm bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg transition-all duration-200 font-medium shadow-lg hover:shadow-indigo-500/25">
            <svg class="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
            Update
          </button>
          
          <div class="h-6 w-px bg-gray-700 mx-1" v-if="latexCode || pdfUrl"></div>

          <button v-if="latexCode" @click="downloadTex" class="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-colors" title="Download LaTeX Source">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
          </button>
          
          <button v-if="pdfUrl" @click="downloadPdf" class="flex items-center gap-2 text-sm bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-lg transition-all duration-200 font-medium shadow-lg hover:shadow-emerald-500/25">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
            Download PDF
          </button>
        </div>
      </div>
      
      <div class="flex-1 relative bg-gray-900/50 p-8 overflow-hidden flex flex-col">
        
        <!-- Loading Overlay -->
        <div v-if="isAnalyzing" class="absolute inset-0 z-50 bg-gray-900/80 backdrop-blur-sm flex flex-col items-center justify-center">
            <div class="relative">
                <div class="w-16 h-16 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin"></div>
                <div class="absolute inset-0 flex items-center justify-center">
                    <svg class="w-6 h-6 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                </div>
            </div>
            <p class="mt-4 text-white font-medium animate-pulse">Generating your resume...</p>
        </div>

        <!-- Preview Mode -->
        <div v-if="viewMode === 'preview'" class="flex-1 flex items-center justify-center h-full">
            <div v-if="pdfUrl" class="relative w-full h-full max-w-4xl shadow-2xl rounded-lg overflow-hidden border border-gray-700/50 bg-gray-800">
                <iframe :src="pdfUrl" class="w-full h-full bg-white"></iframe>
            </div>
            
            <!-- Empty State -->
            <div v-else class="text-center p-10 rounded-3xl bg-gray-800/40 border border-gray-700/50 backdrop-blur-md max-w-md mx-auto transform hover:scale-105 transition-transform duration-300">
                <div class="w-20 h-20 bg-gradient-to-br from-gray-700 to-gray-800 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-inner border border-gray-600/30">
                    <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                </div>
                <h3 class="text-2xl font-bold text-white mb-3">Ready to Create</h3>
                <p class="text-gray-400 leading-relaxed mb-6">Upload your resume and paste the job description to generate a perfectly tailored PDF.</p>
                <div class="flex justify-center gap-2">
                    <div class="h-2 w-2 rounded-full bg-gray-600 animate-bounce" style="animation-delay: 0s"></div>
                    <div class="h-2 w-2 rounded-full bg-gray-600 animate-bounce" style="animation-delay: 0.2s"></div>
                    <div class="h-2 w-2 rounded-full bg-gray-600 animate-bounce" style="animation-delay: 0.4s"></div>
                </div>
            </div>
        </div>

        <!-- Edit Mode -->
        <div v-else class="flex-1 relative rounded-xl overflow-hidden border border-gray-700 shadow-2xl bg-[#1e1e1e]">
            <div class="absolute top-0 left-0 right-0 h-8 bg-[#252526] flex items-center px-4 border-b border-[#333]">
                <span class="text-xs text-gray-400 font-mono">source.tex</span>
            </div>
            <textarea 
                v-model="editableCode" 
                class="w-full h-full bg-[#1e1e1e] text-gray-300 font-mono text-sm p-4 pt-10 resize-none focus:outline-none leading-relaxed"
                spellcheck="false"
            ></textarea>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <GapAnalysisModal 
      :is-open="showGapModal" 
      :analysis-data="analysisData"
      :loading="isAnalyzing"
      @close="showGapModal = false"
      @submit="handleGapSubmit"
    />

    <!-- Status Update Modal -->
    <div v-if="showStatusModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-8 max-w-sm w-full shadow-2xl text-center">
        <div class="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 mb-2">Resume Downloaded!</h3>
        <p class="text-gray-600 mb-6">Would you like to mark this application as <strong>Applied</strong> in your Job Tracker?</p>
        <div class="flex gap-3">
          <button @click="markAsApplied" class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white py-2.5 rounded-xl font-semibold transition-colors">
            Yes, Mark Applied
          </button>
          <button @click="showStatusModal = false" class="flex-1 border border-gray-200 hover:bg-gray-50 text-gray-700 py-2.5 rounded-xl font-semibold transition-colors">
            Not Yet
          </button>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router';
import { useApplicationStore } from '../stores/application';
import api from '../services/api';
import GapAnalysisModal from './GapAnalysisModal.vue';
import NavBar from './NavBar.vue';

const route = useRoute();
const router = useRouter();
const store = useApplicationStore();

// Navigation Guard
onBeforeRouteLeave((to, from, next) => {
  if (store.currentApplicationId && store.status === 'Drafting' && !showStatusModal.value) {
    const answer = window.confirm('You have an active application in progress. Do you want to leave? It will be saved in your Dashboard.');
    if (answer) {
      next();
    } else {
      next(false);
    }
  } else {
    next();
  }
});

const fileName = ref('');
const resumeText = ref('');
const jobDescription = ref('');
const companyName = ref('');
const jobTitle = ref('');

const isAnalyzing = ref(false);
const showGapModal = ref(false);
const showStatusModal = ref(false); // New modal for "Mark as Applied"
const analysisData = ref(null);
const scoreData = ref(null);
const pdfUrl = ref(null);

// Edit Mode State
const viewMode = ref('preview'); // 'preview' or 'edit'
const latexCode = ref('');
const generatedData = ref(null);
const editableCode = ref('');

// Sync editable code when latexCode changes
watch(latexCode, (newVal) => {
    if (newVal) editableCode.value = newVal;
});

// Watch for route changes to load application
watch(() => route.params.applicationId, async (newId) => {
    if (newId) {
        await store.fetchApplication(newId);
        jobDescription.value = store.jobDescription || '';
        companyName.value = store.companyName || '';
        jobTitle.value = store.jobTitle || '';
        
        // Restore resume data
        if (store.latexCode) {
            latexCode.value = store.latexCode;
            generatedData.value = store.tailoredData;
            editableCode.value = store.latexCode; // Ensure sync
            // Trigger compile to show PDF
            setTimeout(() => {
                updatePreview();
            }, 100);
        }
    } else {
        store.reset();
        jobDescription.value = '';
        companyName.value = '';
        jobTitle.value = '';
        latexCode.value = '';
        generatedData.value = null;
        pdfUrl.value = null;
    }
}, { immediate: true });

const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  fileName.value = file.name;
  try {
    const response = await api.parseResume(file);
    resumeText.value = response.data.text;
  } catch (error) {
    console.error('Error parsing resume:', error);
    alert('Failed to parse resume. Please check the backend connection.');
  }
};

const startAnalysis = async () => {
  if (!resumeText.value || !jobDescription.value) return;
  
  // If we don't have an application ID yet, we need to create one (Initiate Tailoring)
  // But we need Company and Title. If they are missing, we should probably ask or extract them.
  // For now, let's assume if they are missing, we try to extract or just use placeholders.
  // Actually, the prompt said "User enters JD and Company".
  // I need to add Company and Job Title inputs to the UI if they are not there.
  // The current UI only has JD textarea.
  // I will add inputs for Company and Title in the template later.
  // For now, let's assume they are provided or we extract them.
  
  isAnalyzing.value = true;
  
  try {
      // 1. Initiate Tailoring (Create Application if needed)
      if (!store.currentApplicationId) {
          // Fallback if inputs are empty
          const company = companyName.value || 'Unknown Company';
          const title = jobTitle.value || 'Unknown Role';
          
          await store.initiateTailoring(company, title, jobDescription.value, '');
          // Update URL to include ID
          router.replace(`/editor/${store.currentApplicationId}`);
      }

      showGapModal.value = true;
      
      // Parallel requests for Gap Analysis and Scoring
      const [gapRes, scoreRes] = await Promise.all([
        api.analyzeGap(resumeText.value, jobDescription.value),
        api.scoreResume(resumeText.value, jobDescription.value)
      ]);
      
      analysisData.value = gapRes.data;
      scoreData.value = scoreRes.data;
  } catch (error) {
    console.error('Analysis failed:', error);
    alert('Analysis failed. Please ensure the backend is running.');
    showGapModal.value = false;
  } finally {
    isAnalyzing.value = false;
  }
};

const handleGapSubmit = async (answers) => {
  showGapModal.value = false;
  isAnalyzing.value = true;
  
  try {
    // Pass application_id to prevent duplicate creation in backend
    const response = await api.tailorResume(resumeText.value, jobDescription.value, answers, store.currentApplicationId);
    
    // Store data and code
    generatedData.value = response.data.tailored_data;
    latexCode.value = response.data.latex_code;
    
    // Generate initial PDF
    await generatePdfFromData(response.data.tailored_data);
    
  } catch (error) {
    console.error('Tailoring failed:', error);
    alert('Failed to generate tailored resume. Please try again.');
  } finally {
    isAnalyzing.value = false;
  }
};

const generatePdfFromData = async (data) => {
    try {
        const response = await api.generatePdf(data);
        const blob = new Blob([response.data], { type: 'application/pdf' });
        pdfUrl.value = URL.createObjectURL(blob);
    } catch (error) {
        console.error('PDF generation failed:', error);
    }
};

const updatePreview = async () => {
    isAnalyzing.value = true;
    try {
        if (latexCode.value) {
            try {
                const response = await api.compileLatex(editableCode.value);
                const blob = new Blob([response.data], { type: 'application/pdf' });
                pdfUrl.value = URL.createObjectURL(blob);
                latexCode.value = editableCode.value; 
                viewMode.value = 'preview';
            } catch (error) {
                console.error('Compilation failed:', error);
                alert('LaTeX Compilation Failed!');
            }
        }
    } catch (error) {
        console.error('Update failed:', error);
    } finally {
        isAnalyzing.value = false;
    }
};

const downloadPdf = async () => {
  if (!pdfUrl.value) return;
  
  // Finalize Resume (Save to DB)
  try {
      await store.finalizeResume(generatedData.value, scoreData.value?.score);
      
      // Download file
      const link = document.createElement('a');
      link.href = pdfUrl.value;
      link.download = `Resume_${companyName.value || 'Tailored'}.pdf`;
      link.click();
      
      // Show Status Modal
      showStatusModal.value = true;
  } catch (error) {
      console.error('Error finalizing:', error);
      // Still allow download even if save fails?
      const link = document.createElement('a');
      link.href = pdfUrl.value;
      link.download = 'tailored_resume.pdf';
      link.click();
  }
};

const downloadTex = () => {
    if (!latexCode.value) return;
    const blob = new Blob([latexCode.value], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'tailored_resume.tex';
    link.click();
};

const markAsApplied = async () => {
    try {
        await api.post('/applications', {
            id: store.currentApplicationId,
            status: 'Applied'
        });
        showStatusModal.value = false;
        router.push('/tracker');
    } catch (error) {
        console.error('Error updating status:', error);
    }
};
</script>
