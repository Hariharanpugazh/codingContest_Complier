import React, { useState, useEffect } from 'react';
import { Button, Typography, Box, Dialog, DialogActions, DialogContent, DialogTitle, Card, CardContent, CardActions, Grid, Menu, MenuItem } from '@mui/material';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import CreateIcon from '@mui/icons-material/Create';

const HrUpload = () => {
  const [questions, setQuestions] = useState([]);
  const [deleteConfirm, setDeleteConfirm] = useState(false);
  const [selectedQuestionId, setSelectedQuestionId] = useState(null);
  const [anchorEl, setAnchorEl] = useState(null);
  const navigate = useNavigate();

  // Fetch questions from tempQuestions
  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await axios.get('http://localhost:8000/manualProblems/');
        setQuestions(response.data.problems);
      } catch (error) {
        console.error('Failed to fetch questions:', error);
      }
    };
    fetchQuestions();
  }, []);

  const handleModify = (question) => {
    navigate('/manualSelectUI', { state: { question } });
  };

  const handleDelete = async (questionId) => {
    try {
      await axios.delete('http://localhost:8000/manualProblems/', { data: { id: questionId } });
      setQuestions(questions.filter(q => q.id !== questionId));
      setDeleteConfirm(false);
    } catch (error) {
      console.error("Failed to delete question:", error);
    }
  };

  const handleUploadClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleBulkUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append("file", file);
      
      // Get CSRF token from the cookie
      const csrfToken = Cookies.get('csrftoken');
      
      axios.post('http://localhost:8000/userinput/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-CSRFToken': csrfToken  // Add CSRF token to headers
        },
        withCredentials: true,  // Include credentials to ensure cookies are sent
      })
      .then(response => {
        console.log("Bulk upload successful:", response.data);
        setQuestions(prevQuestions => [...prevQuestions, ...response.data.problems]);
      })
      .catch(error => console.error("Bulk upload failed:", error));
    }
  };
  const handleManualUpload = () => {
    navigate('/manualSelectUI');
    handleMenuClose();
  };

  return (
    <Box p={4}>
      <Typography variant="h4" align="center" gutterBottom style={{ fontWeight: 'bold', marginBottom: '20px' }}>
        HR Upload
      </Typography>

      <Box display="flex" justifyContent="center" mb={4}>
        <Button 
          variant="contained" 
          color="primary" 
          onClick={handleUploadClick}
          style={{
            backgroundColor: '#1976d2',
            color: '#fff',
            padding: '10px 20px',
            fontWeight: 'bold',
            fontSize: '1rem',
            borderRadius: '25px',
            transition: 'background-color 0.3s, transform 0.2s',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
          }}
          onMouseEnter={(e) => e.target.style.backgroundColor = '#1565c0'}
          onMouseLeave={(e) => e.target.style.backgroundColor = '#1976d2'}
        >
          Upload
        </Button>
        <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleMenuClose}>
          <MenuItem 
            onClick={() => document.getElementById('bulk-upload-input').click()}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              fontSize: '1rem',
              padding: '10px 20px',
              fontWeight: 'bold',
              color: '#1976d2',
              transition: 'color 0.3s',
            }}
          >
            <UploadFileIcon /> Bulk Upload
          </MenuItem>
          <MenuItem 
            onClick={handleManualUpload} 
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              fontSize: '1rem',
              padding: '10px 20px',
              fontWeight: 'bold',
              color: '#1976d2',
              transition: 'color 0.3s',
            }}
          >
            <CreateIcon /> Manual Upload
          </MenuItem>
        </Menu>
        <input
          type="file"
          id="bulk-upload-input"
          accept=".csv"
          style={{ display: 'none' }}
          onChange={handleBulkUpload}
        />
      </Box>

      <Grid container spacing={3}>
        {questions.map((question) => (
          <Grid item xs={12} sm={6} md={4} key={question.id}>
            <Card
              variant="outlined"
              style={{
                borderRadius: '10px',
                transition: 'transform 0.2s',
                boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
              }}
              onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
              onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
            >
              <CardContent>
                <Typography variant="h6" style={{ fontWeight: 'bold' }}>
                  {question.title}
                </Typography>
                <Typography variant="body2" color="textSecondary" style={{ marginTop: '10px' }}>
                  {question.problem_statement}
                </Typography>
              </CardContent>
              <CardActions style={{ justifyContent: 'space-between', padding: '16px' }}>
                <Button 
                  variant="contained" 
                  color="primary" 
                  onClick={() => handleModify(question)}
                  style={{ fontSize: '0.875rem', fontWeight: 'bold' }}
                >
                  Modify
                </Button>
                <Button 
                  variant="contained" 
                  color="error" 
                  onClick={() => { setSelectedQuestionId(question.id); setDeleteConfirm(true); }}
                  style={{ fontSize: '0.875rem', fontWeight: 'bold' }}
                >
                  Delete
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
      
      <Dialog open={deleteConfirm} onClose={() => setDeleteConfirm(false)}>
        <DialogTitle style={{ fontWeight: 'bold' }}>Confirm Deletion</DialogTitle>
        <DialogContent>
          <Typography>Are you sure you want to delete this question?</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteConfirm(false)} color="primary" variant="outlined">
            Cancel
          </Button>
          <Button onClick={() => handleDelete(selectedQuestionId)} color="error" variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default HrUpload;
