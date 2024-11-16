import React from "react";

const OngoingTests = () => {
  const tests = ["CodingContest 1", "CodingContest 2", "CodingContest 3"];

  return (
    <div className="p-4 bg-white shadow rounded-lg">
      <h2 className="text-lg font-semibold mb-2 text-gray-800">Ongoing Tests</h2>
      <div className="grid grid-cols-2 gap-4">
        {tests.map((test, index) => (
          <div
            key={index}
            className="bg-blue-200 p-8 rounded-lg flex items-center justify-center text-blue-800 font-medium text-center shadow hover:bg-blue-300 transition duration-200"
          >
            {test}
          </div>
        ))}
      </div>
    </div>
  );
};

export default OngoingTests;
