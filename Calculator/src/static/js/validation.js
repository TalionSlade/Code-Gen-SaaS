const validateInput = (input) => {
    const numReg = /^-?\d*(\.\d+)?$/;
    if (input === "" || !numReg.test(input)) {
        return false;
    }
    return true;
}

const validateOperator = (operator) => {
    const operators = ["+", "-", "*", "/"];
    if (!operators.includes(operator)) {
        return false;
    }
    return true;
}

const handleValidation = (input1, input2, operator) => {
    let errors = [];

    if (!validateInput(input1)) {
        errors.push("Invalid input: Please enter a valid first number.");
    }

    if (!validateInput(input2)) {
        errors.push("Invalid input: Please enter a valid second number.");
    }

    if (operator === "/" && input2 === "0") {
        errors.push("Cannot divide by zero.");
    }

    if (!validateOperator(operator)) {
        errors.push("Invalid operator: Please use +, -, *, or /.");
    }

    return errors;
}

module.exports = { handleValidation };