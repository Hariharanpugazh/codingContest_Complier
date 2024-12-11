import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Outlet } from 'react-router-dom';
import CreateContest from './pages/CreateContest';
import ContestPage from './pages/ContestPage';
import StartContest from './pages/StartContest';
import SelectTestOption from './pages/SelectTestOption';
import FileUpload from './pages/FileUpload';
import ManualSelectUI from './pages/ManualSelectUI';
import HrUpload from './pages/HrUploadPage';
import OnebyOne from './pages/OnebyOne';
import ManualPage from './pages/ManualPage';
import ContestDashboard from './pages/ContestDashboard';
import Login from './pages/staff/Login';
import Signup from './pages/staff/Signup';
import Dashboard from './pages/staff/Dashboard';
import GeneralHome from './pages/GeneralHome';
import StudentRegister from './pages/student/StudentRegister';
import StudentLogin from './pages/student/StudentLogin';
import StudentDashboard from './pages/student/StudentDashboard';
import StudentProfile from './pages/student/StudentProfile';
import Navbar from './pages/student/Navbar';
import StaffNavbar from './pages/staff/StaffNavbar';
import TestInstructions from './pages/student/TestInstruction';
import ViewContest from './pages/ViewContest';

// Layout component for wrapping student routes
const StudentLayout = () => (
  <>
    <Navbar />
    <Outlet /> {/* Render nested routes */}
  </>
);

// Layout component for wrapping staff routes
const StaffLayout = () => (
  <>
    <StaffNavbar />
    <Outlet /> {/* Render nested routes */}
  </>
);

function App() {
  const [studentId, setStudentId] = useState(null);

  return (
    <Router>
      <Routes>
        {/* General Home */}
        <Route path="/" element={<GeneralHome />} />

        {/* Student Routes */}
        <Route path="/StudentRegister" element={<StudentRegister />} />
        <Route path="/StudentLogin" element={<StudentLogin onLogin={setStudentId} />} />
        <Route element={<StudentLayout />}>
          <Route path="/studentdashboard" element={<StudentDashboard />} />
          <Route path="/studentprofile" element={<StudentProfile studentId={studentId} />} />
        </Route>

        {/* Staff Routes */}
        <Route path="/stafflogin" element={<Login />} />
        <Route path="/staffsignup" element={<Signup />} />
        <Route element={<StaffLayout />}>
          <Route path="/staffdashboard" element={<Dashboard />} />
          <Route path="/coding" element={<ContestDashboard />} />
          <Route path="/SelectTestOption" element={<SelectTestOption />} />
          <Route path="/FileUpload" element={<FileUpload />} />
          <Route path="/ManualSelectUI" element={<ManualSelectUI />} />
          <Route path="/HrUpload/:contestId" element={<HrUpload />} />
          <Route path="/OnebyOne" element={<OnebyOne />} />
          <Route path="/ManualPage/:contestId" element={<ManualPage />} />
          <Route path="/CreateContest" element={<CreateContest />} />
          <Route path="/StartContest" element={<StartContest />} />
          <Route path="/viewcontest/:contestId" element={<ViewContest />} />
        </Route>
        <Route path="/testinstructions/:testId" element={<TestInstructions />} />
        <Route path="/Contest/:testId" element={<ContestPage />} />

        {/* New View Contest Route */}
      </Routes>
    </Router>
  );
}

export default App;
