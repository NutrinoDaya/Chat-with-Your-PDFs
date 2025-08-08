import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api', // proxy configured in vite.config.js to backend
  timeout: 15000,
});

export async function uploadPdf(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await apiClient.post('/pdf/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data; // expected to contain doc_id
}

export async function sendQuestion(docId, question) {
  const response = await apiClient.post('/chat/', {
    doc_id: docId,
    question,
  });
  return response.data; // expected to contain answer
}
