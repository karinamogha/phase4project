import React, { useState } from "react";

function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    const endpoint = isLogin ? "/login" : "/register";
    fetch(`http://localhost:5555${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          alert(isLogin ? "Logged in!" : "Registered!");
        } else {
          alert(data.error || "Something went wrong.");
        }
      })
      .catch(() => alert("Server error."));
  };

  return (
    <div
      style={{
        textAlign: "center",
        margin: "50px",
        padding: "20px",
        backgroundColor: "#002b5c", // Navy background
        borderRadius: "8px",
        color: "#fff", // White text for contrast
      }}
    >
      <h1>Budget Buddy</h1>
      <p>
        Budget Buddy is a personal finance management app designed to help you
        track expenses, manage your budget, and gain insights into your
        spending habits. Whether you're saving for a goal or just trying to
        stay on top of your finances, Budget Buddy makes budgeting simple and
        effective.
      </p>
      <h2>{isLogin ? "Login" : "Register"}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            style={{
              marginBottom: "10px",
              padding: "10px",
              borderRadius: "4px",
              border: "1px solid #ccc",
              width: "80%",
            }}
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{
              marginBottom: "10px",
              padding: "10px",
              borderRadius: "4px",
              border: "1px solid #ccc",
              width: "80%",
            }}
          />
        </div>
        <button
          type="submit"
          style={{
            padding: "10px 20px",
            borderRadius: "4px",
            border: "none",
            backgroundColor: "#00b894", // Green button
            color: "#fff",
            cursor: "pointer",
          }}
        >
          {isLogin ? "Login" : "Register"}
        </button>
      </form>
      <button
        onClick={() => setIsLogin(!isLogin)}
        style={{
          marginTop: "10px",
          padding: "10px 20px",
          borderRadius: "4px",
          border: "none",
          backgroundColor: "#0984e3", // Blue button
          color: "#fff",
          cursor: "pointer",
        }}
      >
        {isLogin ? "Register Instead" : "Login Instead"}
      </button>
    </div>
  );
}

export default AuthPage;
