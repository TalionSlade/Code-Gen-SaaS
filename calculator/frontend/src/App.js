import React, { useState } from 'react';

const Calculator = () => {
  const [number1, setNumber1] = useState(0);
  const [number2, setNumber2] = useState(0);
  const [result, setResult] = useState(0);

  const add = () => {
    setResult(number1 + number2);
  };

  const subtract = () => {
    setResult(number1 - number2);
  };

  const multiply = () => {
    setResult(number1 * number2);
  };

  const divide = () => {
    if (number2 !== 0) {
      setResult(number1 / number2);
    }
  };

  return (
    <div>
      <input type="number" value={number1} onChange={e => setNumber1(parseInt(e.target.value))} />
      <input type="number" value={number2} onChange={e => setNumber2(parseInt(e.target.value))} />
      <button onClick={add}>Add</button>
      <button onClick={subtract}>Subtract</button>
      <button onClick={multiply}>Multiply</button>
      <button onClick={divide}>Divide</button>
      <h1>{result}</h1>
    </div>
  );
};

export default Calculator;