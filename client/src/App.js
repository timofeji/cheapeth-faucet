import React from "react";

import "./App.css";
import Logo from "./logo.png";

class App extends React.Component {
  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
    console.log(this.state);
  };
  handleSubmit = (event) => {
    fetch("https://api.faucet.cheap/request", {
      method: "POST",
      body: JSON.stringify(this.state),
    }).then(function (response) {
      console.log(response);
      return response.json();
    });
    event.preventDefault();
  };

  render() {
    return (
      <div className="App">
        <div className="logo">
          <img src={Logo} alt="logo" />
        </div>
        <p>
          Welcome to CheapETH Faucet.<br></br>
          <small>
            {" "}
            Where you can get cTH cheaper than usual... cuz its free
          </small>
        </p>
        <i>Address:</i>
        <input
          name="address"
          type="text"
          defaultValue="0x0"
          onChange={this.handleChange}
        ></input>
        <i>cTH request amount:</i>
        <input
          name="amt"
          type="number"
          defaultValue="0"
          onChange={this.handleChange}
        ></input>
        <button onClick={this.handleSubmit}>Request Funds</button>
      </div>
    );
  }
}

export default App;
