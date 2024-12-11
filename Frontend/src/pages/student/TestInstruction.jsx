import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Button, Typography, Box, Paper } from "@mui/material";
import { styled } from "@mui/material/styles";
import axios from "axios";

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  maxWidth: 700,
  width: "100%",
  backgroundColor: theme.palette.background.default,
  boxShadow: theme.shadows[3],
  borderRadius: theme.shape.borderRadius,
}));

const StyledButton = styled(Button)(({ theme }) => ({
  marginTop: theme.spacing(3),
  padding: theme.spacing(1.5, 4),
  fontSize: "1rem",
  fontWeight: "bold",
  color: theme.palette.primary.contrastText,
  backgroundColor: theme.palette.primary.main,
  '&:hover': {
    backgroundColor: theme.palette.primary.dark,
  },
}));

const startTest = async (contestId, studentId) => {
  try {
    const response = await axios.post('http://localhost:8000/api/start_test/', {
      contest_id: contestId,
      student_id: studentId,
    });
    console.log(response.data.message);
  } catch (error) {
    console.error("Error starting test:", error);
  }
};

const TestInstructions = () => {
  const navigate = useNavigate();
  const { testId } = useParams(); // Get test ID from route params

  const handleStartTest = async () => {
    const studentId = localStorage.getItem("studentId"); // Retrieve student ID
    if (!studentId) {
      alert("Student ID not found. Please log in again.");
      return;
    }

    await startTest(testId, studentId); // Log test as started
    navigate(`/contest/${testId}`); // Navigate to the contest page
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      minHeight="100vh"
      padding={2}
      bgcolor="background.paper"
    >
      <StyledPaper>
        <Typography variant="h4" gutterBottom align="center" color="textPrimary">
          Test Instructions
        </Typography>
        <Typography variant="body1" paragraph color="textSecondary">
          Please read the following instructions carefully before starting the test:
        </Typography>
        <Typography variant="body2" paragraph color="textSecondary">
          1. Ensure you have a stable internet connection.
        </Typography>
        <Typography variant="body2" paragraph color="textSecondary">
          2. The test is timed and will automatically submit when the time is up.
        </Typography>
        <Typography variant="body2" paragraph color="textSecondary">
          3. Do not refresh the page during the test.
        </Typography>
        <Typography variant="body2" paragraph color="textSecondary">
          4. Make sure to save your answers frequently.
        </Typography>
        <Typography variant="body2" paragraph color="textSecondary">
          5. Contact support if you face any issues.
        </Typography>
        <Box display="flex" justifyContent="center">
          <StyledButton variant="contained" onClick={handleStartTest}>
            Start Test
          </StyledButton>
        </Box>
      </StyledPaper>
    </Box>
  );
};

export default TestInstructions;
