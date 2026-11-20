import {Routes, Route, Link } from "react-router-dom";
import Home from "./components/Home";
import About from "./components/About";
import Shop from "./components/Shop";
import Register from "./components/Register";
import Admin from "./components/Admin";
import './App.css';



function App() {
  return (
    <div>
    <div><h1>Wholly Roasters</h1></div>

  <ul id="navbar">
    <li className="navitem"><Link to="" className="active">Home</Link></li>
    <li className="navitem"><Link to="/about">About</Link></li>
    <li className="navitem"><Link to="/shop">Shop</Link></li>
    <li className="navitem"><Link to="/register">Register</Link></li>
    <li className="navitem"><Link to="/admin">Admin</Link></li>
  </ul>

   <div className="main">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/shop" element={<Shop />} />
        <Route path="/register" element={<Register />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>

   </div>    



    </div>
  );
}

export default App;
