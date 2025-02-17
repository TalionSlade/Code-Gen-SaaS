import React from 'react';
import axios from 'axios';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      firstNumber: '',
      secondNumber: '',
      result: ''
    };
  }

  handleFirstNumberChange = (event) => {
    this.setState({ firstNumber: event.target.value });
  };

  handleSecondNumberChange = (event) => {
    this.setState({ secondNumber: event.target.value });
  };

  calculateResult = () => {
    const { firstNumber, secondNumber } = this.state;
    axios.get(`/calculate?first_number=${firstNumber}&second_number=${secondNumber}`)
      .then(response => {
        this.setState({ result: response.data });
      })
      .catch(error => {
        console.log(error);
      });
  };

  render() {
    return (
      <div>
        <input type="number" value={this.state.firstNumber} onChange={this.handleFirstNumberChange} />
        <input type="number" value={this.state.secondNumber} onChange={this.handleSecondNumberChange} />
        <button onClick={this.calculateResult}>Calculate</button>
        <p>{this.state.result}</p>
      </div>
    );
  }
}

export default App;