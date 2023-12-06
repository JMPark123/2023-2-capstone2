import React, { useState } from 'react';
import './GenerateEndpoint.css'; // CSS 파일 import

const GenerateEndpoint = () => {
    const [sentence, setSentence] = useState('');
    const [response, setResponse] = useState('');
    const [score, setScore] = useState('');
    const [count, setCount] = useState('');

    const handleInputChange = (e) => {
        setSentence(e.target.value);
        setResponse('');
        setScore('');
        setCount('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch('http://localhost:5000/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ sentence }),
            });

            const data = await response.json();
            setResponse(data.message); // 서버로부터 받은 응답 문장 표시
            setScore(data.score); // 유사도 점수 표시
            setCount(data.count); // 총 문장 생성 횟수 표시
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="container">
            <h1>문장 생성기</h1>
            <div className="guideline">
                유사 문장을 생성하려는 문장을 빈칸에 작성하시고, 우측의 submit 버튼을 클릭해 주세요.
            </div>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={sentence}
                    onChange={handleInputChange}
                    placeholder="문장을 입력하세요"
                />
                <button type="submit">Submit</button>
            </form>
            {response && (
                <div className="response-container">
                    <p>생성된 문장: {response}</p>
                    <p>원 문장과의 유사도 점수: {score}</p>
                    <p>총 문장 생성 횟수: {count}</p>
                </div>
            )}
        </div>
    );
};

export default GenerateEndpoint;
