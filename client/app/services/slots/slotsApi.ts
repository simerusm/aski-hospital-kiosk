import api from '../api'

export const slotsService = {
    getSlots: async () => {
        return await api.get('/api/dev/get/slots'); // Fetch all slots from the backend
    }
}