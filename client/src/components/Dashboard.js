import React from "react";
import { Pie, Bar, Line } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement);

const Dashboard = () => {
const dummyData = {
    labels: ["Rent", "Food", "Utilities"],
    datasets: [
    {
        label: "Expenses",
        data: [500, 200, 100],
        backgroundColor: ["red", "blue", "green"],
    },
    ],
};

return (
    <div>
    <h1>Dashboard</h1>
    <div style={{ width: "400px", margin: "auto" }}>
        <h2>Pie Chart</h2>
        <Pie data={dummyData} />
        <h2>Bar Chart</h2>
        <Bar data={dummyData} />
        <h2>Line Chart</h2>
        <Line data={dummyData} />
    </div>
    </div>
);
};

export default Dashboard;