
pragma solidity ^0.7.5;

contract faucet {
	address public deployer;

	struct requester {
        address requesteraddress;
        uint amount;
    }
    
    requester[] public requesters;

	constructor() public payable {
		deployer = msg.sender;
	}

	event sent(uint _amountsent);
	event received(uint amt);

    // function testFunc(address payable adr) returns(address ret){
    //     return adr;
    // }

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
        r.requesteraddress = _targetAddress;
        r.amount = _amt;
        requesters.push(r);
        emit sent(_amt);
    }
}