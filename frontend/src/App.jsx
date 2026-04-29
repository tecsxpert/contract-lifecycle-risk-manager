import React from 'react';
import Navbar from './components/Navbar';

function App() {
    return (
        <div className="min-h-screen bg-gray-50 font-arial">
            {/* Renders the Navbar with #1B4F8A brand color */}
            <Navbar />

            <main className="p-8">
                <div className="max-w-7xl mx-auto">
                    <h2 className="text-2xl font-bold text-gray-800 mb-6">
                        Dashboard Overview
                    </h2>

                    {/* Placeholder for Day 12 Analytics/Charts */}
                    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                        <p className="text-gray-600">
                            Backend status: 30 records seeded successfully.
                        </p>
                    </div>
                </div>
            </main>
        </div>
    );
}

export default App;