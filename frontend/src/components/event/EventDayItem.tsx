import React from "react";
import { EventDay } from "../../types/Event";
import {
  ChevronRightIcon,
  UsersIcon,
} from "@heroicons/react/16/solid";
import { format, getISOWeek } from 'date-fns'
import { sv } from 'date-fns/locale'

interface EventDayItemProps {
  day: EventDay;
}

const EventDayItem: React.FC<EventDayItemProps> = ({ day }) => {
    const date = new Date(day.start_datetime)
    const dayOfWeekName = format(date, 'EEEE', { locale: sv });
    const weekNumber = getISOWeek(date);
    const formattedDate = format(date, 'dd MMMM', { locale: sv });
    const start_time = format(date, 'HH:MM', { locale: sv });
  return (

    <ul role="list" className="divide-y divide-gray-100">
      <li className="relative py-1 hover:bg-gray-50">
        <div className="px-4 sm:px-6 lg:px-2">
          <div className="mx-auto flex max-w-4xl justify-between gap-x-6">
            <div className="flex min-w-0 gap-x-4">
              <div className="min-w-0 flex-auto">
                <p className="text-sm/6 font-semibold text-gray-900">
                  <span className="absolute inset-x-0 -top-px bottom-0" />
                  {dayOfWeekName} - {formattedDate} (vecka {weekNumber})
                </p>
                <p className="mt-1 flex text-xs/5 text-gray-500">Samling {start_time}</p>
              </div>
            </div>
            <div className="flex shrink-0 items-center gap-x-4">
              <div className="hidden sm:flex sm:flex-col sm:items-end">
                <p className="text-sm/6 text-gray-900"></p>
                <UsersIcon className="w-4 h-4 text-slate-600 " />
                {day.registration_count}
              </div>
              <ChevronRightIcon
                aria-hidden="true"
                className="size-5 flex-none text-gray-400"
              />
            </div>
          </div>
        </div>
      </li>
    </ul>
  );
};

export default EventDayItem;
