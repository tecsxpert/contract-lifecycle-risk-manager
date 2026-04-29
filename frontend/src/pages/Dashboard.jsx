import React from 'react';
// Note: You will need to install recharts: npm install recharts
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
    // Mock data based on your 30 seeded records for the Day 12 Polish
    const data = [
        { name: 'Low Risk', count: 10 },
        { name: 'Medium Risk', count: 12 },
        { name: 'High Risk', count: 8 },
    ];

    return (
        <div className="font-arial p-8 bg-gray-50 min-h-screen">
            <h1 className="text-[#1B4F8A] text-3xl font-bold mb-8">System Dashboard</h1>

            {/* 4 KPI Cards - 8px Grid (gap-8 = 32px) */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                <div className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-[#1B4F8A]">
                    <p className="text-sm text-gray-500 uppercase font-semibold">Total Contracts</p>
                    <p className="text-3xl font-bold">30</p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-red-600">
                    <p className="text-sm text-gray-500 uppercase font-semibold">High Risk</p>
                    <p className="text-3xl font-bold text-red-600">8</p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-yellow-500">
                    <p className="text-sm text-gray-500 uppercase font-semibold">Pending Review</p>
                    <p className="text-3xl font-bold text-yellow-500">12</p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-green-600">
                    <p className="text-sm text-gray-500 uppercase font-semibold">Active</p>
                    <p className="text-3xl font-bold text-green-600">10</p>
                </div>
            </div>

            {/* Charts Section */}
            <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-200">
                <h3 className="text-lg font-semibold mb-6 text-gray-700">Risk Distribution Overview</h3>
                <div className="h-80 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={data}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip cursor={{fill: '#f3f4f6'}} />
                            <Bar dataKey="count" fill="#1B4F8A" radius={[4, 4, 0, 0]} barSize={60} />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;