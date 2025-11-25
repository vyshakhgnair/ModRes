import { createRouter, createWebHistory } from 'vue-router';
import Workspace from './components/Workspace.vue';
import Login from './components/Login.vue';
import Register from './components/Register.vue';
import Dashboard from './components/Dashboard.vue';
import Profile from './views/Profile.vue';
import JobTracker from './views/JobTracker.vue';
import ApplicationDetails from './views/ApplicationDetails.vue';
import api from './services/api';

const routes = [
    { path: '/editor/:applicationId?', component: Workspace, meta: { requiresAuth: true } },
    { path: '/', redirect: '/editor' },
    { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
    { path: '/application/:id', component: ApplicationDetails, meta: { requiresAuth: true } },
    { path: '/profile', component: Profile, meta: { requiresAuth: true } },
    { path: '/tracker', component: JobTracker, meta: { requiresAuth: true } },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
    if (to.meta.requiresAuth) {
        try {
            // Check if user is authenticated
            await api.me();
            next();
        } catch (error) {
            next('/login');
        }
    } else {
        next();
    }
});

export default router;
