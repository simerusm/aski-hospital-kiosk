import api from '../api'

export const slotsService = {
    getSlots: async () => {
        return api.get('/api/dev/get/slots'); // Fetch all slots from the backend
    }
}