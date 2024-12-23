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
    <div>
      <h1>Budget Buddy</h1>
      <h2>{isLogin ? "Login" : "Register"}</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">{isLogin ? "Login" : "Register"}</button>
      </form>
      <button onClick={() => setIsLogin(!isLogin)}>
        {isLogin ? "Register Instead" : "Login Instead"}
      </button>
    </div>
  );
}

export default AuthPage;