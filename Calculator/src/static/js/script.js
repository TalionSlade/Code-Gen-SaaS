import React, { useState } from 'react';
import axios from 'axios';

const Calculator = () => {
    const [num1, setNum1] = useState('');
    const [num2, setNum2] = useState('');
    const [operator, setOperator] = useState('+');
    const [result, setResult] = useState('');
    const [error, setError] = useState('');

    const calculateResult = async () => {
        if (isNaN(num1) || isNaN(num2)) {
            setError('Invalid input: Please enter numeric values');
            return;
        }

        if (operator !== '+' && operator !== '-' && operator !== '*' && operator !== '/') {
            setError('Invalid operator: Please use +, -, *, or /');
            return;
        }

        if (operator === '/' && num2 === '0') {
            setError('Cannot divide by zero');
            return;
        }

        try {
            const response = await axios.post('http:
                num1, 
                num2, 
                operator
            });

            setResult(response.data.result);
            setError('');
        } catch (err) {
            setError('An error occurred while calculating. Please try again.');
        }
    }

    const clearInput = () => {
        setNum1('');
        setNum2('');
        setOperator('+');
        setResult('');
        setError('');
    }

    return (
        <div>
            <input type="text" value={num1} onChange={e => setNum1(e.target.value)} />
            <select value={operator} onChange={e => setOperator(e.target.value)}>
                <option value="+">+</option>
                <option value="-">-</option>
                <option value="*">*</option>
                <option value="/">/</option>
            </select>
            <input type="text" value={num2} onChange={e => setNum2(e.target.value)} />
            <button onClick={calculateResult}>Calculate</button>
            <button onClick={clearInput}>Clear</button>
            {result && <div>Result: {result}</div>}
            {error && <div>Error: {error}</div>}
        </div>
    );
}

export default Calculator;