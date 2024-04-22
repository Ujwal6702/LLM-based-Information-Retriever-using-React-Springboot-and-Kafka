import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css"; 

export default function OTPVerification( request_id) {
  const navigate = useNavigate();
  const [otp, setOTP] = useState(["", "", "", "", "", ""]); // Array to hold each digit of OTP
  const inputRefs = useRef([]); // Refs to manage focus between input boxes
  const [verificationError, setVerificationError] = useState(null);

  // Function to handle changes in OTP input boxes
  const handleChange = (index, value) => {
    if (value.length > 1) {
      return; // Prevent entering more than one character in each box
    }

    const newOTP = [...otp];
    newOTP[index] = value;
    setOTP(newOTP);

    // Move focus to the next input box
    if (value && index < 5) {
      inputRefs.current[index + 1].focus();
    }
  };

  // Backspace key
  const handleKeyDown = (index, event) => {
    if (event.key === "Backspace" && index > 0 && !otp[index]) {
      // If Backspace is pressed and the current box is empty, move focus to the previous box
      inputRefs.current[index - 1].focus();
    }
  };

  // Function to handle form submission (e.g., OTP validation)
  const handleSubmit = async (event) => {
    event.preventDefault();
    navigate("/Dashboard")
    // Validate the OTP (for demo purposes, just navigate to success page)
    const enteredOTP = otp.join("");
    
    console.log(request_id.reqid, enteredOTP)
    fetch("http://localhost:8080/verify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ requestId: request_id.reqid, otp: enteredOTP }),
    })
      .then((response) => {
       if (!response.ok) {
          throw new Error("OTP verification failed");
        }
      return response.json();
    })
     .then((data) => {
      navigate("/");
    })
     .catch((error) => {
      console.error("Error verifying OTP", error);
      setVerificationError("OTP verification failed. Please try again");
    });
  };

  
  const otpInputs = Array.from({ length: 6 }, (_, index) => (
    <input
      key={index}
      type="text"
      maxLength={1}
      value={otp[index]}
      onChange={(e) => handleChange(index, e.target.value)}
      onKeyDown={(e) => handleKeyDown(index, e)}
      ref={(el) => (inputRefs.current[index] = el)}
      className="otp-input"
    />
  ));

  return (
    <div className="OTP-verification-container">
      <h3 className="Auth-form-title">Enter OTP</h3>
      <form onSubmit={handleSubmit} className="Auth-form-content">
        <div className="otpContainer">{otpInputs}</div>
        <button type="submit" className="btn btn-primary mt-3">
          Verify OTP
        </button>
        {verificationError && <p style={{color: "red"}}>{verificationError}</p>} 
        
      </form>
    </div>
  );
}