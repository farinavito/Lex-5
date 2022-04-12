from itertools import chain
import pytest
import brownie
from brownie import *
from brownie import accounts
from brownie.network import rpc
from brownie.network.state import Chain

depositAmount = 10**6
depositLockTime = 86400 #1day
depositSignee = 9
agreements_number = 1

@pytest.fixture(autouse=True)
def deploy(LockMyFunds):
    return LockMyFunds.deploy({'from': accounts[0]})

@pytest.fixture(autouse=True)
def deploy_newsafe(deploy):
    return deploy.deposit(depositAmount, depositLockTime, {'from': accounts[depositSignee]})



'''TESTING DEPOSIT FUNCTION'''



def test_exactSafe_id(deploy):
    '''check if the first id of the safe is one'''
    assert deploy.exactSafe(agreements_number)[0] == str(agreements_number)

def test_exactSafe_signee(deploy):
    '''check if the first signe of the safe is accounts[9]'''
    assert deploy.exactSafe(agreements_number)[1] == accounts[depositSignee]

def test_exactSafe_balances(deploy):
    '''check if the first balances of the safe is depositAmount'''
    assert deploy.exactSafe(agreements_number)[2] == depositAmount