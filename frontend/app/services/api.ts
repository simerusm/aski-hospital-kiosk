import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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

export const queueService = {
  joinQueue: async (doctorId: number, patientId: number) => {
    return api.post('/queue/join', { doctor_id: doctorId, patient_id: patientId });
  },
  
  getQueueStatus: async (doctorId: number) => {
    return api.get(`/queue/status/${doctorId}`);
  }
};