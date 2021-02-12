import React from "react";

import "./App.css";
import Logo from "./logo.png";

import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

class App extends React.Component {
  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
    console.log(this.state);
  };
  handleSubmit = (event) => {
    fetch("http://127.0.0.1:8000/request", {
      method: "POST",
      body: JSON.stringify(this.state),
    })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(await response.text());
        } else return response.json();
      })
      .then((data) => {
        toast.success(data.message, {
          position: "top-center",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          draggable: true,
          progress: undefined,
        });
      })
      .catch((error) => {
        console.log();
        toast.error("Error: " + JSON.parse(error.message).detail, {
          position: "top-center",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          draggable: true,
          progress: undefined,
        });
      });
    event.preventDefault();
  };

  render() {
    return (
      <div className="App">
        <ToastContainer />
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

        <i className="credit">
          A <a href="https://github.com/timofeji">@timofeji</a> project
        </i>
      </div>
    );
  }
}

export default App;
