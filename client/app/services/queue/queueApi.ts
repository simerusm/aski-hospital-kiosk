import api from '../api'

export const queueService = {
    joinQueue: async (doctorId: number, patientId: number) => {
      return api.post('/queue/join', { doctor_id: doctorId, patient_id: patientId });
    },
    
    getQueueStatus: async (doctorId: number) => {
      return api.get(`/queue/status/${doctorId}`);
    }
};