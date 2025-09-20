import React from 'react';

function StageCard({ stage, level, isExpanded, onClick, onMarkComplete }) {
  const getCardStyles = () => {
    const baseStyles = "border rounded-lg p-4 mb-3 cursor-pointer transition-all duration-200 hover:shadow-md";
    const levelStyles = {
      1: "bg-blue-50 border-blue-200 hover:bg-blue-100",
      2: "bg-green-50 border-green-200 hover:bg-green-100 ml-4",
      3: "bg-yellow-50 border-yellow-200 hover:bg-yellow-100 ml-8",
      4: "bg-purple-50 border-purple-200 hover:bg-purple-100 ml-12"
    };
    const completedStyles = stage.isCompleted ? "bg-green-100 border-green-300" : "";
    const expandedStyles = isExpanded ? "shadow-lg ring-2 ring-blue-300" : "shadow-sm";
    
    return `${baseStyles} ${levelStyles[level] || levelStyles[4]} ${completedStyles} ${expandedStyles}`;
  };

  const getTitleStyles = () => {
    const levelStyles = {
      1: "text-lg font-bold text-blue-900",
      2: "text-base font-semibold text-green-900",
      3: "text-sm font-medium text-yellow-900",
      4: "text-sm font-medium text-purple-900"
    };
    return levelStyles[level] || levelStyles[4];
  };

  return (
    <div 
      className={getCardStyles()}
      onClick={() => onClick()}
    >
      <div className="flex justify-between items-start">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
              stage.isCompleted 
                ? 'bg-green-500 text-white' 
                : 'bg-gray-300 text-gray-600'
            }`}>
              {stage.isCompleted ? '✓' : stage.stageNumber || '○'}
            </div>
            <h3 className={getTitleStyles()}>
              {stage.title}
            </h3>
          </div>
          
          <p className="text-sm text-gray-600 mb-2">
            {stage.shortDescription}
          </p>
          
          {stage.estimatedTime && (
            <div className="text-xs text-gray-500 mb-2">
              ⏱️ Estimated time: {stage.estimatedTime}
            </div>
          )}
          
          {stage.confidence && (
            <div className="flex items-center gap-1 mb-2">
              <span className="text-xs text-gray-500">Confidence:</span>
              <span className={`text-xs px-2 py-1 rounded-full ${
                stage.confidence === 'high' 
                  ? 'bg-green-100 text-green-800'
                  : stage.confidence === 'medium'
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-red-100 text-red-800'
              }`}>
                {stage.confidence}
              </span>
            </div>
          )}
        </div>
        
        <div className="flex items-center gap-2 ml-4">
          {stage.isCompleted ? (
            <div className="flex items-center gap-1 text-green-600">
              <span className="text-sm">✓</span>
              <span className="text-xs">Completed</span>
            </div>
          ) : (
            <button 
              className="text-xs bg-blue-500 text-white px-3 py-1 rounded-full hover:bg-blue-600 transition-colors"
              onClick={(e) => { 
                e.stopPropagation(); 
                onMarkComplete(); 
              }}
            >
              Mark Done
            </button>
          )}
          
          {stage.subStages && stage.subStages.length > 0 && (
            <div className="text-xs text-gray-400">
              {isExpanded ? '▼' : '▶'}
            </div>
          )}
        </div>
      </div>
      
      {stage.citations && stage.citations.length > 0 && (
        <div className="mt-2 pt-2 border-t border-gray-200">
          <div className="text-xs text-gray-500">
            Sources: {stage.citations.length} reference{stage.citations.length > 1 ? 's' : ''}
          </div>
        </div>
      )}
    </div>
  );
}

export default StageCard;
