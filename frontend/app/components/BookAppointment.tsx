'use client'

import React, { useState, useEffect, useCallback } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import { fetchAvailableSlots } from '../utils/api';
import { TimeSlot } from '../types/timeSlot';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { cn } from "../utils/utils";

const localizer = momentLocalizer(moment); // Ensure localizer is defined

function Button({ className, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2",
        className
      )}
      {...props}
    />
  );
}

function formatEvents(slots: TimeSlot[]) {
  return slots.map(slot => ({
    title: `${slot.slot_type.charAt(0).toUpperCase() + slot.slot_type.slice(1)} (ID: ${slot.slot_id})`,
    start: new Date(slot.start_time),
    end: new Date(slot.end_time),
    resource: slot
  }));
}

export default function AppointmentCalendar() {
  const [events, setEvents] = useState<any[]>([]);
  const [currentDate, setCurrentDate] = useState(new Date());

  const loadEvents = useCallback(async (start: Date, end: Date) => {
    const slots = await fetchAvailableSlots(start, end);
    const formattedEvents = formatEvents(slots);
    setEvents(formattedEvents);
  }, []);

  useEffect(() => {
    const start = moment(currentDate).startOf('week').toDate();
    const end = moment(currentDate).endOf('week').toDate();
    loadEvents(start, end);
  }, [currentDate, loadEvents]);

  const handleNavigate = (action: 'PREV' | 'NEXT' | 'TODAY') => {
    if (action === 'PREV') {
      setCurrentDate(moment(currentDate).subtract(1, 'week').toDate());
    } else if (action === 'NEXT') {
      setCurrentDate(moment(currentDate).add(1, 'week').toDate());
    } else {
      setCurrentDate(new Date());
    }
  };

  return (
    <div className="flex flex-col h-[600px] w-full max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-4">
        <Button onClick={() => handleNavigate('PREV')}>
          <ChevronLeft className="mr-2 h-4 w-4" /> Previous Week
        </Button>
        <Button onClick={() => handleNavigate('TODAY')}>Today</Button>
        <Button onClick={() => handleNavigate('NEXT')}>
          Next Week <ChevronRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
      <div className="flex-grow">
        <Calendar
          localizer={localizer}
          events={events}
          startAccessor="start"
          endAccessor="end"
          defaultView={Views.WEEK}
          views={['week']}
          date={currentDate}
          onNavigate={(newDate) => setCurrentDate(newDate)}
          formats={{
            timeGutterFormat: (date, culture, localizer) =>
              localizer.format(date, 'HH:mm', culture),
            eventTimeRangeFormat: ({ start, end }, culture, localizer) =>
              `${localizer.format(start, 'HH:mm', culture)} - ${localizer.format(end, 'HH:mm', culture)}`,
          }}
          min={new Date(0, 0, 0, 8, 0, 0)}
          max={new Date(0, 0, 0, 20, 0, 0)}
          className="bg-white shadow-lg rounded-lg overflow-hidden"
        />
      </div>
    </div>
  );
} 