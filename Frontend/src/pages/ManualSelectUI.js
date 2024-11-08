import React, { useState } from 'react';
import { TextField, MenuItem, Button, Grid, Box, Typography, IconButton, Select, Checkbox, ListItemText, InputLabel, FormControl } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axios from 'axios';
import PreviewButton from '../components/previewButton';

const roles = ["Junior Developer", "Senior Developer", "AI Developer"];

const ProblemForm = () => {
  const [testCases, setTestCases] = useState([{ inputs: [''], output: '' }]);
  const [hiddenTestCases, setHiddenTestCases] = useState([{ inputs: [''], output: '' }]);
  const [selectedRoles, setSelectedRoles] = useState([]);
  const [problemData, setProblemData] = useState({
    id: '',
    title: '',
    description: '',
    level: '',
  });

  // Function to load problem data for modification
  const loadProblemData = (problem) => {
    setProblemData({
      id: problem.id || '',
      title: problem.title || '',
      description: problem.problem_statement || '',
      level: problem.level ? problem.level.charAt(0).toUpperCase() + problem.level.slice(1) : '',
    });

    setSelectedRoles(problem.role || []);

    // Safely set test cases, ensuring each has the necessary structure
    setTestCases(
      problem.samples && Array.isArray(problem.samples) && problem.samples.length > 0
        ? problem.samples.map(testCase => ({
            inputs: testCase.input ? [...testCase.input] : [''], // Ensuring inputs is an array
            output: testCase.output || ''
          }))
        : [{ inputs: [''], output: '' }]
    );

    // Safely set hidden test cases, ensuring each has the necessary structure
    setHiddenTestCases(
      problem.hidden_samples && Array.isArray(problem.hidden_samples) && problem.hidden_samples.length > 0
        ? problem.hidden_samples.map(hiddenTestCase => ({
            inputs: hiddenTestCase.input ? [...hiddenTestCase.input] : [''], // Ensuring inputs is an array
            output: hiddenTestCase.output || ''
          }))
        : [{ inputs: [''], output: '' }]
    );
  };

  const handleAddTestCase = (isHidden = false) => {
    const cases = isHidden ? hiddenTestCases : testCases;
    const newCases = [...cases, { inputs: [''], output: '' }];
    isHidden ? setHiddenTestCases(newCases) : setTestCases(newCases);
  };

  const handleAddInputField = (testCaseIndex, isHidden = false) => {
    const cases = isHidden ? hiddenTestCases : testCases;
    const updatedCases = [...cases];
    updatedCases[testCaseIndex].inputs.push('');
    isHidden ? setHiddenTestCases(updatedCases) : setTestCases(updatedCases);
  };

  const handleRemoveInputField = (testCaseIndex, inputIndex, isHidden = false) => {
    const cases = isHidden ? hiddenTestCases : testCases;
    const updatedCases = [...cases];
    updatedCases[testCaseIndex].inputs = updatedCases[testCaseIndex].inputs.filter((_, idx) => idx !== inputIndex);
    isHidden ? setHiddenTestCases(updatedCases) : setTestCases(updatedCases);
  };

  const handleRoleChange = (event) => {
    setSelectedRoles(event.target.value);
  };

  const handleProblemDataChange = (field, value) => {
    setProblemData((prevData) => ({ ...prevData, [field]: value }));
  };

  const saveProblemAsJson = async () => {
    const problemJson = {
      problems: [
        {
          id: parseInt(problemData.id, 10),
          title: problemData.title,
          role: selectedRoles,
          level: problemData.level.toLowerCase(),
          problem_statement: problemData.description,
          samples: testCases.map((testCase) => ({
            input: testCase.inputs.map(input => `${input}`),
            output: `${testCase.output}`
          })),
          hidden_samples: hiddenTestCases.map((hiddenTestCase) => ({
            input: hiddenTestCase.inputs.map(input => `${input}`),
            output: `${hiddenTestCase.output}`
          }))
        }
      ]
    };

    try {
      const response = await axios.post('http://localhost:8000/manualProblems/', problemJson);
      toast.success(response.data.message, {
        position: "top-right",
        autoClose: 3000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
      });
    } catch (error) {
      console.error('Failed to save problem data:', error);
      toast.error('Failed to save problem data.', {
        position: "top-right",
        autoClose: 3000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
      });
    }
  };

  return (
    <Box p={3} bgcolor="#f9f9f9" borderRadius={2} boxShadow={3} maxWidth="90%" mx="auto">
      <Typography variant="h4" align="center" gutterBottom>
        Problem Form
      </Typography>
      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="ID"
            type="number"
            variant="outlined"
            margin="normal"
            value={problemData.id}
            onChange={(e) => handleProblemDataChange('id', e.target.value)}
          />
          <TextField
            fullWidth
            label="Problem"
            variant="outlined"
            margin="normal"
            value={problemData.title}
            onChange={(e) => handleProblemDataChange('title', e.target.value)}
          />
          <TextField
            fullWidth
            label="Description"
            variant="outlined"
            margin="normal"
            multiline
            rows={3}
            value={problemData.description}
            onChange={(e) => handleProblemDataChange('description', e.target.value)}
          />
          <Box mt={2}>
            <Typography variant="h6">Test Cases</Typography>
            {testCases && testCases.map((testCase, testCaseIndex) => (
              <Box key={testCaseIndex} mb={2} p={2} border="1px solid #ddd" borderRadius={1}>
                <Typography variant="subtitle1" gutterBottom>
                  Test Case {testCaseIndex + 1}
                </Typography>
                {testCase.inputs && testCase.inputs.map((input, inputIndex) => (
                  <Box display="flex" alignItems="center" key={inputIndex}>
                    <TextField
                      fullWidth
                      label={`Input ${inputIndex + 1}`}
                      variant="outlined"
                      margin="normal"
                      value={input}
                      onChange={(e) => {
                        const updatedCases = [...testCases];
                        updatedCases[testCaseIndex].inputs[inputIndex] = e.target.value;
                        setTestCases(updatedCases);
                      }}
                    />
                    {inputIndex === testCase.inputs.length - 1 && (
                      <IconButton
                        onClick={() => handleAddInputField(testCaseIndex)}
                        color="success"
                        sx={{ ml: 1 }}
                      >
                        <AddIcon />
                      </IconButton>
                    )}
                    {inputIndex > 0 && (
                      <IconButton
                        onClick={() => handleRemoveInputField(testCaseIndex, inputIndex)}
                        color="error"
                        sx={{ ml: 1 }}
                      >
                        <RemoveIcon />
                      </IconButton>
                    )}
                  </Box>
                ))}
                <TextField
                  fullWidth
                  label="Output"
                  variant="outlined"
                  margin="normal"
                  value={testCase.output}
                  onChange={(e) => {
                    const updatedCases = [...testCases];
                    updatedCases[testCaseIndex].output = e.target.value;
                    setTestCases(updatedCases);
                  }}
                />
                {testCaseIndex === testCases.length - 1 && (
                  <Button
                    onClick={() => handleAddTestCase(false)}
                    variant="contained"
                    color="success"
                    sx={{
                      mt: 1,
                      px: 2,
                      ':hover': { backgroundColor: '#66bb6a' },
                      fontSize: '0.8rem',
                    }}
                  >
                    Add Test Case
                  </Button>
                )}
              </Box>
            ))}
          </Box>
        </Grid>

        <Grid item xs={12} md={6}>
          <FormControl fullWidth variant="outlined" margin="normal">
            <InputLabel>Roles</InputLabel>
            <Select
              multiple
              value={selectedRoles}
              onChange={handleRoleChange}
              label="Roles"
              renderValue={(selected) => selected.join(', ')}
            >
              {roles.map((role) => (
                <MenuItem key={role} value={role}>
                  <Checkbox checked={selectedRoles.indexOf(role) > -1} />
                  <ListItemText primary={role} />
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          
          <TextField
            fullWidth
            select
            label="Difficulty"
            variant="outlined"
            margin="normal"
            value={problemData.level}
            onChange={(e) => handleProblemDataChange('level', e.target.value)}
          >
            <MenuItem value="Easy">Easy</MenuItem>
            <MenuItem value="Medium">Medium</MenuItem>
            <MenuItem value="Hard">Hard</MenuItem>
          </TextField>
          <Box mt={2}>
            <Typography variant="h6">Hidden Test Cases</Typography>
            {hiddenTestCases && hiddenTestCases.map((hiddenTestCase, hiddenTestCaseIndex) => (
              <Box key={hiddenTestCaseIndex} mb={2} p={2} border="1px solid #ddd" borderRadius={1}>
                <Typography variant="subtitle1" gutterBottom>
                  Hidden Test Case {hiddenTestCaseIndex + 1}
                </Typography>
                {hiddenTestCase.inputs && hiddenTestCase.inputs.map((input, inputIndex) => (
                  <Box display="flex" alignItems="center" key={inputIndex}>
                    <TextField
                      fullWidth
                      label={`Hidden Input ${inputIndex + 1}`}
                      variant="outlined"
                      margin="normal"
                      value={input}
                      onChange={(e) => {
                        const updatedCases = [...hiddenTestCases];
                        updatedCases[hiddenTestCaseIndex].inputs[inputIndex] = e.target.value;
                        setHiddenTestCases(updatedCases);
                      }}
                    />
                    {inputIndex === hiddenTestCase.inputs.length - 1 && (
                      <IconButton
                        onClick={() => handleAddInputField(hiddenTestCaseIndex, true)}
                        color="success"
                        sx={{ ml: 1 }}
                      >
                        <AddIcon />
                      </IconButton>
                    )}
                    {inputIndex > 0 && (
                      <IconButton
                        onClick={() => handleRemoveInputField(hiddenTestCaseIndex, inputIndex, true)}
                        color="error"
                        sx={{ ml: 1 }}
                      >
                        <RemoveIcon />
                      </IconButton>
                    )}
                  </Box>
                ))}
                <TextField
                  fullWidth
                  label="Hidden Output"
                  variant="outlined"
                  margin="normal"
                  value={hiddenTestCase.output}
                  onChange={(e) => {
                    const updatedCases = [...hiddenTestCases];
                    updatedCases[hiddenTestCaseIndex].output = e.target.value;
                    setHiddenTestCases(updatedCases);
                  }}
                />
                {hiddenTestCaseIndex === hiddenTestCases.length - 1 && (
                  <Button
                    onClick={() => handleAddTestCase(true)}
                    variant="contained"
                    color="success"
                    sx={{
                      mt: 1,
                      px: 2,
                      ':hover': { backgroundColor: '#66bb6a' },
                      fontSize: '0.8rem',
                    }}
                  >
                    Add Hidden Test Case
                  </Button>
                )}
              </Box>
            ))}
          </Box>
        </Grid>
      </Grid>
      
      <Box display="flex" justifyContent="space-between" mt={4}>
        <Button variant="contained" onClick={saveProblemAsJson} color="primary">
          Save
        </Button>
        <PreviewButton onEditProblem={loadProblemData} />
      </Box>

      <ToastContainer />
    </Box>
  );
};

export default ProblemForm;