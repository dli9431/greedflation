import React, { useState, useEffect } from 'react';

export default function App() {
  
  function DataComponent() {
    fetch('http://localhost:5000/api/get_all')
      .then(response => response.json())
      .then(data => console.log(data));
  }
  
  return (
    <div>
      <button onClick={DataComponent}>Click me</button>
      <h1>Hello, World!</h1>
    </div>

  )
}