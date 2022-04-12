from itertools import chain
import pytest
import brownie
from brownie import *
from brownie import accounts
from brownie.network import rpc
from brownie.network.state import Chain

#new safe -> 1
depositAmount = 10**6
depositLockTime = 86400 #1day
depositSignee = 9
agreements_number = 1

#new safe -> 2
depositAmount2 = 10**7
depositLockTime2 = 86400 #1day
depositSignee2 = 8
agreements_number2 = 2

@pytest.fixture(autouse=True)
def deploy(LockMyFunds):
    return LockMyFunds.deploy({'from': accounts[0]})

chain = Chain()
deploymentTime = chain.time()
@pytest.fixture(autouse=True)
def deploy_newsafe(deploy):
    return deploy.deposit(depositAmount, depositLockTime, {'from': accounts[depositSignee]})

chain = Chain()
deploymentTime2 = chain.time()
@pytest.fixture(autouse=True)
def deploy_newsafe2(deploy):
    return deploy.deposit(depositAmount2, depositLockTime2, {'from': accounts[depositSignee2]})


'''TESTING DEPOSIT FUNCTION FOR SAFE 1'''



def test_exactSafe_id(deploy):
    '''check if the first id of the safe is one'''
    assert deploy.exactSafe(agreements_number)[0] == str(agreements_number)

def test_exactSafe_signee(deploy):
    '''check if the first signe of the safe is accounts[9]'''
    assert deploy.exactSafe(agreements_number)[1] == accounts[depositSignee]

def test_exactSafe_balances(deploy):
    '''check if the first balances of the safe is depositAmount'''
    assert deploy.exactSafe(agreements_number)[2] == depositAmount

def test_exactSafe_lockedUpTime(deploy):
    '''check if the first lockedUpTime of the safe is depositAmount'''
    assert deploy.exactSafe(agreements_number)[3] == depositLockTime + deploymentTime + 13



'''TESTING DEPOSIT FUNCTION FOR SAFE 2'''



def test_exactSafe_id_2(deploy):
    '''check if the first id of the safe is one'''
    assert deploy.exactSafe(agreements_number2)[0] == str(agreements_number2)

def test_exactSafe_signee_2(deploy):
    '''check if the first signe of the safe is accounts[9]'''
    assert deploy.exactSafe(agreements_number2)[1] == accounts[depositSignee2]

def test_exactSafe_balances_2(deploy):
    '''check if the first balances of the safe is depositAmount'''
    assert deploy.exactSafe(agreements_number2)[2] == depositAmount2

def test_exactSafe_lockedUpTime_2(deploy):
    '''check if the first lockedUpTime of the safe is depositAmount'''
    assert deploy.exactSafe(agreements_number2)[3] == depositLockTime2 + deploymentTime2 + 18