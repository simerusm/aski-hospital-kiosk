"use client"

import React from "react"
import { QRCodeSVG } from "qrcode.react"
import { CalendarIcon, ClockIcon, UserIcon, MapPinIcon } from "lucide-react"
import PageWrapper from "../components/PageWrapper"

import { useSearchParams } from "next/navigation";

function getExactDate(dateTimeString: string | null): string {
    if (!dateTimeString) return "Invalid date";

    const date = new Date(dateTimeString);
    if (isNaN(date.getTime())) return "Invalid date";

    return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric"
    });
}

export function ConfirmationPage() {
  const searchParams = useSearchParams();
  
  // Retrieve values from URL parameters
  const startTime = searchParams.get("start_time");
  const endTime = searchParams.get("end_time");
  const doctorId = searchParams.get("doctor_id");
  const slotType = searchParams.get("slot_type");
  const qrCodeData = JSON.stringify({startTime, endTime, doctorId, slotType})

  return (
    <PageWrapper>
      <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-lg">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">Appointment Confirmed</h2>
          <p className="mt-2 text-sm text-gray-600">
            Your appointment has been successfully booked. Please find the details below.
          </p>
        </div>
        <div className="mt-8 space-y-6">
          <div className="flex items-center space-x-3">
            <UserIcon className="h-5 w-5 text-indigo-500" aria-hidden="true" />
            <span className="text-sm font-medium text-gray-900">{doctorId}</span>
          </div>
          <div className="flex items-center space-x-3">
            <CalendarIcon className="h-5 w-5 text-indigo-500" aria-hidden="true" />
            <span className="text-sm font-medium text-gray-900">{getExactDate(startTime)}</span>
          </div>
          <div className="flex items-center space-x-3">
            <ClockIcon className="h-5 w-5 text-indigo-500" aria-hidden="true" />
            <span className="text-sm font-medium text-gray-900">{startTime}</span>
          </div>
          <div className="flex items-center space-x-3">
            <MapPinIcon className="h-5 w-5 text-indigo-500" aria-hidden="true" />
            <span className="text-sm font-medium text-gray-900">{slotType}</span>
          </div>
        </div>
        <div className="mt-8 flex justify-center">
          <QRCodeSVG value={qrCodeData} size={200} />
        </div>
        <div className="mt-4 text-center">
          <p className="text-sm text-gray-600">Please show this QR code when you arrive for your appointment.</p>
        </div>
      </div>
    </PageWrapper>
  )
}