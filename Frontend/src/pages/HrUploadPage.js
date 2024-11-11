import React, { useEffect, useState } from "react";
import axios from "axios";
import AddProblemSlide from "../components/AddProblemSlide";

function HrUpload() {
  const [questions, setQuestions] = useState([]);
  const [difficultyFilter, setDifficultyFilter] = useState("");
  const [isSlideOpen, setIsSlideOpen] = useState(false);

  useEffect(() => {
    fetchQuestions();
  }, []);

  const fetchQuestions = async () => {
    const response = await axios.get("http://127.0.0.1:8000/questions/");
    setQuestions(response.data.problems);
  };

  const handleModifyQuestion = (question) => {
    // This function will open a modification form in the future
    alert(`Modify question: ${question.title}`);
  };

  const handleDeleteQuestion = async (questionId) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/questions/${questionId}/`);
      fetchQuestions();
    } catch (error) {
      console.error("Error deleting question:", error);
    }
  };

  const filteredQuestions = questions.filter((q) =>
    difficultyFilter ? q.level === difficultyFilter : true
  );

  return (
    <div style={{ padding: "20px", maxWidth: "800px", margin: "auto" }}>
      <h1>Questions</h1>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "10px" }}>
        <span>Count: {filteredQuestions.length}</span>
        <button
          onClick={() => setIsSlideOpen(true)}
          style={{
            background: "blue",
            color: "white",
            borderRadius: "5px",
            padding: "5px 10px",
          }}
        >
          + Add Question
        </button>
      </div>
      <select
        onChange={(e) => setDifficultyFilter(e.target.value)}
        value={difficultyFilter}
        style={{ marginBottom: "20px", padding: "5px" }}
      >
        <option value="">Filter by difficulty</option>
        <option value="easy">Easy</option>
        <option value="medium">Medium</option>
        <option value="hard">Hard</option>
      </select>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ backgroundColor: "#f2f2f2" }}>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>S.No</th>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>Title</th>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>Difficulty</th>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredQuestions.map((question, index) => (
            <tr key={question.id}>
              <td style={{ border: "1px solid #ddd", padding: "8px", textAlign: "center" }}>{index + 1}</td>
              <td style={{ border: "1px solid #ddd", padding: "8px" }}>{question.title}</td>
              <td style={{ border: "1px solid #ddd", padding: "8px" }}>{question.level}</td>
              <td style={{ border: "1px solid #ddd", padding: "8px", textAlign: "center" }}>
                <button
                  onClick={() => handleModifyQuestion(question)}
                  style={{
                    background: "Green",
                    color: "white",
                    borderRadius: "5px",
                    padding: "5px 10px",
                    marginRight: "5px",
                  }}
                >
                  Modify
                </button>
                <button
                  onClick={() => handleDeleteQuestion(question.id)}
                  style={{
                    background: "red",
                    color: "white",
                    borderRadius: "5px",
                    padding: "5px 10px",
                  }}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      
      <AddProblemSlide isOpen={isSlideOpen} onClose={() => setIsSlideOpen(false)} />
    </div>
  );
}

export default HrUpload;