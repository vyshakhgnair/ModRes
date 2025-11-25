import { defineStore } from 'pinia';
import api from '../services/api';

export const useApplicationStore = defineStore('application', {
    state: () => ({
        currentApplicationId: null,
        companyName: '',
        jobTitle: '',
        jobDescription: '',
        jobUrl: '',
        status: '',
        resumeText: '',
        tailoredData: null,
        latexCode: '',
        pdfUrl: null,
        isAnalyzing: false,
    }),

    actions: {
        setApplicationId(id) {
            this.currentApplicationId = id;
        },

        async fetchApplication(id) {
            try {
                const response = await api.get(`/applications/${id}`);
                const app = response.data;

                if (app) {
                    this.currentApplicationId = app.id;
                    this.companyName = app.company;
                    this.jobTitle = app.job_title;
                    this.jobDescription = app.jd_text; // Now we get the full JD text
                    this.jobUrl = app.job_url;
                    this.status = app.status;

                    if (app.resume) {
                        this.tailoredData = app.resume.json_data;
                        this.latexCode = app.resume.latex_code;
                        // We might want to store pdfUrl if we have a way to serve it
                        // For now, we can regenerate it in Workspace if needed, or just show "Ready to Create" if no PDF
                        // But if we have latexCode, Workspace can compile it.
                    }
                }
            } catch (error) {
                console.error('Error fetching application:', error);
            }
        },

        async initiateTailoring(company, title, jd, url) {
            this.isAnalyzing = true;
            try {
                const response = await api.post('/initiate-tailoring', {
                    company_name: company,
                    job_title: title,
                    job_description: jd,
                    job_url: url
                });

                this.currentApplicationId = response.data.application_id;
                this.companyName = company;
                this.jobTitle = title;
                this.jobDescription = jd;
                this.jobUrl = url;

                return response.data;
            } catch (error) {
                console.error('Error initiating tailoring:', error);
                throw error;
            } finally {
                this.isAnalyzing = false;
            }
        },

        async finalizeResume(tailoredData, score) {
            if (!this.currentApplicationId) return;

            try {
                const response = await api.post(`/application/${this.currentApplicationId}/finalize-resume`, {
                    tailored_data: tailoredData,
                    score: score
                });
                return response.data;
            } catch (error) {
                console.error('Error finalizing resume:', error);
                throw error;
            }
        },

        reset() {
            this.currentApplicationId = null;
            this.companyName = '';
            this.jobTitle = '';
            this.jobDescription = '';
            this.jobUrl = '';
            this.status = '';
            this.tailoredData = null;
            this.latexCode = '';
            this.pdfUrl = null;
        }
    }
});
