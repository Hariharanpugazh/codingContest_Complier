import React, { useState } from 'react';
import { Button, Dialog, DialogTitle, DialogContent, DialogActions, Accordion, AccordionSummary, AccordionDetails, Typography } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import axios from 'axios';

const PreviewButton = ({ onEditProblem }) => {
  const [openPreview, setOpenPreview] = useState(false);
  const [previewData, setPreviewData] = useState({ easy: [], medium: [], hard: [] });

  const handlePreview = async () => {
    try {
      // Fetch problems data from the backend API
      const response = await axios.get('http://localhost:8000/manualProblems/');
      const questions = response.data.problems;

      // Group questions by difficulty level
      const easyQuestions = questions.filter((problem) => problem.level === "easy");
      const mediumQuestions = questions.filter((problem) => problem.level === "medium");
      const hardQuestions = questions.filter((problem) => problem.level === "hard");

      setPreviewData({ easy: easyQuestions, medium: mediumQuestions, hard: hardQuestions });
      setOpenPreview(true);
    } catch (error) {
      console.error("Failed to fetch preview data:", error);
    }
  };

  const handleClosePreview = () => {
    setOpenPreview(false);
  };

  // Function to handle delete
  const handleDelete = async (problemId) => {
    try {
      await axios.delete(`http://localhost:8000/manualProblems/`, { data: { id: problemId } });
      // Refresh the preview data after deletion
      handlePreview();
    } catch (error) {
      console.error("Failed to delete problem:", error);
    }
  };

  // Function to handle modify
  const handleModify = (problem) => {
    onEditProblem(problem); // Pass the problem data to the parent (ManualSelectUi.js)
    setOpenPreview(false);  // Close the preview dialog
  };

  return (
    <div>
      <Button variant="contained" color="secondary" onClick={handlePreview}>
        Preview
      </Button>

      {/* Preview Dialog */}
      <Dialog open={openPreview} onClose={handleClosePreview} fullWidth maxWidth="md">
        <DialogTitle>Preview Problems by Difficulty</DialogTitle>
        <DialogContent>
          {["easy", "medium", "hard"].map((level) => (
            <Accordion key={level} disabled={!previewData[level].length}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h6" sx={{ textTransform: "capitalize" }}>
                  {level} ({previewData[level].length})
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                {previewData[level].map((problem) => (
                  <div key={problem.id} style={{ marginBottom: '15px' }}>
                    <Typography variant="h6">{problem.title}</Typography>
                    <Typography variant="body1">{problem.problem_statement}</Typography>
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={() => handleModify(problem)}
                      style={{ marginRight: '10px', marginTop: '10px' }}
                    >
                      Modify
                    </Button>
                    <Button
                      variant="contained"
                      color="error"
                      onClick={() => handleDelete(problem.id)}
                      style={{ marginTop: '10px' }}
                    >
                      Delete
                    </Button>
                  </div>
                ))}
              </AccordionDetails>
            </Accordion>
          ))}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClosePreview} color="primary">Close</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default PreviewButton;
