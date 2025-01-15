'use client' // interface used in client-side component, use client needed

import { TimeSlot } from './timeSlot';

export interface CalendarEvent {
  title: string;
  start: Date;
  end: Date;
  resource: TimeSlot;
}