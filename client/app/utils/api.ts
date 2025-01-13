import { TimeSlot } from '../types/timeSlot'

export async function fetchAvailableSlots(start: Date, end: Date): Promise<TimeSlot[]> {
  const response = await fetch(`/api/available-slots?start=${start.toISOString()}&end=${end.toISOString()}`)
  if (!response.ok) {
    throw new Error('Failed to fetch available slots')
  }
  return response.json()
}