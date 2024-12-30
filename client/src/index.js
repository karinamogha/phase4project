import React from "react";
import ReactDOM from "react-dom/client"; // Import the new ReactDOM API
import "./index.css";
import App from "./App";

const root = ReactDOM.createRoot(document.getElementById("root")); // Create the root element
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
