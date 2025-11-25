<template>
  <div class="min-h-screen bg-gray-50">
    <NavBar />
    <div class="py-8 px-4">
    <div class="max-w-4xl mx-auto">
      <div class="bg-white rounded-2xl shadow-lg p-8">
        <div class="flex items-center gap-4 mb-8">
          <div class="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
          </div>
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Profile</h1>
            <p class="text-gray-500">Manage your application autofill settings</p>
          </div>
        </div>

        <form @submit.prevent="saveProfile" class="space-y-6">
          <!-- Basic Info -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Full Name</label>
              <input v-model="profile.full_name" type="text" class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent" placeholder="John Doe">
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Email</label>
              <input v-model="profile.email" type="email" class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent" placeholder="john@example.com">
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Phone</label>
              <input v-model="profile.phone" type="tel" class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent" placeholder="+1 (555) 123-4567">
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Work Authorization</label>
              <select v-model="profile.work_auth_status" class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                <option value="">Select...</option>
                <option value="Citizen">US Citizen</option>
                <option value="Green Card">Green Card</option>
                <option value="H1B">H1B Visa</option>
                <option value="OPT">OPT</option>
                <option value="Requires Sponsorship">Requires Sponsorship</option>
              </select>
            </div>
          </div>

          <!-- Links -->
          <div class="space-y-4">
            <h3 class="text-lg font-semibold text-gray-900">Professional Links</h3>
            <div class="grid grid-cols-1 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">LinkedIn URL</label>
                <input v-model="profile.linkedin_url" type="url" class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent" placeholder="https://linkedin.com/in/johndoe">
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">GitHub URL</label>
                <input v-model="profile.github_url" type="url" class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent" placeholder="https://github.com/johndoe">
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Portfolio URL</label>
                <input v-model="profile.portfolio_url" type="url" class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent" placeholder="https://johndoe.com">
              </div>
            </div>
          </div>

          <!-- Compliance -->
          <div class="space-y-4">
            <h3 class="text-lg font-semibold text-gray-900">Compliance (Optional)</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Disability Status</label>
                <select v-model="profile.disability_status" class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                  <option value="">Prefer not to answer</option>
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Veteran Status</label>
                <select v-model="profile.veteran_status" class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                  <option value="">Prefer not to answer</option>
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>
            </div>
          </div>

          <div class="flex gap-4 pt-6">
            <button type="submit" :disabled="saving" class="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:opacity-50">
              {{ saving ? 'Saving...' : 'Save Profile' }}
            </button>
            <router-link to="/dashboard" class="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors font-semibold">
              Cancel
            </router-link>
          </div>
        </form>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';
import { useRouter } from 'vue-router';
import NavBar from '../components/NavBar.vue';

const router = useRouter();
const saving = ref(false);
const profile = ref({
  full_name: '',
  email: '',
  phone: '',
  linkedin_url: '',
  github_url: '',
  portfolio_url: '',
  work_auth_status: '',
  disability_status: '',
  veteran_status: ''
});

onMounted(async () => {
  try {
    const response = await api.get('/profile');
    if (response.data) {
      profile.value = { ...profile.value, ...response.data };
    }
  } catch (error) {
    console.error('Error loading profile:', error);
  }
});

const saveProfile = async () => {
  saving.value = true;
  try {
    await api.post('/profile', profile.value);
    alert('Profile saved successfully!');
    router.push('/dashboard');
  } catch (error) {
    console.error('Error saving profile:', error);
    alert('Failed to save profile');
  } finally {
    saving.value = false;
  }
};
</script>
