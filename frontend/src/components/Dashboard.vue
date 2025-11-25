<template>
  <div class="min-h-screen bg-gray-50 font-sans">
    <NavBar />
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">My Applications</h1>
        <p class="text-gray-600 mt-2">Track all your job applications in one place</p>
      </div>

      <div v-if="Object.keys(groupedApplications).length > 0" class="space-y-8">
        <div v-for="(apps, date) in groupedApplications" :key="date">
            <h3 class="text-lg font-semibold text-gray-700 mb-3">{{ date }}</h3>
            <div class="bg-white shadow overflow-hidden sm:rounded-md">
                <ul role="list" class="divide-y divide-gray-200">
                <li v-for="app in apps" :key="app.id">
                    <div class="block hover:bg-gray-50 transition cursor-pointer" @click="goToDetails(app.id)">
                    <div class="px-4 py-4 sm:px-6">
                        <div class="flex items-center justify-between">
                        <p class="text-sm font-medium text-indigo-600 truncate">
                            {{ app.job_title }}
                        </p>
                        <div class="ml-2 flex-shrink-0 flex items-center gap-3">
                            <p class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="getStatusColor(app.status)">
                            {{ app.status }}
                            </p>
                            <button @click.stop="deleteApplication(app)" class="text-gray-400 hover:text-red-600 transition-colors p-1 rounded-full hover:bg-red-50">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                            </button>
                        </div>
                        </div>
                        <div class="mt-2 sm:flex sm:justify-between">
                        <div class="sm:flex">
                            <p class="flex items-center text-sm text-gray-500">
                            <svg class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
                            {{ app.company }}
                            </p>
                        </div>
                        <div class="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                            <svg class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                            <p>
                            Applied on <time :datetime="app.created_at">{{ new Date(app.created_at).toLocaleDateString() }}</time>
                            </p>
                        </div>
                        </div>
                    </div>
                    </div>
                </li>
                </ul>
            </div>
        </div>
      </div>
      
      <div v-else class="text-center py-12 bg-white rounded-lg shadow">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No applications</h3>
        <p class="mt-1 text-sm text-gray-500">Get started by creating a new resume.</p>
        <div class="mt-6">
            <router-link to="/" class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
            New Resume
            </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import NavBar from './NavBar.vue';

const applications = ref([]);
const router = useRouter();

const loadApplications = async () => {
    try {
        const response = await api.getApplications();
        applications.value = response.data;
    } catch (error) {
        console.error('Failed to fetch applications:', error);
    }
};

onMounted(loadApplications);

const groupedApplications = computed(() => {
    const groups = {};
    applications.value.forEach(app => {
        const date = new Date(app.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
        if (!groups[date]) {
            groups[date] = [];
        }
        groups[date].push(app);
    });
    return groups;
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

const deleteApplication = async (app) => {
    if (!confirm(`Are you sure you want to delete the application for ${app.company}?`)) return;
    
    try {
        await api.delete(`/applications/${app.id}`);
        await loadApplications();
    } catch (error) {
        console.error('Failed to delete application:', error);
        alert('Failed to delete application');
    }
};

const goToDetails = (id) => {
    router.push(`/application/${id}`);
};
</script>
