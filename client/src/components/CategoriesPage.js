import React, { useState } from "react";

function CategoriesPage() {
  const [name, setName] = useState("");
  const [budget, setBudget] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch("http://localhost:5555/categories", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, budget }),
    })
      .then((res) => res.json())
      .then((data) => alert("Category Added!"))
      .catch(() => alert("Server Error"));
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Category Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Budget Limit"
        value={budget}
        onChange={(e) => setBudget(e.target.value)}
        required
      />
      <button type="submit">Add Category</button>
    </form>
  );
}

export default CategoriesPage;