import React from "react";

const Expense = ({ description, amount, date }) => {
  return (
    <div>
      <h3>{description}</h3>
      <p>Amount: ${amount}</p>
      <p>Date: {date}</p>
    </div>
  );
};

export default Expense;