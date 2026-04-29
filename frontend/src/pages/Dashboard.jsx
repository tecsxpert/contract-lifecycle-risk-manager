import { useEffect, useState, useContext } from "react";
import api from "../services/api";
import { AuthContext } from "../context/AuthContext";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

function Dashboard() {
  const [stats, setStats] = useState({});
  const [period, setPeriod] = useState("7");
  const { token } = useContext(AuthContext);

  useEffect(() => {
    api
      .get(`/contracts/stats?days=${period}`, { 
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setStats(res.data))
      .catch((err) => console.error(err));
  }, [period]);

  const data = [
    { name: "Active", value: stats.active || 0 },
    { name: "Pending", value: stats.pending || 0 },
    { name: "Completed", value: stats.completed || 0 },
  ];

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Dashboard</h1>
      <select
        className="border p-2 mb-4"
        value={period}
        onChange={(e) => setPeriod(e.target.value)}
      >
        <option value="7">Last 7 Days</option>
        <option value="30">Last 30 Days</option>
      </select>
      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-blue-200 p-4">Total: {stats.total || 0}</div>
        <div className="bg-green-200 p-4">Active: {stats.active || 0}</div>
        <div className="bg-yellow-200 p-4">Pending: {stats.pending || 0}</div>
        <div className="bg-red-200 p-4">Completed: {stats.completed || 0}</div>
      </div>
      <BarChart width={500} height={300} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="value" />
      </BarChart>
    </div>
  );
}

export default Dashboard;