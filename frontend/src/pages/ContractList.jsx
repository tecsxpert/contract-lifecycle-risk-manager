import React, { useState, useEffect } from 'react';

const ContractList = () => {
    // State to hold the 30 seeded records for the demo
    const [contracts, setContracts] = useState([]);

    return (
        <div className="font-arial p-8"> {/* 8px Grid: p-8 = 32px  */}
            <div className="flex justify-between items-center mb-8">
                <h1 className="text-[#1B4F8A] text-3xl font-bold">Contract Inventory</h1>

                {/* 44px Touch Target Button  */}
                <button className="bg-[#1B4F8A] text-white min-h-[44px] min-w-[44px] px-6 rounded-md hover:bg-blue-900 transition-colors">
                    + Create New Contract
                </button>
            </div>

            {/* Table following the 8px grid system  */}
            <div className="bg-white shadow-sm rounded-lg overflow-hidden border border-gray-200">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                    <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Contract Name</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vendor</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Risk Score</th>
                    </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                    {/* Placeholder for the 30 seeded records */}
                    <tr className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">High-Risk Vendor Agreement</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">TechCorp Solutions</td>
                        <td className="px-6 py-4 whitespace-nowrap">
                                <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                                    Pending Review
                                </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-bold text-red-600">8.5</td>
                    </tr>
                    {/* More rows will appear here after API integration */}
                    </tbody>
                </table>

                {/* Pagination Placeholder to show 30 records capacity  */}
                <div className="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
                    <div className="flex justify-between items-center">
                        <p className="text-sm text-gray-700">
                            Showing <span className="font-medium">1</span> to <span className="font-medium">10</span> of <span className="font-medium">30</span> results
                        </p>
                        <div className="flex gap-2">
                            <button className="min-h-[44px] px-4 py-2 border rounded-md">Previous</button>
                            <button className="min-h-[44px] px-4 py-2 border rounded-md">Next</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ContractList;