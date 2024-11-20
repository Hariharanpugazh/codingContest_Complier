
import React, { useState, useEffect } from "react";
import axios from "axios";

const ContestDashboard = () => {
  const [contests, setContests] = useState([]);

  useEffect(() => {
    const fetchContests = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/contests/");
        setContests(response.data); // Array of contest objects
      } catch (error) {
        console.error("Error fetching contests:", error);
      }
    };

    fetchContests();
  }, []);

  const deleteContest = async (contestId) => {
    const confirmation = window.confirm(
      `Are you sure you want to delete the contest with ID ${contestId}?`
    );
    if (!confirmation) return;

    try {
      const response = await axios.delete(
        `http://localhost:8000/api/contests/delete/${contestId}/`
      );
      if (response.status === 200) {
        alert(response.data.message);
        setContests((prevContests) =>
          prevContests.filter((contest) => contest.contest_id !== contestId)
        );
      }
    } catch (error) {
      console.error("Error deleting contest:", error);
      alert("Failed to delete contest. Please try again.");
    }
  };

  return (
    <div className="bg-gray-100 min-h-screen p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Contest Dashboard</h1>
        <button
          onClick={() => (window.location.href = "/createcontest")}
          className="bg-yellow-400 text-gray-800 px-4 py-2 rounded-lg shadow hover:bg-yellow-500"
        >
          + Create Test
        </button>
      </div>

      <div className="grid grid-cols-3 gap-8">
        {contests.map((contest) => (
          <div
            key={contest.contest_id}
            className="p-4 bg-white shadow-lg rounded-lg hover:shadow-xl transition relative"
          >
            <h2 className="text-xl font-semibold mb-2 text-gray-800">
              {contest.contest_name}
            </h2>
            <p className="text-gray-600">
              <strong>Start Time:</strong>{" "}
              {contest.start_time ? contest.start_time : "N/A"}
            </p>
            <p className="text-gray-600">
              <strong>End Time:</strong>{" "}
              {contest.end_time ? contest.end_time : "N/A"}
            </p>
            <p className="text-gray-600">
              <strong>Organization Type:</strong> {contest.organization_type}
            </p>
            <p className="text-gray-600">
              <strong>Organization Name:</strong> {contest.organization_name}
            </p>
            <p className="text-gray-600">
              <strong>Type:</strong> {contest.testType}
            </p>
            <button
              onClick={() => deleteContest(contest.contest_id)}
              className="absolute top-2 right-2 bg-red-500 text-white px-3 py-1 rounded-full hover:bg-red-600 shadow-md"
            >
              Remove
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ContestDashboard;