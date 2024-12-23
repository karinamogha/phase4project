import React, { useState } from "react";

function ExpenseForm() {
const [description, setDescription] = useState("");
const [amount, setAmount] = useState("");
const [date, setDate] = useState("");
const [category, setCategory] = useState("");

const handleSubmit = (e) => {
    e.preventDefault();
    fetch("http://localhost:5555/expenses", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ description, amount, date, category }),
    })
    .then((res) => res.json())
    .then((data) => alert("Expense Added!"))
    .catch(() => alert("Server Error"));
};

return (
    <form onSubmit={handleSubmit}>
    <input
        type="text"
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
    />
    <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        required
    />
    <input
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
        required
    />
    <input
        type="text"
        placeholder="Category"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
        required
    />
    <button type="submit">Add Expense</button>
    </form>
);
}

export default ExpenseForm;