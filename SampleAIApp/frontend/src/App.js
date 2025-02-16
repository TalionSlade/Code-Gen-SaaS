import React from 'react';
import './App.css';

function App() {
  const [num1, setNum1] = React.useState('');
  const [num2, setNum2] = React.useState('');
  const [result, setResult] = React.useState('');
  const [operation, setOperation] = React.useState('');

  function handleClick(e) {
    e.preventDefault();
    if (operation === '+') {
      setResult((parseFloat(num1) + parseFloat(num2)).toString());
    } else if (operation === '-') {
      setResult((parseFloat(num1) - parseFloat(num2)).toString());
    } else if (operation === '/') {
      setResult((parseFloat(num1) / parseFloat(num2)).toString());
    } else if (operation === '*') {
      setResult((parseFloat(num1) * parseFloat(num2)).toString());
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <p>
          Enter two numbers and select an operation (+, -, x, /):
          <br />
          <input
            type="text"
            value={num1}
            onChange={(e) => setNum1(e.target.value)}
          />
          <select value={operation} onChange={(e) => setOperation(e.target.value)}>
            <option value="+">+</option>
            <option value="-">-</option>
            <option value="/">/</option>
            <option value="*">*</option>
          </select>
          <input
            type="text"
            value={num2}
            onChange={(e) => setNum2(e.target.value)}
          />
          <button onClick={handleClick}>Calculate</button>
        </p>
        <p>{result}</p>
      </header>
    </div>
  );
}

export default App;