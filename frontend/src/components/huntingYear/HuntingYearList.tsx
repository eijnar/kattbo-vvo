// src/components/huntingYear/HuntingYearList.tsx

import React from "react";
import { HuntingYear } from "../../types/HuntingYear";
import HuntingYearSelector from "./HuntingYearSelector";

interface HuntingYearListProps {
  huntingYears: HuntingYear[];
  selectedYear: number | null;
  onYearSelect: (year: number) => void;
}

const HuntingYearList: React.FC<HuntingYearListProps> = ({
  huntingYears,
  selectedYear,
  onYearSelect,
}) => {
  return (
    <div className="mb-6">
      <HuntingYearSelector
        huntingYears={huntingYears}
        selectedYear={selectedYear}
        onYearSelect={onYearSelect}
      />
    </div>
  );
};

export default HuntingYearList;
