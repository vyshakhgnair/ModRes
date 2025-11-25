<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <NavBar />
    
    <div class="max-w-7xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex justify-between items-center mb-6">
          <div>
            <h1 class="text-4xl font-bold text-gray-900 mb-2">Job Tracker</h1>
            <p class="text-gray-600">Manage and track your job applications</p>
          </div>
          <button 
            @click="showAddModal = true" 
            class="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white px-6 py-3 rounded-xl font-semibold flex items-center gap-2 shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-0.5"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
            Add Application
          </button>
        </div>

        <!-- Analytics Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-white p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow border border-gray-100">
            <div class="flex items-center justify-between mb-2">
              <div class="text-sm font-medium text-gray-500">Total</div>
              <div class="p-2 bg-gray-100 rounded-lg">
                <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
              </div>
            </div>
            <div class="text-3xl font-bold text-gray-900">{{ totalApplications }}</div>
          </div>
          
          <div class="bg-gradient-to-br from-indigo-50 to-indigo-100 p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow border border-indigo-200">
            <div class="flex items-center justify-between mb-2">
              <div class="text-sm font-medium text-indigo-700">Applied</div>
              <div class="p-2 bg-indigo-200 rounded-lg">
                <svg class="w-5 h-5 text-indigo-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              </div>
            </div>
            <div class="text-3xl font-bold text-indigo-700">{{ appliedCount }}</div>
          </div>
          
          <div class="bg-gradient-to-br from-amber-50 to-amber-100 p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow border border-amber-200">
            <div class="flex items-center justify-between mb-2">
              <div class="text-sm font-medium text-amber-700">Interviewing</div>
              <div class="p-2 bg-amber-200 rounded-lg">
                <svg class="w-5 h-5 text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z"></path></svg>
              </div>
            </div>
            <div class="text-3xl font-bold text-amber-700">{{ interviewingCount }}</div>
          </div>
          
          <div class="bg-gradient-to-br from-emerald-50 to-emerald-100 p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow border border-emerald-200">
            <div class="flex items-center justify-between mb-2">
              <div class="text-sm font-medium text-emerald-700">Offers</div>
              <div class="p-2 bg-emerald-200 rounded-lg">
                <svg class="w-5 h-5 text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              </div>
            </div>
            <div class="text-3xl font-bold text-emerald-700">{{ offerCount }}</div>
          </div>
        </div>
      </div>

      <!-- Kanban Board -->
      <div class="flex gap-4 overflow-x-auto pb-4">
        <div v-for="status in statuses" :key="status" class="flex-shrink-0 w-80">
          <div class="bg-white rounded-2xl p-4 shadow-sm border border-gray-200">
            <div class="flex items-center justify-between mb-4 pb-3 border-b border-gray-100">
              <h3 class="font-bold text-gray-900 flex items-center gap-2">
                <span class="w-3 h-3 rounded-full" :class="getStatusDotColor(status)"></span>
                {{ status }}
              </h3>
              <span class="text-sm font-semibold text-gray-500 bg-gray-100 px-2.5 py-1 rounded-full">
                {{ getApplicationsByStatus(status).length }}
              </span>
            </div>
            
            <div 
              class="space-y-3 min-h-[200px]"
              @dragover.prevent
              @drop="drop(status)"
            >
              <div 
                v-for="app in getApplicationsByStatus(status)" 
                :key="app.id"
                @dragstart="dragStart(app)"
                draggable="true"
                class="bg-white p-4 rounded-xl shadow-sm hover:shadow-md transition-all cursor-move border-l-4 group"
                :class="getStatusBorderColor(status)"
              >
                <div class="flex justify-between items-start mb-3">
                  <h4 class="font-semibold text-gray-900 flex-1 pr-2">{{ app.job_title }}</h4>
                  <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button 
                      @click="editApplication(app)" 
                      class="p-1.5 hover:bg-gray-100 rounded-lg transition-colors"
                      title="Edit"
                    >
                      <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                    </button>
                    <button 
                      @click="deleteApplication(app)" 
                      class="p-1.5 hover:bg-red-50 rounded-lg transition-colors"
                      title="Delete"
                    >
                      <svg class="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                    </button>
                    <button 
                      @click="triggerAutoApply(app)" 
                      class="p-1.5 hover:bg-indigo-50 rounded-lg transition-colors"
                      title="Auto-Apply"
                    >
                      <svg class="w-4 h-4 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                    </button>
                  </div>
                </div>
                
                <p class="text-sm text-gray-600 mb-3 flex items-center gap-2">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
                  {{ app.company }}
                </p>
                
                <div class="flex items-center justify-between text-xs text-gray-500">
                  <div class="flex items-center gap-1">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                    {{ formatDate(app.created_at) }}
                  </div>
                  <a v-if="app.job_url" :href="app.job_url" target="_blank" class="text-indigo-600 hover:text-indigo-800 font-medium">
                    View →
                  </a>
                </div>
              </div>
              
              <div v-if="getApplicationsByStatus(status).length === 0" class="text-center py-8 text-gray-400">
                <svg class="w-12 h-12 mx-auto mb-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path></svg>
                <p class="text-sm">No applications</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal || editingApp" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="closeModal">
      <div class="bg-white rounded-2xl p-8 max-w-md w-full mx-4 shadow-2xl transform transition-all">
        <h2 class="text-2xl font-bold mb-6">{{ editingApp ? 'Edit Application' : 'Add Application' }}</h2>
        <form @submit.prevent="saveApplication" class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Job Title *</label>
            <input v-model="formData.job_title" required class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all">
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Company *</label>
            <input v-model="formData.company" required class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all">
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Job URL</label>
            <input v-model="formData.job_url" type="url" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all" placeholder="https://...">
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Status</label>
            <select v-model="formData.status" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all">
              <option v-for="status in statuses" :key="status" :value="status">{{ status }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Notes</label>
            <textarea v-model="formData.notes" rows="3" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all resize-none" placeholder="Add any notes..."></textarea>
          </div>
          <div class="flex gap-3 pt-4">
            <button type="submit" class="flex-1 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white py-3 rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all">
              {{ editingApp ? 'Save Changes' : 'Add Application' }}
            </button>
            <button type="button" @click="closeModal" class="px-6 py-3 border-2 border-gray-300 rounded-xl hover:bg-gray-50 font-semibold transition-all">
              Cancel
            </button>
          </div>
          
          <div v-if="editingApp" class="pt-4 border-t border-gray-100 mt-4">
            <button type="button" @click="goToEditor" class="w-full bg-indigo-50 text-indigo-700 hover:bg-indigo-100 py-3 rounded-xl font-semibold flex items-center justify-center gap-2 transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                Tailor Resume for this Job
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import NavBar from '../components/NavBar.vue';

const router = useRouter();

const statuses = ['Drafting', 'Wishlist', 'Applied', 'Interviewing', 'Offer', 'Rejected'];
const applications = ref([]);
const showAddModal = ref(false);
const editingApp = ref(null);
const draggedApp = ref(null);

const formData = ref({
  job_title: '',
  company: '',
  job_url: '',
  status: 'Wishlist',
  notes: ''
});

const totalApplications = computed(() => applications.value.length);
const appliedCount = computed(() => applications.value.filter(a => a.status === 'Applied').length);
const interviewingCount = computed(() => applications.value.filter(a => a.status === 'Interviewing').length);
const offerCount = computed(() => applications.value.filter(a => a.status === 'Offer').length);

const getApplicationsByStatus = (status) => {
  return applications.value.filter(app => app.status === status);
};

const getStatusBorderColor = (status) => {
  const colors = {
    'Drafting': 'border-gray-300',
    'Wishlist': 'border-gray-400',
    'Applied': 'border-indigo-500',
    'Interviewing': 'border-amber-500',
    'Offer': 'border-emerald-500',
    'Rejected': 'border-red-500'
  };
  return colors[status] || 'border-gray-400';
};

const getStatusDotColor = (status) => {
  const colors = {
    'Drafting': 'bg-gray-300',
    'Wishlist': 'bg-gray-400',
    'Applied': 'bg-indigo-500',
    'Interviewing': 'bg-amber-500',
    'Offer': 'bg-emerald-500',
    'Rejected': 'bg-red-500'
  };
  return colors[status] || 'bg-gray-400';
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
};

const loadApplications = async () => {
  try {
    const response = await api.get('/applications');
    applications.value = response.data;
  } catch (error) {
    console.error('Error loading applications:', error);
  }
};

const saveApplication = async () => {
  try {
    if (editingApp.value) {
      // Update existing
      await api.post('/applications', {
        id: editingApp.value.id,
        ...formData.value
      });
    } else {
      // Create new
      await api.post('/applications', formData.value);
    }
    closeModal();
    await loadApplications();
  } catch (error) {
    console.error('Error saving application:', error);
    alert('Failed to save application');
  }
};



const goToEditor = () => {
    if (editingApp.value) {
        router.push(`/editor/${editingApp.value.id}`);
    }
};

const editApplication = (app) => {
  editingApp.value = app;
  formData.value = {
    job_title: app.job_title,
    company: app.company,
    job_url: app.job_url || '',
    status: app.status,
    notes: app.notes || ''
  };
};

const deleteApplication = async (app) => {
  if (!confirm(`Delete application for ${app.job_title} at ${app.company}?`)) {
    return;
  }
  
  try {
    await api.delete(`/applications/${app.id}`);
    await loadApplications();
  } catch (error) {
    console.error('Error deleting application:', error);
    alert('Failed to delete application');
  }
};

const closeModal = () => {
  showAddModal.value = false;
  editingApp.value = null;
  formData.value = {
    job_title: '',
    company: '',
    job_url: '',
    status: 'Wishlist',
    notes: ''
  };
};

const dragStart = (app) => {
  draggedApp.value = app;
};

const drop = async (newStatus) => {
  if (!draggedApp.value) return;
  
  try {
    await api.post('/applications', {
      id: draggedApp.value.id,
      status: newStatus
    });
    // Reload applications to get fresh data from server
    await loadApplications();
    draggedApp.value = null;
  } catch (error) {
    console.error('Error updating status:', error);
    alert('Failed to update status');
  }
};

const triggerAutoApply = async (app) => {
  if (!app.job_url) {
    alert('No job URL provided for this application');
    return;
  }
  
  if (!confirm(`Start auto-apply for ${app.job_title} at ${app.company}?`)) {
    return;
  }
  
  try {
    await api.post('/auto-apply', {
      job_url: app.job_url,
      application_id: app.id,
      headless: false
    });
    alert('Auto-apply agent started! Check the backend console for progress.');
  } catch (error) {
    console.error('Error starting auto-apply:', error);
    alert(error.response?.data?.error || 'Failed to start auto-apply');
  }
};

onMounted(() => {
  loadApplications();
});
</script>
