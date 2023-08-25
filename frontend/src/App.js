import "./App.css";
import Chatapp from "./Components/Chat";
import Login from "./Components/Login";
import Signup from "./Components/Signup";
import Home from "./Components/Home";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom"; // Note the use of Routes

function App() {
  // add random cliend id by date time

  let token = localStorage.getItem("access_token");
  console.log(token);

  document.addEventListener("DOMContentLoaded", () => {
    if (token != null) {
      document.getElementById("login").style.display = "none";
      document.getElementById("signup").style.display = "none";
    }
  });

  return (
    <div className="App">
      {/* make a route and append it by names */}
      <Router>
        <div className="container">
          <div className="nav">
            <Link to="/" className="nav-link">
              HOME
            </Link>
            <Link to="/login" id="login" className="nav-link">
              LOGIN
            </Link>
            <Link to="/signup" id="signup" className="nav-link">
              SIGNUP
            </Link>
            <Link to="/chat" className="nav-link">
              CHAT
            </Link>
            <Link to="/about" className="nav-link">
              ABOUT
            </Link>
            <Link to="/logout" id="logout" className="nav-link">
              LOGOUT
            </Link>
          </div>
        </div>
        <div></div>
        <Routes>
          <Route path="/chat" element={<Chatapp />} />
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
