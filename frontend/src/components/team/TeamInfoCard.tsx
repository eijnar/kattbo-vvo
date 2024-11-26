import React from "react";

const TeamInfoCard: React.FC = () => {
  return (
    <div>
      <div className="pb-2">
        <h3 className="text-base/7 font-semibold text-gray-900 text-center">
          Allmän information
        </h3>
        <p className="mt-1 max-w-2xl text-sm/6 text-gray-500">
          Information kring jaktledare, tilldelning och antal deltagare för
          angivet år
        </p>
      </div>
      <div className="border-t border-gray-100">
        <dl className="divide-y divide-gray-100">
          <div className="py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm/6 font-bold text-gray-900">
              Ordinarie jaktledare
            </dt>
            <dd className="mt-1 text-sm/6 font-bold text-gray-700 sm:col-span-2 sm:mt-0">
              Johan Andersson
            </dd>
          </div>
          <div className="py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm/6 font-medium text-gray-900">
              Biträdande jaktledare
            </dt>
            <dd className="mt-1 text-sm/6 text-gray-700 sm:col-span-2 sm:mt-0">
              Mats Johansson
            </dd>
          </div>
          <div className=" py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm/6 font-medium text-gray-900">Tilldelning</dt>
            <dd className="mt-1 text-sm/6 text-gray-700 sm:col-span-2 sm:mt-0">
              6 oxar | 3 kor | 8 kalvar
            </dd>
          </div>
        </dl>
      </div>
    </div>
  );
};

export default TeamInfoCard;
