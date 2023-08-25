// Login.js
import React, { useState } from 'react';
import './CSS/signup.css'

const Signup = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignup = () => {
    
    if(email === '' || password === ''){
        alert("Please fill all the fields");
        return;
    }

    const formData = {
        email: email,
        password: password
    }

    fetch('http://localhost:8000/user/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            if(data.message === "User SignUp in successfully"){
                alert("User SignUp in successfully");
                localStorage.setItem('access_token', data.access_token);
            }else{
                alert(data.message);
            }
        })
        .catch((error) => {
            console.log(error);
        });
  };

  return (

    <div className="auth-container">
      <h2>SIGN UP</h2>
      <form>
        <label htmlFor="email">Email</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <label htmlFor="password">Password</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="button" onClick={handleSignup}>
          Signup
        </button>
      </form>
    </div>
  );
};

export default Signup;
