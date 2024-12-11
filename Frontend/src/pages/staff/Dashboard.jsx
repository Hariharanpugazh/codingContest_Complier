import { useState } from 'react';
import { FaCode, FaQuestionCircle, FaComments, FaPlus } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const navigate = useNavigate();

  

  return (
    <div className="min-h-screen bg-yellow-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Assessment Dashboard</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* MCQ Round Card */}
          <div className="bg-white rounded-2xl shadow-xl border border-yellow-200 p-6 relative">
            <div className="flex items-center mb-4">
              <FaQuestionCircle className="h-8 w-8 text-yellow-600 mr-3" />
              <h2 className="text-xl font-semibold text-gray-900">MCQ Round</h2>
              <FaPlus 
                className="h-6 w-6 text-gray-500 absolute top-4 right-4 cursor-pointer"
                onClick={() => navigate(`/mcq`)}
              />
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg hover:bg-yellow-100 transition-colors cursor-pointer">
                <span className="font-medium">Ongoing</span>
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">3 Active</span>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg hover:bg-yellow-100 transition-colors cursor-pointer">
                <span className="font-medium">Draft</span>
                <span className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm">2 Saved</span>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg hover:bg-yellow-100 transition-colors cursor-pointer">
                <span className="font-medium">Published</span>
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">5 Tests</span>
              </div>
            </div>
          </div>

          {/* Coding Round Card */}
          <div className="bg-white rounded-2xl shadow-xl border border-yellow-200 p-6 relative">
            <div className="flex items-center mb-4">
              <FaCode className="h-8 w-8 text-yellow-600 mr-3" />
              <h2 className="text-xl font-semibold text-gray-900">Coding Round</h2>
              <FaPlus 
                className="h-6 w-6 text-gray-500 absolute top-4 right-4 cursor-pointer"
                onClick={() => navigate('/coding')}
              />
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg hover:bg-yellow-100 transition-colors cursor-pointer">
                <span className="font-medium">Ongoing</span>
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">2 Active</span>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg hover:bg-yellow-100 transition-colors cursor-pointer">
                <span className="font-medium">Draft</span>
                <span className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm">1 Saved</span>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg hover:bg-yellow-100 transition-colors cursor-pointer">
                <span className="font-medium">Published</span>
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">4 Tests</span>
              </div>
            </div>
          </div>

          {/* Communication Round Card */}
          <div className="bg-white rounded-2xl shadow-xl border border-yellow-200 p-6 relative">
            <div className="flex items-center mb-4">
              <FaComments className="h-8 w-8 text-yellow-600 mr-3" />
              <h2 className="text-xl font-semibold text-gray-900">Communication Round</h2>
              <FaPlus 
                className="h-6 w-6 text-gray-500 absolute top-4 right-4 cursor-pointer"
                onClick={() => navigate('/communication')}
              />
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg hover:bg-yellow-100 transition-colors cursor-pointer">
                <span className="font-medium">Ongoing</span>
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">1 Active</span>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg hover:bg-yellow-100 transition-colors cursor-pointer">
                <span className="font-medium">Draft</span>
                <span className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm">3 Saved</span>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg hover:bg-yellow-100 transition-colors cursor-pointer">
                <span className="font-medium">Published</span>
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">2 Tests</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
