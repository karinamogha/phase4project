import React, { useState } from "react";

function AuthPage() {
  const [isLogin, setIsLogin] = useState(true); // To toggle between login and register
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  //form submission
  const handleSubmit = (e) => {
    e.preventDefault();

    const endpoint = isLogin ? "/login" : "/register";
    const data = {
      username: username,
      password: password,
    };

    fetch(`http://localhost:5000${endpoint}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert(
            isLogin ? "Logged in successfully!" : "Registered successfully!"
          );
        } else {
          alert(data.message || "Something went wrong.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Could not connect to the server.");
      });
  };

  return (
    <div style={{ textAlign: "center", margin: "50px" }}>
      <h1>Budget Buddy</h1>
      <h2>{isLogin ? "Log In" : "Register"}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Username:
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              style={{ marginLeft: "10px", marginBottom: "10px" }}
            />
          </label>
        </div>
        <div>
          <label>
            Password:
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{ marginLeft: "10px", marginBottom: "10px" }}
            />
          </label>
        </div>
        <button type="submit">{isLogin ? "Log In" : "Register"}</button>
      </form>
      <div style={{ marginTop: "20px" }}>
        {isLogin ? (
          <p>
            Don't have an account?{" "}
            <button
              onClick={() => setIsLogin(false)}
              style={{
                background: "none",
                border: "none",
                color: "blue",
                cursor: "pointer",
              }}
            >
              Register
            </button>
          </p>
        ) : (
          <p>
            Already have an account?{" "}
            <button
              onClick={() => setIsLogin(true)}
              style={{
                background: "none",
                border: "none",
                color: "blue",
                cursor: "pointer",
              }}
            >
              Log In
            </button>
          </p>
        )}
      </div>
    </div>
  );
}

export default AuthPage;