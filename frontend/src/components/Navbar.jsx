import React from 'react';

const Navbar = () => {
    return (
        <nav className="bg-[#1B4F8A] p-4 shadow-md flex items-center justify-between">
            <div className="flex items-center gap-4">
                {/* Brand Name in Arial */}
                <h1 className="text-white text-xl font-bold font-arial">
                    Contract Risk Manager
                </h1>
            </div>

            {/* 44px Touch Target Button for Demo */}
            <button className="bg-white text-[#1B4F8A] font-arial font-semibold min-h-[44px] px-6 py-2 rounded-md hover:bg-gray-100 transition-colors">
                Logout
            </button>
        </nav>
    );
};

export default Navbar;