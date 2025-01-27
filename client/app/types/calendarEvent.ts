'use client'

import { TimeSlot } from './timeSlot';

export interface CalendarEvent {
  title: string;
  start: Date;
  end: Date;
  resource: TimeSlot;
}