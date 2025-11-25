<template>
  <div class="min-h-screen bg-gray-50 font-sans">
    <NavBar />
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
        <p class="mt-4 text-gray-500">Loading application details...</p>
      </div>

      <div v-else-if="application" class="space-y-6">
        <!-- Header -->
        <div class="bg-white shadow rounded-2xl p-6 sm:p-8">
          <div class="flex justify-between items-start">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">{{ application.job_title }}</h1>
              <div class="mt-2 flex items-center text-gray-600">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
                <span class="text-lg">{{ application.company }}</span>
              </div>
              <div class="mt-4 flex gap-3">
                <span class="px-3 py-1 rounded-full text-sm font-medium" :class="getStatusColor(application.status)">
                  {{ application.status }}
                </span>
                <span class="px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-600">
                  Applied on {{ new Date(application.created_at).toLocaleDateString() }}
                </span>
              </div>
            </div>
            <div class="flex gap-2">
                <button @click="editResume" class="bg-indigo-50 text-indigo-700 hover:bg-indigo-100 px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                    Edit Resume
                </button>
                <a v-if="application.job_url" :href="application.job_url" target="_blank" class="border border-gray-300 text-gray-700 hover:bg-gray-50 px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2">
                    View Job Post
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                </a>
            </div>
          </div>
        </div>

        <!-- Job Description -->
        <div class="bg-white shadow rounded-2xl p-6 sm:p-8">
            <h2 class="text-xl font-bold text-gray-900 mb-4">Job Description</h2>
            <div class="prose max-w-none text-gray-600 whitespace-pre-wrap bg-gray-50 p-4 rounded-xl border border-gray-100">
                {{ application.jd_text || 'No job description provided.' }}
            </div>
        </div>

        <!-- Notes -->
        <div class="bg-white shadow rounded-2xl p-6 sm:p-8">
            <h2 class="text-xl font-bold text-gray-900 mb-4">Notes</h2>
            <div v-if="application.notes" class="prose max-w-none text-gray-600 whitespace-pre-wrap">
                {{ application.notes }}
            </div>
            <p v-else class="text-gray-500 italic">No notes added.</p>
        </div>
      </div>
      
      <div v-else class="text-center py-12">
        <p class="text-red-500">Application not found.</p>
        <router-link to="/dashboard" class="text-indigo-600 hover:underline mt-4 inline-block">Back to Dashboard</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../services/api';
import NavBar from '../components/NavBar.vue';

const route = useRoute();
const router = useRouter();
const application = ref(null);
const loading = ref(true);

onMounted(async () => {
    try {
        const response = await api.get(`/applications/${route.params.id}`);
        application.value = response.data;
    } catch (error) {
        console.error('Failed to fetch application details:', error);
    } finally {
        loading.value = false;
    }
});

const getStatusColor = (status) => {
    const colors = {
        'Drafting': 'bg-gray-100 text-gray-800',
        'Wishlist': 'bg-blue-100 text-blue-800',
        'Applied': 'bg-indigo-100 text-indigo-800',
        'Interviewing': 'bg-amber-100 text-amber-800',
        'Offer': 'bg-emerald-100 text-emerald-800',
        'Rejected': 'bg-red-100 text-red-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
};

const editResume = () => {
    router.push(`/editor/${application.value.id}`);
};
</script>
