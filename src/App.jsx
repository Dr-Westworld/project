import React, { useState } from 'react';
import PlanView from './components/PlanView';
import DemoView from './components/DemoView';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('demo'); // 'demo', 'upload', 'plan'

  const renderView = () => {
    switch (currentView) {
      case 'demo':
        return <DemoView onStartUpload={() => setCurrentView('upload')} />;
      case 'upload':
        return <PlanView onBackToDemo={() => setCurrentView('demo')} />;
      default:
        return <DemoView onStartUpload={() => setCurrentView('upload')} />;
    }
  };

  return (
    <div className="App">
      {renderView()}
    </div>
  );
}

export default App;
