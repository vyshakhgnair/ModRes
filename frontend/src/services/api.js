import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
    withCredentials: true, // Important for session cookies
    headers: {
        'Content-Type': 'application/json',
    },
});

export default {
    parseResume(file) {
        const formData = new FormData();
        formData.append('resume', file);
        return api.post('/parse-resume', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
    },
    analyzeGap(resumeText, jdText) {
        return api.post('/analyze-gap', { resume_text: resumeText, jd_text: jdText });
    },
    scoreResume(resumeText, jdText) {
        return api.post('/score-resume', { resume_text: resumeText, jd_text: jdText });
    },
    generatePdf(data) {
        return api.post('/generate-pdf', data, {
            responseType: 'blob',
        });
    },
    tailorResume(resumeText, jdText, userAnswers) {
        return api.post('/tailor-resume', {
            resume_text: resumeText,
            jd_text: jdText,
            user_answers: userAnswers
        });
    },
    compileLatex(latexCode) {
        return api.post('/compile-latex', { latex_code: latexCode }, {
            responseType: 'blob',
        });
    },
    login(email, password) {
        return api.post('/auth/login', { email, password });
    },
    register(email, password) {
        return api.post('/auth/register', { email, password });
    },
    me() {
        return api.get('/auth/me');
    },
    logout() {
        return api.post('/auth/logout');
    },
    getApplications() {
        return api.get('/applications');
    },
    // Phase 2: Profile & Auto-Apply
    getProfile() {
        return api.get('/profile');
    },
    updateProfile(profileData) {
        return api.post('/profile', profileData);
    },
    createApplication(appData) {
        return api.post('/applications', appData);
    },
    updateApplication(appData) {
        return api.post('/applications', appData);
    },
    triggerAutoApply(jobUrl, applicationId, headless = false) {
        return api.post('/auto-apply', {
            job_url: jobUrl,
            application_id: applicationId,
            headless: headless
        });
    },
    // Convenience methods
    get(url) {
        return api.get(url);
    },
    post(url, data) {
        return api.post(url, data);
    },
    delete(url) {
        return api.delete(url);
    }
};
