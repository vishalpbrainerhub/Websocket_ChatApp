// Login.js
import React, { useState } from 'react';
import './CSS/login.css'

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    
    // i have to send data in the form data format for oauth2formpassword

    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    fetch('http://localhost:8000/login/', {
        method: 'POST',
        body: formData,
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            if(data.message === "User logged in successfully"){
                alert("User logged in successfully");
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('username', data.username);
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
      <h2>Login</h2>
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
        <button type="button" onClick={handleLogin}>
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
