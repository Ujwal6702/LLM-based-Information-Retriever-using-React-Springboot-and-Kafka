import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import OTPVerification from "./OTPVerification";
import Dashboard from "./Dashboard";

export default function Auth() {
  const navigate = useNavigate();
  const [authMode, setAuthMode] = useState("signin");
  const [otp, setOTP] = useState(false);
  const [reqid, setReqId] = useState(false);
  const [dashb, setDashb] = useState(false);
  
  const changeAuthMode = () => {
    setAuthMode(authMode === "signin" ? "signup" : "signin");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    // Perform authentication logic here (e.g., validate credentials)
    //CREATE FETCH API : IF ITS YES GO TO DASHBOARD USING AUTHENTICATION
    // For demo purposes, navigate to OTP verification upon successful authentication
    if( authMode === "signup") {
      const formData = new FormData(event.target);
      const name = formData.get("name");
      const email = formData.get("email");
      const password = formData.get("password");

      // Assuming you have an endpoint to send the data
      const url = "http://localhost:8080/register";
      const data = {
        email,
        name,
        password
      };
      console.log(JSON.stringify(data), url)
      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
        });
    
        if (response.ok) {
          console.log("here")
          // If the response is successful, parse the response JSON
          const responseData = await response.json();
          // Assuming responseData contains message and requestId
          const { message, request_id } = responseData;
          setReqId(request_id)
          // Handle the message and requestId as needed
          console.log("Response message:", message);
          console.log("Request ID:", request_id);
          
          // For demo purposes, navigate to OTP verification upon successful authentication
          if (authMode === "signup") {
            setOTP(true);
          }
        } else {
          // Handle error cases here
          alert("User already exists! Please sign in.")
          console.error("Error:", response.statusText);
        }
      } catch (error) {
        // Handle fetch error
        console.error("Fetch error:", error);
      }
    }
    else {
      const formData = new FormData(event.target);
      const email = formData.get("email");
      const password = formData.get("password");

      // Assuming you have an endpoint to send the data
      const url = "http://localhost:8080/login";
      const data = {
        email,
        password
      };
      console.log(JSON.stringify(data), url)
      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          // If the response is successful, parse the response JSON
          const responseData = await response.json();
          // Assuming responseData contains message and requestId
          const message = responseData["auth"];
          localStorage.setItem('auth_key_llm', message)
          localStorage.setItem('email_llm', email)
          console.log("Response message:", message);
          console.log("Request ID:", email);
          setDashb(true);
          // navigate("/dashboard")

        } else {
          // Handle error cases here
          console.error("Error:", response.statusText);
        }
      } catch (error) {
        // Handle fetch error
        console.error("Fetch error:", error);
      }
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      // Check if auth_key is present in localStorage
      const email = localStorage.getItem("email_llm");
      const auth = localStorage.getItem("auth_key_llm");
      if (auth && email) {
        try {
          const response = await fetch('http://localhost:8080/auth', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, auth }),
          });
          if (response.ok) {
            console.log('Authenticated successfully!');
            setDashb(true);
          } else {
            const data = await response.json(); // Parse error response
            console.log('Authentication failed:', data.error);
            // Handle error as needed
          }
        } catch (error) {
          console.error('Error:', error);
          console.log('An error occurred while authenticating.');
          // Handle error as needed
        }
      }
    };
  
    fetchData(); // Call the async function
  }, []);


  if (dashb) {
    return <Dashboard />;
  }
  if (authMode=="signup" && otp) {
    console.log(reqid)
    return <OTPVerification {...{reqid}} />;
  }

  return (
    <div className="Auth-form-container">
      <form className="Auth-form" onSubmit={handleSubmit}>
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">{authMode === "signin" ? "Sign In" : "Sign Up"}</h3>
          <div className="text-center">
            {authMode === "signin" ? (
              <p>
                Not registered yet?{" "}
                <span className="link-primary" onClick={changeAuthMode}>
                  Sign Up
                </span>
              </p>
            ) : (
              <p>
                Already registered?{" "}
                <span className="link-primary" onClick={changeAuthMode}>
                  Sign In
                </span>
              </p>
            )}
          </div>
          {authMode === "signup" && (
            <div className="form-group mt-3">
              <label>Full Name</label>
              <input type="text" className="form-control mt-1" placeholder="e.g. Jane Doe" name = "name" />
            </div>
          )}
          <div className="form-group mt-3">
            <label>Email address</label>
            <input type="email" className="form-control mt-1" placeholder="Enter email" name = "email" />
          </div>
          <div className="form-group mt-3">
            <label>Password</label>
            <input type="password" className="form-control mt-1" placeholder="Enter password" name = "password" />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary">
              Submit
            </button>
          </div>
          {authMode === "signin"  ?(
              <p className="text-center mt-2">
              Forgot <a href="/forgotpassword">password?</a>
            </p>
            ):(<p></p>)}
          
        </div>
      </form>
    </div>
  );
}