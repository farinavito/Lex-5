// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

/// @title This smart contract enables you to lock your funds for the time you choose
/// @author Farina Vito

contract LockMyFunds {

    struct Funds{
        uint256 id; 
        address signee;
        uint256 balances;
        uint256 lockedUpTime;
    }

    /// @notice Using against re-entrancy
    uint16 internal locked = 1;

    /// @notice Used to increase the id of the agreements in the "createAgreements" function
    uint numAgreement = 1;

    /// @notice Doesn't allow reentrance attack
    modifier noReentrant() {
        require(locked == 1, "No re-entrancy");
        locked = 2;
        _;
        locked = 1;
    }

    /// @notice A unique identifier of the agreement. The same as the id.
    mapping(uint256 => Funds) public exactSafe;

    /// @notice Storing the id's of the safes that the signee has created
    mapping(address => uint[]) public mySafes;

    /// @notice After other event than Terminated happens, emit it and send a message
    event NotifyUser(uint256 quantity);

    function deposit(uint256 _lockTime) external payable {
        //increment the agreement id
        uint256 agreementId = numAgreement++;
        //initialize a new safe
        Funds storage newSafe = exactSafe[agreementId];
        //initialize id
        newSafe.id = agreementId;
        //initialize the variable to msg.sender
        newSafe.signee = msg.sender;
        //add how much you want to lock
        newSafe.balances = msg.value;
        //add how long you want to lock it for
        newSafe.lockedUpTime = block.timestamp + _lockTime;
        //storing the ids of the safes and connecting them to msg.sender's address so we can display them to the frontend
        mySafes[msg.sender].push(agreementId);
    }

    function withdraw(uint256 _id, uint256 _quantity) external payable noReentrant{
        //checking if the signee is the same as the msg.sender
        require(exactSafe[_id].signee == msg.sender, "You aren't the signee");
        //checking if the lock up time has ended
        require(exactSafe[_id].lockedUpTime <= block.timestamp, "The lock up time hasn't ended yet");
        //checking if the balance is big enough 
        require(exactSafe[_id].balances >= _quantity, "Not enough funds");
        //send the funds
        (bool sent, ) = msg.sender.call{value: _quantity}("");
        require(sent, "Failed to send Ether");
        //reduce the balance
        exactSafe[_id].balances -= _quantity;
        //emit the event
        emit NotifyUser(_quantity);  
    }

    fallback() external {}
    receive() external payable {}
}