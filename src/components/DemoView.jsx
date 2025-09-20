import React, { useState } from 'react';
import PlanView from './PlanView';
import samplePlan from '../data/samplePlan';

function DemoView({ onStartUpload }) {
  const [showDemo, setShowDemo] = useState(false);

  if (showDemo) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto p-6">
          <div className="mb-6 flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">
              Legal Document Assistant - Demo
            </h1>
            <button
              onClick={() => setShowDemo(false)}
              className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600"
            >
              Back to Upload
            </button>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Chat Interface */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="mb-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  AI Chat Assistant
                </h3>
                <p className="text-sm text-gray-600">
                  Ask questions about your progress path. Try asking:
                </p>
                <ul className="text-sm text-gray-600 mt-2 space-y-1">
                  <li>• "What documents do I need for stage 2?"</li>
                  <li>• "How long will this process take?"</li>
                  <li>• "What are the common issues I should watch out for?"</li>
                </ul>
              </div>
              
              <div className="space-y-4">
                <div className="flex justify-end">
                  <div className="max-w-xs bg-blue-600 text-white px-4 py-2 rounded-lg">
                    <p className="text-sm">What documents do I need for stage 2?</p>
                    <p className="text-xs opacity-75 mt-1">10:30 AM</p>
                  </div>
                </div>
                
                <div className="flex justify-start">
                  <div className="max-w-xs bg-white text-gray-900 border border-gray-200 px-4 py-2 rounded-lg">
                    <p className="text-sm">For stage 2 (Prepare Required Documents), you'll need:</p>
                    <ul className="text-xs mt-2 space-y-1">
                      <li>• Articles of Organization</li>
                      <li>• Operating Agreement</li>
                      <li>• Statement of Information</li>
                      <li>• Registered Agent Information</li>
                    </ul>
                    <p className="text-xs opacity-75 mt-2">10:30 AM</p>
                  </div>
                </div>
              </div>
              
              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    placeholder="Ask about your progress path..."
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled
                  />
                  <button
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                    disabled
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>

            {/* Progress Path */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">
                  {samplePlan.taskTitle}
                </h2>
                <div className="text-sm text-gray-500">
                  {samplePlan.stages.filter(s => s.isCompleted).length} / {samplePlan.stages.length} completed
                </div>
              </div>
              
              <div className="space-y-4">
                {samplePlan.stages.map((stage, index) => (
                  <div key={stage.id} className="border rounded-lg p-4 bg-blue-50 border-blue-200 hover:bg-blue-100 transition-all duration-200 hover:shadow-md">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <div className="w-6 h-6 rounded-full bg-gray-300 text-gray-600 flex items-center justify-center text-xs font-bold">
                            {index + 1}
                          </div>
                          <h3 className="text-lg font-bold text-blue-900">
                            {stage.title}
                          </h3>
                        </div>
                        
                        <p className="text-sm text-gray-600 mb-2">
                          {stage.shortDescription}
                        </p>
                        
                        <div className="text-xs text-gray-500 mb-2">
                          ⏱️ Estimated time: {stage.estimatedTime}
                        </div>
                        
                        <div className="flex items-center gap-1 mb-2">
                          <span className="text-xs text-gray-500">Confidence:</span>
                          <span className="text-xs px-2 py-1 rounded-full bg-green-100 text-green-800">
                            {stage.confidence}
                          </span>
                        </div>
                      </div>
                      
                      <div className="flex items-center gap-2 ml-4">
                        <button className="text-xs bg-blue-500 text-white px-3 py-1 rounded-full hover:bg-blue-600 transition-colors">
                          Mark Done
                        </button>
                        
                        <div className="text-xs text-gray-400">
                          ▶
                        </div>
                      </div>
                    </div>
                    
                    <div className="mt-2 pt-2 border-t border-gray-200">
                      <div className="text-xs text-gray-500">
                        Sources: {stage.citations?.length || 0} reference{(stage.citations?.length || 0) > 1 ? 's' : ''}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Legal Document Assistant
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            AI-powered tool to demystify legal documents and create step-by-step progress paths
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            How it works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">1. Upload Document</h3>
              <p className="text-gray-600">Upload your legal document (PDF or Word) and describe what you need help with</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">2. AI Analysis</h3>
              <p className="text-gray-600">Our AI analyzes your document and creates a structured progress path</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">3. Follow Steps</h3>
              <p className="text-gray-600">Click on stages to see detailed instructions and track your progress</p>
            </div>
          </div>
        </div>

        <div className="text-center">
          <button
            onClick={() => setShowDemo(true)}
            className="px-8 py-4 bg-blue-600 text-white text-lg font-semibold rounded-lg hover:bg-blue-700 transition-colors mr-4"
          >
            View Demo
          </button>
          <button
            onClick={onStartUpload}
            className="px-8 py-4 bg-green-600 text-white text-lg font-semibold rounded-lg hover:bg-green-700 transition-colors"
          >
            Start Now
          </button>
        </div>
      </div>
    </div>
  );
}

export default DemoView;
