import api from '../api'

export const patientService = {
  authenticate: async (ssn: string, phone: string) => {
    return api.post('api/patients/auth', { ssn, phone });
  },
  
  checkin: async (ssn: string) => {
    return api.post('/patient/checkin', { ssn });
  },
  
  getDoctors: async () => {
    return api.get('/patient/doctors');
  },
  
  matchSymptoms: async (symptoms: string) => {
    return api.post('/patient/symptoms/match', { symptoms });
  }
};