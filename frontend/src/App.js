import './App.css';
import SubCard from "./Components/SubCard.js"
import Carousel from 'react-elastic-carousel';
import React, { Component, useState, useEffect} from 'react';
import Email from "./Components/Email.js";
import Navbar from "./Components/Navbar.js"
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  // Assigns state to count so we can add new subs
  let[subCount, setSubCount] = useState([])

  let SubCardArr = [];
  var i;
  // Creates an array of subcard components
  for(i = 0; i < subCount; i++){
    SubCardArr.push(<SubCard position={i}></SubCard>)
  }
  // Sends a post request for our number of subs
  useEffect(()=>{
    fetch('http://localhost:5000/totalcount/')
    .then ((response) => response.json())
    .then((data) => setSubCount(data))
    .catch((error) => console.log(error))
  }, [])

  return (
    <div className="App">
    <Navbar></Navbar>
    <p>Current Subs</p>
    <Carousel>
    {SubCardArr}
    </Carousel>
    <Email></Email>
    </div>
  );
}

export default App;
