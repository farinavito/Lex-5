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