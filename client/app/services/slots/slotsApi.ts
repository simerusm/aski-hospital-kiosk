import api from '../api'

export const slotsService = {
    getSlots: async () => {
        return await api.get('/api/dev/get/slots');
    },

    deleteSlot: async (slotId: number) => {
        console.log(slotId)
        return await api.delete(`/api/slots/delete/slot/${slotId}`);
    }
}