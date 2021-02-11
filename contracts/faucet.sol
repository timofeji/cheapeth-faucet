
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

    function sendFunds(address payable _requester, uint _request)
        public
        payable
    {
        // require(msg.sender == deployer);

        uint amountsent = 0;
        _request = _request * 1e18;
        
        if (address(this).balance > _request){
            amountsent = _request/1e18;
            _requester.transfer(_request);   
        }
        else{
            amountsent = (address(this).balance)/1e18;
            _requester.transfer(address(this).balance);
        }
        
        requester memory r;
        r.requesteraddress = _requester;
        r.amount = amountsent;
        requesters.push(r);
        emit sent(amountsent);
    }
}