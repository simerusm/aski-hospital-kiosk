'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import { slotsService } from '../services/slots/slotsApi';
import { TimeSlot } from '../types/timeSlot';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import Button from '../components/Button';
import { CalendarEvent } from '../types/calendarEvent';
import Modal from '../components/Modal';
import PageWrapper from '../components/PageWrapper';

const localizer = momentLocalizer(moment);

// Function to format events for the calendar
function formatEvents(slots: TimeSlot[]): CalendarEvent[] {
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
  const [selectedSlot, setSelectedSlot] = useState<TimeSlot | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Function to load events from API
  const loadEvents = useCallback(async () => {
    try {
      const response = await slotsService.getSlots();
      const slots: TimeSlot[] = response.data.response;

      const formattedEvents = formatEvents(slots);
      setEvents(formattedEvents);
    } catch (error) {
      console.error('Failed to load slots:', error);
    }
  }, []);

  useEffect(() => {
    loadEvents();
  }, [currentDate, loadEvents]);

  // Handle navigation between weeks
  const handleNavigate = (action: 'PREV' | 'NEXT' | 'TODAY') => {
    if (action === 'PREV') {
      setCurrentDate(moment(currentDate).subtract(1, 'week').toDate());
    } else if (action === 'NEXT') {
      setCurrentDate(moment(currentDate).add(1, 'week').toDate());
    } else {
      setCurrentDate(new Date());
    }
  };

  // Handle clicking an event to open the modal
  const handleSelectEvent = (event: CalendarEvent) => {
    setSelectedSlot(event.resource);
    setIsModalOpen(true);
  };

  // Function to handle slot deletion
  const handleDeleteSlot = async () => {
    if (selectedSlot) {
      try {
        await slotsService.deleteSlot(selectedSlot.slot_id);
        setIsModalOpen(false);
        loadEvents();
      } catch (error) {
        console.error('Failed to delete slot:', error);
      }
    }
  };

  return (
    <PageWrapper>
      <div className="flex flex-col h-[90vh] w-full md:h-[90vh] md:w-[70vw] max-w-7xl mx-auto text-black">
        <div className="flex flex-col space-y-4 mb-6 p-5 text-black">
          {/* Current month/year display */}
          <div className="text-center text-black">
            <div className="text-3xl font-bold text-black">
              {moment(currentDate).format('MMMM YYYY')}
            </div>
          </div>
          
          {/* Navigation controls */}
          <div className="flex justify-center items-center space-x-4">
            <Button 
              onClick={() => handleNavigate('PREV')}
              className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            >
              <ChevronLeft className="h-7 w-7" />
            </Button>
            <Button 
              onClick={() => handleNavigate('TODAY')}
              className="px-4 py-2 text-xl font-medium"
            >
              Today
            </Button>
            <Button 
              onClick={() => handleNavigate('NEXT')}
              className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            >
              <ChevronRight className="h-7 w-7" />
            </Button>
          </div>
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
            onSelectEvent={handleSelectEvent}
            formats={{
              timeGutterFormat: (date, culture, localizer) =>
                localizer!.format(date, 'hh:mm A', culture),
              eventTimeRangeFormat: ({ start, end }, culture, localizer) =>
                `${localizer!.format(start, 'hh:mm A', culture)} - ${localizer!.format(end, 'hh:mm A', culture)}`,
              dayFormat: (date, culture, localizer) =>
                localizer!.format(date, 'ddd DD/MM', culture),
            }}
            min={new Date(0, 0, 0, 8, 0, 0)}
            max={new Date(0, 0, 0, 20, 0, 0)}
            toolbar={false}
            className="bg-white shadow-lg rounded-lg overflow-hidden text-black font-sans border border-gray-200"
            components={{
              week: {
                header: ({ date }) => (
                  <span className="font-medium text-gray-700">
                    {moment(date).format('ddd DD/MM')}
                  </span>
                ),
              },
            }}
          />
        </div>

        {/* Modal Component */}
        <Modal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          slotDetails={selectedSlot}
          handleDeleteSlot={handleDeleteSlot}
        />
      </div>
    </PageWrapper>
  );
}