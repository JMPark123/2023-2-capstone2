/* 
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
*/

import { render, screen } from '@testing-library/react';
import MainPage from './MainPage'; // MainPage로 변경해서 렌더링한 버전

test('renders go to generate endpoint button', () => {
  render(<MainPage />); // MainPage 컴포넌트로 렌더링
  const buttonElement = screen.getByText(/Go to Generate Endpoint/i); // 버튼 텍스트로 찾기, 메인페이지가 처음으로 렌더링되므로 button이 있는지를 확인함
  expect(buttonElement).toBeInTheDocument();
});
