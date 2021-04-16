
pragma solidity ^0.5.0;

contract faucet {
	address public deployer;

	struct requester {
        address requestAddress;
        uint amount;
    }
    
    requester[] public requesters;

	constructor() public payable {
		deployer = msg.sender;
	}

	event sent(uint _amountsent);
	event received(uint amt);

	function fundFaucet()
		public
		payable
	{
		emit received(msg.value);
	}

    function sendFunds(address payable _targetAddress, uint _amt)
        public
        payable
    {
        require(msg.sender == deployer);
        require(address(this).balance >= _amt);

        _targetAddress.transfer(_amt);   
        requester memory r;
        r.requestAddress = _targetAddress;
        r.amount = _amt;
        requesters.push(r);
        emit sent(_amt);
    }
}
