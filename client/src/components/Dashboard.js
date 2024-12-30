import React, { useEffect, useState } from "react";
import { Pie, Bar, Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
} from "chart.js";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement
);

const Dashboard = () => {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    // Fetch user-specific expenses
    const fetchExpenses = async () => {
        try {
            const response = await fetch("http://localhost:5555/expenses", {
                method: "GET",
                credentials: "include", // Ensures cookies are sent with the request
            });
    
            if (response.ok) {
                const data = await response.json();
                setExpenses(data);
            } else {
                console.error("Error fetching expenses:", await response.json());
            }
        } catch (err) {
            console.error("Error fetching expenses:", err);
        }
    };

    fetchExpenses();
  }, []);

  const generateChartData = (data) => {
    const categories = {};
    data.forEach((expense) => {
      if (expense.category) {
        categories[expense.category.name] =
          (categories[expense.category.name] || 0) + expense.amount;
      } else {
        categories["Uncategorized"] = (categories["Uncategorized"] || 0) + expense.amount;
      }
    });

    const labels = Object.keys(categories);
    const values = Object.values(categories);

    setChartData({
      labels,
      datasets: [
        {
          label: "Expenses",
          data: values,
          backgroundColor: [
            "#FF6384",
            "#36A2EB",
            "#FFCE56",
            "#4BC0C0",
            "#9966FF",
            "#FF9F40",
          ],
        },
      ],
    });
  };

  if (!chartData) {
    return <p>Loading dashboard data...</p>;
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <div style={{ width: "400px", margin: "auto" }}>
        <h2>Pie Chart</h2>
        <Pie data={chartData} />
        <h2>Bar Chart</h2>
        <Bar data={chartData} />
        <h2>Line Chart</h2>
        <Line data={chartData} />
      </div>
    </div>
  );
};

export default Dashboard;
