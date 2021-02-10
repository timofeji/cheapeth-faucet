import "./App.css";
import Logo from "./logo.png"

function App() {
  return (
    <div className="App">
      <div className="logo">
        <img src={Logo} alt="logo" />
      </div>
      <p>
        Welcome to CheapETH Faucet.<br></br>
        <small> Where you can get cTH cheaper than usual.</small>
      </p>
      <i>Address:</i>
      <input id="address" type="text" defaultValue="0x0"></input>
      <i>cTH request amount:</i>
      <input id="amt" type="number" defaultValue="0"></input>
      <button>Request</button>
    </div>
  );
}

export default App;
