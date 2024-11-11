import React, { useState, useEffect } from 'react';
import { TextField, Button, Typography, Box, Grid, IconButton, Select, MenuItem, InputLabel, FormControl, ListItemText, Checkbox } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';

// Define available roles (can be customized or fetched from an API if needed)
const availableRoles = ["Junior Software Developer", "Senior Software Developer", "AI Developer", "Project Manager"];

const ManualSelectUI = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const initialQuestionData = location.state?.question || {
    title: '',
    problem_statement: '',
    samples: [],
    hidden_samples: [],
    role: [],
    level: '',
  };

  const [questionData, setQuestionData] = useState(initialQuestionData);
  const [testCases, setTestCases] = useState(
    initialQuestionData.samples.map(sample => ({
      ...sample,
      input: sample.input || ['']  // Ensure input is an array with at least one element
    }))
  );
  const [hiddenTestCases, setHiddenTestCases] = useState(
    initialQuestionData.hidden_samples.map(hiddenSample => ({
      ...hiddenSample,
      input: hiddenSample.input || ['']  // Ensure input is an array with at least one element
    }))
  );

  useEffect(() => {
    if (!questionData.id) navigate('/hrUpload'); // Redirect if no question data is provided
  }, [questionData, navigate]);

  const handleSave = async () => {
    try {
      const updatedQuestion = {
        ...questionData,
        samples: testCases,
        hidden_samples: hiddenTestCases,
      };
      await axios.put('http://localhost:8000/manualProblems/', { problems: [updatedQuestion] });
      navigate('/hrUpload');
    } catch (error) {
      console.error("Failed to save question:", error);
    }
  };

  const handleRoleChange = (event) => {
    setQuestionData({ ...questionData, role: event.target.value });
  };

  const handleAddTestCase = (isHidden = false) => {
    if (isHidden) {
      setHiddenTestCases([...hiddenTestCases, { input: [''], output: '' }]);
    } else {
      setTestCases([...testCases, { input: [''], output: '' }]);
    }
  };

  const handleRemoveTestCase = (index, isHidden = false) => {
    if (isHidden) {
      const updatedHiddenTestCases = [...hiddenTestCases];
      updatedHiddenTestCases.splice(index, 1);
      setHiddenTestCases(updatedHiddenTestCases);
    } else {
      const updatedTestCases = [...testCases];
      updatedTestCases.splice(index, 1);
      setTestCases(updatedTestCases);
    }
  };

  return (
    <Box p={3}>
      <Typography variant="h4" align="center" gutterBottom>
        Edit Question
      </Typography>
      <Grid container spacing={4}>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Title"
            variant="outlined"
            margin="normal"
            value={questionData.title}
            onChange={(e) => setQuestionData({ ...questionData, title: e.target.value })}
          />
          <TextField
            fullWidth
            label="Description"
            variant="outlined"
            margin="normal"
            multiline
            rows={3}
            value={questionData.problem_statement}
            onChange={(e) => setQuestionData({ ...questionData, problem_statement: e.target.value })}
          />
        </Grid>

        {/* Role Selection */}
        <Grid item xs={12}>
          <FormControl fullWidth variant="outlined" margin="normal">
            <InputLabel>Roles</InputLabel>
            <Select
              multiple
              value={questionData.role}
              onChange={handleRoleChange}
              renderValue={(selected) => selected.join(', ')}
              label="Roles"
            >
              {availableRoles.map((role) => (
                <MenuItem key={role} value={role}>
                  <Checkbox checked={questionData.role.includes(role)} />
                  <ListItemText primary={role} />
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      {/* Test Cases Section */}
      <Box mt={2}>
        <Typography variant="h6">Test Cases</Typography>
        {testCases.map((testCase, index) => (
          <Box key={index} mb={2}>
            <Typography variant="subtitle1">Test Case {index + 1}</Typography>
            {testCase.input.map((input, inputIndex) => (
              <TextField
                key={inputIndex}
                fullWidth
                label={`Input ${inputIndex + 1}`}
                variant="outlined"
                margin="normal"
                value={input}
                onChange={(e) => {
                  const updatedTestCases = [...testCases];
                  updatedTestCases[index].input[inputIndex] = e.target.value;
                  setTestCases(updatedTestCases);
                }}
              />
            ))}
            <TextField
              fullWidth
              label="Output"
              variant="outlined"
              margin="normal"
              value={testCase.output}
              onChange={(e) => {
                const updatedTestCases = [...testCases];
                updatedTestCases[index].output = e.target.value;
                setTestCases(updatedTestCases);
              }}
            />
            <IconButton onClick={() => handleRemoveTestCase(index)} color="error">
              <RemoveIcon />
            </IconButton>
          </Box>
        ))}
        <Button onClick={() => handleAddTestCase(false)} variant="contained" color="success">
          Add Test Case
        </Button>
      </Box>

      {/* Hidden Test Cases Section */}
      <Box mt={2}>
        <Typography variant="h6">Hidden Test Cases</Typography>
        {hiddenTestCases.map((hiddenTestCase, index) => (
          <Box key={index} mb={2}>
            <Typography variant="subtitle1">Hidden Test Case {index + 1}</Typography>
            {hiddenTestCase.input.map((input, inputIndex) => (
              <TextField
                key={inputIndex}
                fullWidth
                label={`Hidden Input ${inputIndex + 1}`}
                variant="outlined"
                margin="normal"
                value={input}
                onChange={(e) => {
                  const updatedHiddenTestCases = [...hiddenTestCases];
                  updatedHiddenTestCases[index].input[inputIndex] = e.target.value;
                  setHiddenTestCases(updatedHiddenTestCases);
                }}
              />
            ))}
            <TextField
              fullWidth
              label="Hidden Output"
              variant="outlined"
              margin="normal"
              value={hiddenTestCase.output}
              onChange={(e) => {
                const updatedHiddenTestCases = [...hiddenTestCases];
                updatedHiddenTestCases[index].output = e.target.value;
                setHiddenTestCases(updatedHiddenTestCases);
              }}
            />
            <IconButton onClick={() => handleRemoveTestCase(index, true)} color="error">
              <RemoveIcon />
            </IconButton>
          </Box>
        ))}
        <Button onClick={() => handleAddTestCase(true)} variant="contained" color="success">
          Add Hidden Test Case
        </Button>
      </Box>
      
      <Box mt={4}>
        <Button variant="contained" color="primary" onClick={handleSave}>
          Save
        </Button>
      </Box>
    </Box>
  );
};

export default ManualSelectUI;
