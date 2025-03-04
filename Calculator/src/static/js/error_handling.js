import React from 'react';

export const validateInput = (num1, num2, operator) => {
  const validOperators = ['+', '-', '*', '/'];
  const errorMessage = {
    operator: "Invalid operator: Please use +, -, *, or /",
    number: "Invalid input: Please enter numeric values",
    divideByZero: "Cannot divide by zero"
  };

  if (!validOperators.includes(operator)) {
    return errorMessage.operator;
  }

  if (isNaN(num1) || isNaN(num2)) {
    return errorMessage.number;
  }

  if (operator === '/' && num2 == 0) {
    return errorMessage.divideByZero;
  }

  return null;
};

export const ErrorDisplay = ({error}) => {
  if (error) {
    return (
      <div className="error-message">
        {error}
      </div>
    );
  } else {
    return null;
  }
};