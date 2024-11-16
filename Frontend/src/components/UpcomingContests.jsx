import React from "react";

const UpcomingContests = () => {
  const contests = ["JavaScript Mastery", "Algorithm Challenge"];

  return (
    <div className="p-4 bg-white shadow rounded-lg">
      <h2 className="text-lg font-semibold mb-2 text-gray-800">Upcoming Tests</h2>
      <div className="grid grid-cols-2 gap-4">
        {contests.map((contest, index) => (
          <div
            key={index}
            className="bg-green-200 p-8 rounded-lg flex items-center justify-center text-green-800 font-medium text-center shadow hover:bg-green-300 transition duration-200"
          >
            {contest}
          </div>
        ))}
      </div>
    </div>
  );
};

export default UpcomingContests;
