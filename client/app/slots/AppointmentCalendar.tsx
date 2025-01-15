'use client'

import React, { useState, useEffect, useCallback } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import { slotsService } from '../services/slots/slotsApi';
import { TimeSlot } from '../types/timeSlot';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import Button from '../components/Button';
import { CalendarEvent } from '../types/calendarEvent';

const localizer = momentLocalizer(moment);

function formatEvents(slots: TimeSlot[]) {
    return slots.map(slot => ({
      title: "",
      start: new Date(slot.start_time),
      end: new Date(slot.end_time),
      resource: slot,
    }));
  }

export default function AppointmentCalendar() {
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [currentDate, setCurrentDate] = useState(new Date());

  const loadEvents = useCallback(async () => {
    const response = await slotsService.getSlots();
    const slots = response.data.response;
    
    const formattedEvents = formatEvents(slots);
    setEvents(formattedEvents);
  }, []);

  useEffect(() => {
    // const start = moment(currentDate).startOf('week').toDate();
    // const end = moment(currentDate).endOf('week').toDate();
    loadEvents();
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
              localizer!.format(date, 'HH:mm', culture),
            eventTimeRangeFormat: ({ start, end }, culture, localizer) =>
              `${localizer!.format(start, 'HH:mm', culture)} - ${localizer!.format(end, 'HH:mm', culture)}`,
            dayFormat: (date, culture, localizer) =>
                localizer!.format(date, 'ddd DD/MM', culture),
          }}
          min={new Date(0, 0, 0, 8, 0, 0)}
          max={new Date(0, 0, 0, 20, 0, 0)}
          toolbar={false}
          components={{
            week: {
              header: ({ date }) => (
                <span>{moment(date).format('ddd DD/MM')}</span>
              ),
            },
          }}
          className="bg-white shadow-lg rounded-lg overflow-hidden text-black font-sans"
        />
      </div>
    </div>
  );
}