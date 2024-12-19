import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App"; // App.js is correctly located in the src/ directory
import "./index.css"; // Include any global CSS styles

const container = document.getElementById("root");
const root = createRoot(container);

root.render(<App />);
