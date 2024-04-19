import React from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";
const ChoicesPage = () => {
  const navigate = useNavigate();

  const handleMentorClick = () => {
    navigate("/dashboard");
  };

  const handlePracticeQuestionsClick = () => {
    navigate("/practice-questions");
  };

  return (
    <div className="container">
      <div className="button-container">
        <button className="button" onClick={handleMentorClick}>
          24/7 mentor
        </button>
        <button className="button" onClick={handlePracticeQuestionsClick}>
          Practice Questions
        </button>
      </div>
    </div>
  );
};

export default ChoicesPage;
