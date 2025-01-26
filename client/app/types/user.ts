'use client'

export interface User {
    id: number;
    name: string;
    ssn: string;
    phone: string;
    checkin_status?: boolean;
}