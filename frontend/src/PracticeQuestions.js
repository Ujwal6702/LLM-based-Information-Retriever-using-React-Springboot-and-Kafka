import React from 'react';
import './Textbook.css';
import { useNavigate } from "react-router-dom";

const Textbook = () => {
    const navigate = useNavigate();
    const handleMCQClick = () => {
        // Navigate to the MCQ page or perform any action
        console.log("Clicked MCQ");
      };
    
      const handleDescriptiveClick = () => {
        // Navigate to the Descriptive page or perform any action
        navigate("/descriptive")
      };
    return (
        <div className="container">
          <div className="box mcq" onClick={handleMCQClick}>
            MCQ
          </div>
          <div className="box descriptive" onClick={handleDescriptiveClick}>
            Descriptive
          </div>
        </div>
      );
    };
  
  export default Textbook;