// src/components/huntingYear/HuntingYearSelector.tsx

import React from "react";
import { HuntingYear } from "../../types/HuntingYear";

interface HuntingYearSelectorProps {
  huntingYears: HuntingYear[];
  selectedYear: number | null;
  onYearSelect: (year: number) => void;
}

const HuntingYearSelector: React.FC<HuntingYearSelectorProps> = ({
  huntingYears,
  selectedYear,
  onYearSelect,
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const year = parseInt(e.target.value, 10);
    if (!isNaN(year)) {
      onYearSelect(year);
    }
  };

  return (
    <div className="flex items-center">
      <label htmlFor="huntingYear" className="mr-2 font-medium">
        Select Hunting Year:
      </label>
      <select
        id="huntingYear"
        value={selectedYear || ""}
        onChange={handleChange}
        className="border border-gray-300 rounded px-3 py-2"
      >
        {huntingYears.map((year) => (
          <option key={year.id} value={year.year}>
            {year.year} {year.is_current ? "(Current)" : ""}
          </option>
        ))}
      </select>
    </div>
  );
};

export default HuntingYearSelector;
