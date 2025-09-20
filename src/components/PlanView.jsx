import React, { useState, useEffect } from 'react';
import StageCard from './StageCard';
import StageDetail from './StageDetail';
import UploadArea from './UploadArea';
import ChatInterface from './ChatInterface';

function PlanView({ onBackToDemo }) {
  const [plan, setPlan] = useState(null);
  const [expandedPath, setExpandedPath] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [chatMessages, setChatMessages] = useState([]);

  // Handle document upload and plan generation
  const handleUpload = async (file, prompt) => {
    setLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('prompt', prompt);

      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload document');
      }

      const result = await response.json();
      setPlan(result.plan);
      setChatMessages([{
        id: 1,
        type: 'user',
        content: `Uploaded document: ${file.name}. Prompt: ${prompt}`,
        timestamp: new Date()
      }, {
        id: 2,
        type: 'assistant',
        content: 'I\'ve analyzed your document and generated a step-by-step progress path. Click on any stage to see detailed instructions.',
        timestamp: new Date()
      }]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle stage click - expand to show details
  const handleStageClick = async (stageId, levelPath) => {
    setExpandedPath(levelPath);
    
    // Fetch detailed information for this stage
    try {
      const response = await fetch(`/api/plan/${plan.planId}/stage/${stageId}`);
      if (response.ok) {
        const stageDetail = await response.json();
        // Update the plan with detailed stage information
        setPlan(prevPlan => updateStageDetail(prevPlan, stageId, stageDetail));
      }
    } catch (err) {
      console.error('Failed to fetch stage details:', err);
    }
  };

  // Update stage detail in the plan structure
  const updateStageDetail = (currentPlan, stageId, detail) => {
    const updateStages = (stages) => {
      return stages.map(stage => {
        if (stage.id === stageId) {
          return { ...stage, ...detail, subStages: detail.subStages || stage.subStages };
        }
        if (stage.subStages) {
          return { ...stage, subStages: updateStages(stage.subStages) };
        }
        return stage;
      });
    };

    return {
      ...currentPlan,
      stages: updateStages(currentPlan.stages)
    };
  };

  // Handle stage completion
  const handleMarkComplete = async (stageId) => {
    try {
      const response = await fetch(`/api/plan/${plan.planId}/stage/${stageId}/markComplete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: true })
      });

      if (response.ok) {
        // Update local state
        setPlan(prevPlan => markStageComplete(prevPlan, stageId));
      }
    } catch (err) {
      console.error('Failed to mark stage complete:', err);
    }
  };

  // Mark stage as complete in the plan structure
  const markStageComplete = (currentPlan, stageId) => {
    const updateStages = (stages) => {
      return stages.map(stage => {
        if (stage.id === stageId) {
          return { ...stage, isCompleted: true };
        }
        if (stage.subStages) {
          return { ...stage, subStages: updateStages(stage.subStages) };
        }
        return stage;
      });
    };

    return {
      ...currentPlan,
      stages: updateStages(currentPlan.stages)
    };
  };

  // Handle closing expanded view
  const handleClose = () => {
    setExpandedPath(prev => prev.slice(0, -1));
  };

  // Render stages recursively
  const renderStages = (stages, level = 1, pathPrefix = []) => {
    return stages.map(stage => {
      const thisPath = [...pathPrefix, stage.id];
      const isExpanded = expandedPath.length >= thisPath.length &&
                         expandedPath.every((id, idx) => id === thisPath[idx]);
      
      return (
        <div key={stage.id} className={`stage-container level-${level}`}>
          <StageCard 
            stage={stage}
            level={level}
            isExpanded={isExpanded}
            onClick={() => handleStageClick(stage.id, thisPath)}
            onMarkComplete={() => handleMarkComplete(stage.id)}
          />
          
          {isExpanded && stage.subStages && stage.subStages.length > 0 && (
            <StageDetail
              stage={stage}
              onClose={handleClose}
              onSubStageClick={(subStageId) => handleStageClick(subStageId, [...thisPath, subStageId])}
              onSubStageComplete={handleMarkComplete}
            />
          )}
        </div>
      );
    });
  };

  if (!plan) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-4xl mx-auto">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900">
              Legal Document Assistant
            </h1>
            {onBackToDemo && (
              <button
                onClick={onBackToDemo}
                className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600"
              >
                ← Back to Demo
              </button>
            )}
          </div>
          <UploadArea onUpload={handleUpload} loading={loading} error={error} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Chat Interface */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <ChatInterface 
              messages={chatMessages}
              onSendMessage={(message) => {
                setChatMessages(prev => [...prev, {
                  id: Date.now(),
                  type: 'user',
                  content: message,
                  timestamp: new Date()
                }]);
                // Handle chat message processing here
              }}
            />
          </div>

          {/* Progress Path */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                {plan.taskTitle}
              </h2>
              <div className="text-sm text-gray-500">
                {plan.stages.filter(s => s.isCompleted).length} / {plan.stages.length} completed
              </div>
            </div>
            
            <div className="space-y-4">
              {renderStages(plan.stages)}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PlanView;
