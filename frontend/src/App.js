// import logo from './logo.svg';
import React from 'react';
import './App.css';
import "bootstrap/dist/css/bootstrap.min.css"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Auth from "./Auth"
import "bootstrap/dist/css/bootstrap.min.css";
import OTPVerification from "./OTPVerification";
import Dashboard from './Dashboard';
import ChoicesPage from "./choicesPage";
import PracticeQuestions from "./PracticeQuestions";
import Descriptive from "./descriptive";
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Auth />} />
        <Route path="/verify-otp" element={<OTPVerification />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/choices" element={<ChoicesPage/>} />
        <Route path="/practice-questions" element={<PracticeQuestions />} />
        <Route path="/descriptive" element={<Descriptive/>} />
      </Routes>
    </BrowserRouter>
  )
  
}

export default App;
