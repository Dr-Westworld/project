import React, { useState } from 'react';

function StageDetail({ stage, onClose, onSubStageClick, onSubStageComplete }) {
  const [expandedSubStages, setExpandedSubStages] = useState(new Set());

  const toggleSubStage = (subStageId) => {
    setExpandedSubStages(prev => {
      const newSet = new Set(prev);
      if (newSet.has(subStageId)) {
        newSet.delete(subStageId);
      } else {
        newSet.add(subStageId);
      }
      return newSet;
    });
  };

  const renderSubStages = (subStages, level = 2) => {
    return subStages.map(subStage => {
      const isExpanded = expandedSubStages.has(subStage.id);
      
      return (
        <div key={subStage.id} className="mb-3">
          <div 
            className={`border rounded-lg p-3 cursor-pointer transition-all duration-200 hover:shadow-md ${
              subStage.isCompleted 
                ? 'bg-green-50 border-green-200' 
                : 'bg-white border-gray-200'
            }`}
            onClick={() => {
              if (subStage.subStages && subStage.subStages.length > 0) {
                toggleSubStage(subStage.id);
              } else {
                onSubStageClick(subStage.id);
              }
            }}
          >
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <div className={`w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold ${
                    subStage.isCompleted 
                      ? 'bg-green-500 text-white' 
                      : 'bg-gray-300 text-gray-600'
                  }`}>
                    {subStage.isCompleted ? '✓' : subStage.stageNumber || '○'}
                  </div>
                  <h4 className={`font-medium ${
                    level === 2 ? 'text-green-900' : 'text-gray-900'
                  }`}>
                    {subStage.title}
                  </h4>
                </div>
                
                <p className="text-sm text-gray-600 mb-2">
                  {subStage.shortDescription}
                </p>
                
                {subStage.estimatedTime && (
                  <div className="text-xs text-gray-500 mb-1">
                    ⏱️ {subStage.estimatedTime}
                  </div>
                )}
                
                {subStage.requiredDocuments && subStage.requiredDocuments.length > 0 && (
                  <div className="text-xs text-gray-500 mb-1">
                    📄 Required: {subStage.requiredDocuments.join(', ')}
                  </div>
                )}
                
                {subStage.website && (
                  <div className="text-xs text-blue-600 mb-1">
                    🌐 <a href={subStage.website} target="_blank" rel="noopener noreferrer" 
                         className="hover:underline" onClick={(e) => e.stopPropagation()}>
                      {subStage.website}
                    </a>
                  </div>
                )}
              </div>
              
              <div className="flex items-center gap-2 ml-4">
                {subStage.isCompleted ? (
                  <span className="text-green-600 text-sm">✓</span>
                ) : (
                  <button 
                    className="text-xs bg-green-500 text-white px-2 py-1 rounded hover:bg-green-600 transition-colors"
                    onClick={(e) => { 
                      e.stopPropagation(); 
                      onSubStageComplete(subStage.id); 
                    }}
                  >
                    Done
                  </button>
                )}
                
                {subStage.subStages && subStage.subStages.length > 0 && (
                  <span className="text-xs text-gray-400">
                    {isExpanded ? '▼' : '▶'}
                  </span>
                )}
              </div>
            </div>
            
            {subStage.citations && subStage.citations.length > 0 && (
              <div className="mt-2 pt-2 border-t border-gray-200">
                <div className="text-xs text-gray-500 mb-1">Sources:</div>
                <div className="space-y-1">
                  {subStage.citations.map((citation, idx) => (
                    <div key={idx} className="text-xs">
                      <a 
                        href={citation.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline"
                        onClick={(e) => e.stopPropagation()}
                      >
                        {citation.title || citation.url}
                      </a>
                      <span className="text-gray-400 ml-1">
                        ({citation.source_type})
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
          
          {/* Recursive rendering for nested sub-stages */}
          {isExpanded && subStage.subStages && subStage.subStages.length > 0 && (
            <div className="ml-4 mt-2">
              {renderSubStages(subStage.subStages, level + 1)}
            </div>
          )}
        </div>
      );
    });
  };

  return (
    <div className="bg-white border-2 border-blue-200 rounded-lg p-4 mt-2 shadow-lg">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-bold text-blue-900">
          {stage.title} - Detailed Instructions
        </h3>
        <button 
          onClick={onClose}
          className="text-red-500 hover:text-red-700 text-xl font-bold"
          title="Close detail view"
        >
          ✕
        </button>
      </div>
      
      {stage.description && (
        <div className="mb-4 p-3 bg-gray-50 rounded">
          <p className="text-sm text-gray-700">{stage.description}</p>
        </div>
      )}
      
      {stage.requiredDocuments && stage.requiredDocuments.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-semibold text-gray-900 mb-2">Required Documents:</h4>
          <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
            {stage.requiredDocuments.map((doc, idx) => (
              <li key={idx}>{doc}</li>
            ))}
          </ul>
        </div>
      )}
      
      {stage.website && (
        <div className="mb-4">
          <h4 className="text-sm font-semibold text-gray-900 mb-2">Website:</h4>
          <a 
            href={stage.website} 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline text-sm"
          >
            {stage.website}
          </a>
        </div>
      )}
      
      {stage.estimatedTime && (
        <div className="mb-4">
          <h4 className="text-sm font-semibold text-gray-900 mb-2">Timeline:</h4>
          <p className="text-sm text-gray-700">{stage.estimatedTime}</p>
        </div>
      )}
      
      {stage.subStages && stage.subStages.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-gray-900 mb-3">Step-by-step process:</h4>
          <div className="space-y-2">
            {renderSubStages(stage.subStages)}
          </div>
        </div>
      )}
      
      {stage.warnings && stage.warnings.length > 0 && (
        <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded">
          <h4 className="text-sm font-semibold text-yellow-800 mb-2">⚠️ Important Notes:</h4>
          <ul className="list-disc list-inside text-sm text-yellow-700 space-y-1">
            {stage.warnings.map((warning, idx) => (
              <li key={idx}>{warning}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default StageDetail;
