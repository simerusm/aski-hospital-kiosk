import React from "react";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  slotDetails: {
    start_time: string;
    end_time: string;
    doctor_id: number;
    slot_type: string;
  } | null;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, slotDetails }) => {
  if (!isOpen || !slotDetails) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center text-black">
      <div className="bg-white p-6 rounded shadow-lg w-96">
        <h2 className="text-xl font-semibold mb-4">Slot Details</h2>
        <p><strong>Start Time:</strong> {new Date(slotDetails.start_time).toLocaleString()}</p>
        <p><strong>End Time:</strong> {new Date(slotDetails.end_time).toLocaleString()}</p>
        <p><strong>Doctor ID:</strong> {slotDetails.doctor_id}</p>
        <p><strong>Type:</strong> {slotDetails.slot_type}</p>

        <div className="flex justify-end mt-4">
          <button onClick={onClose} className="px-4 py-2 bg-gray-500 text-white rounded">
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default Modal;