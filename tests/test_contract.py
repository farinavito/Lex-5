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
notDepositSignee = 8
agreements_number = 1

#new safe -> 2
depositAmount2 = 10**7
depositLockTime2 = 86400 #1day
depositSignee2 = 8
notDepositSignee2 = 7
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



'''TESTING MYSAFES FUNCTION'''



def test_mySafes_emits_correct_id_accounts_1(deploy):
    '''check if the mapping mySafes emits correct agreementId for the first element in the mapping of address signee'''
    assert deploy.mySafes(accounts[depositSignee], 0) == '1'

def test_mySafes_emits_correct_id_accounts_2(deploy):
    '''check if the mapping mySafes is returning correctly the ids'''
    assert deploy.mySafes(accounts[depositSignee2], 0) == '2'



'''TESTING WITHDRAW FUNCTION'''


@pytest.mark.aaa
def test_withdraw_1st_require(deploy):
    '''check if signee is the same as the msg.sender'''
    try:
        deploy.withdraw(1, 10**5, {'from': accounts[notDepositSignee]})
    except Exception as e:
       assert e.message[50:] == "You aren't the signee"