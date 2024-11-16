import React from "react";
import { useNavigate} from "react-router-dom";

const CreateContest = () => {
  const navigate = useNavigate();
  const handleCreate = () => {
    alert("Create a new contest!");
    navigate('/CreateContest')
  };

  return (
    <div className="p-4 bg-white shadow rounded-lg">
      <h2 className="text-lg font-semibold mb-2 text-gray-800">Create Test</h2>
      <div
        onClick={handleCreate}
        className="bg-yellow-200 p-8 rounded-lg flex items-center justify-center text-yellow-800 font-bold text-3xl cursor-pointer shadow hover:bg-yellow-300 transition duration-200"
      >
        +
      </div>
    </div>
  );
};

export default CreateContest;
