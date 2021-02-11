import "./App.css";
import Logo from "./logo.png";

let requestFunds = () => {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title: "React POST Request Example" }),
  };
  fetch("https://faucet.cheap/request", requestOptions)
    .then((response) => response.json())
    .then((data) => this.setState({ postId: data.id }));
};

function App() {
  return (
    <div className="App">
      <div className="logo">
        <img src={Logo} alt="logo" />
      </div>
      <p>
        Welcome to CheapETH Faucet.<br></br>
        <small> Where you can get cTH cheaper than usual... cuz its free</small>
      </p>
      <i>Address:</i>
      <input id="address" type="text" defaultValue="0x0"></input>
      <i>cTH request amount:</i>
      <input id="amt" type="number" defaultValue="0"></input>
      <button>Request Funds</button>
    </div>
  );
}

export default App;
