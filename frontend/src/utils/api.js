import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

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

export const composeDocuments = async (sessionId, questionIds, title, subject, totalScore) => {
  return api.post('/compose', {
    session_id: sessionId,
    question_ids: questionIds,
    title,
    subject,
    total_score: totalScore
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