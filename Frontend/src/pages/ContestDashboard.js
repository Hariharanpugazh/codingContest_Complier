import React from "react";
import OngoingTests from "../components/OngoingTests";
import UpcomingContests from "../components/UpcomingContests";
import CreateContest from "../components/CreateContest";

const ContestDashboard = () => {
  return (
    <div className="bg-gray-100 min-h-screen p-8 flex flex-col items-center">
      <h1 className="text-2xl font-bold text-gray-800 mb-8">Contest Dashboard</h1>
      <div className="w-full max-w-2xl space-y-8">
        <OngoingTests />
        <UpcomingContests />
        <CreateContest />
      </div>
    </div>
  );
};

export default ContestDashboard;
