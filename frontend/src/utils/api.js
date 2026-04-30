import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000/api'
    : `${window.location.origin}/api`)

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000
})

export const uploadDocuments = async (questionFile, answerFile) => {
  const formData = new FormData()
  formData.append('question_file', questionFile)
  formData.append('answer_file', answerFile)
  
  return api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const getQuestions = async (sessionId) => {
  return api.get(`/questions/${sessionId}`)
}

export const uploadToBank = async (sessionId, questionIds) => {
  return api.post('/upload-to-bank', {
    session_id: sessionId,
    question_ids: questionIds
  })
}

export const getQuestionBank = async () => {
  return api.get('/bank')
}

export const removeFromBank = async (questionId) => {
  return api.delete(`/bank/${questionId}`)
}

export const clearBank = async () => {
  return api.delete('/bank')
}

export const composeDocuments = async (questionIds, title) => {
  return api.post('/compose', {
    question_ids: questionIds,
    title
  })
}

export const downloadDocument = async (sessionId, docType) => {
  return api.get(`/download/${sessionId}/${docType}`, {
    responseType: 'blob'
  })
}

export const deleteSession = async (sessionId) => {
  return api.delete(`/session/${sessionId}`)
}
