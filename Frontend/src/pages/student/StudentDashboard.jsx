import React, { useState, useEffect } from "react";
import { Tabs, Tab, AppBar, Typography, Box, Container } from "@mui/material";
import { styled } from "@mui/system";
import TestCard from "./TestCard";
import axios from "axios";
import NoExams from "../../assets/happy.png";

// Custom styling for tabs to match Dashboard color schema
const StyledTabs = styled(Tabs)({
  "& .MuiTabs-indicator": {
    backgroundColor: "#D97706", // Yellow underline for active tab
  },
});

const StyledTab = styled(Tab)({
  textTransform: "none",
  fontSize: "16px",
  fontWeight: "bold",
  color: "#1E293B", // Dark Gray text for tabs
  "&.Mui-selected": {
    color: "#D97706", // Yellow for the selected tab
  },
});

const StudentDashboard = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [openTests, setOpenTests] = useState([]);
  const [studentData, setStudentData] = useState({
    name: "",
    regno: "",
  });

  // Fetch student data and tests
  const fetchStudentData = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/student/profile/", {
        withCredentials: true, // Include cookies for authentication
      });

      const { name, regno } = response.data;
      setStudentData({ name, regno });

      // Fetch open tests using the student's registration number
      fetchOpenTests(regno);
    } catch (error) {
      console.error("Error fetching student data:", error);
    }
  };

  const fetchOpenTests = async (regno) => {
    try {
      const response = await axios.get(`http://localhost:8000/api/student/tests?regno=${regno}`, {
        withCredentials: true, // Include cookies for authentication
      });
      setOpenTests(response.data); // Expected to return contests visible to this student
    } catch (error) {
      console.error("Error fetching open tests:", error);
    }
  };

  useEffect(() => {
    fetchStudentData();
  }, []);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <Container maxWidth="lg">
        <AppBar position="static" color="transparent" elevation={0} className="mb-8">
          <Typography variant="h4" className="font-bold text-gray-900">
            Hi! {studentData.name}
          </Typography>
          <Typography variant="subtitle1" className="text-gray-600">
            Registration Number: {studentData.regno}
          </Typography>
        </AppBar>

        <Box className="bg-white p-6">
          <StyledTabs value={activeTab} onChange={handleTabChange}>
            <StyledTab label="Assigned to you" />
            <StyledTab label="Completed/Closed" />
          </StyledTabs>

          <Box className="mt-8">
            {activeTab === 0 && (
              <Box>
                {openTests.length > 0 ? (
                  openTests.map((test) => <TestCard key={test._id} test={test} />)
                ) : (
                  <Box className="text-center">
                    <img
                      src={NoExams}
                      alt="No Exams"
                      className="mx-auto mb-4"
                      style={{ width: "300px", height: "300px" }}
                    />
                    <Typography variant="h6" className="font-medium text-gray-900">
                      Any day is a good day when <br /> there are no exams!
                    </Typography>
                  </Box>
                )}
              </Box>
            )}
            {activeTab === 1 && (
              <Typography
                variant="h6"
                className="font-medium text-gray-900 text-center"
              >
                Feature Coming Soon!
              </Typography>
            )}
          </Box>
        </Box>
      </Container>
    </div>
  );
};

export default StudentDashboard;
