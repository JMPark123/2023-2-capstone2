// App.js
/*
import React from 'react';
import { useNavigate, Routes, Route } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import GenerateEndpoint from './GenerateEndpoint'; // GenerateEndpoint 컴포넌트 import

function App() {
  const navigate = useNavigate();

  const redirectToGenerateEndpoint = () => {
    navigate('/generate');
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <h1>Welcome to My App</h1>
        <button onClick={redirectToGenerateEndpoint}>문장을 생성해 봅시다!</button>
      </header>
      <Routes>
        <Route path="/generate" element={<GenerateEndpoint />} />
      </Routes>
    </div>
  );
}

export default App;

*/

import React from 'react';
import { useNavigate, Routes, Route } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import GenerateEndpoint from './GenerateEndpoint'; // GenerateEndpoint 컴포넌트 import

function App() {
  const navigate = useNavigate();

  const redirectToGenerateEndpoint = () => {
    navigate('/generate');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>SBERT-GPT 파이프라이닝을 활용한 양질의 문장 생성기</h1>
        <p>
          본 프로젝트는 SBERT-GPT 파이프라이닝을 통해 보다 더 유지보수가 쉬운 서비스 구성과 높은 품질의 문장을 생성합니다.
        </p>
        <button onClick={redirectToGenerateEndpoint}>Generate a Sentence</button>
      </header>
      <Routes>
        <Route path="/generate" element={<GenerateEndpoint />} />
      </Routes>
    </div>
  );
}

export default App;
