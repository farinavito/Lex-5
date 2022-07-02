from itertools import chain
import pytest
import brownie
from brownie import *
from brownie import accounts
from brownie.network import rpc
from brownie.network.state import Chain

sleeping_time = [86400, 604800, 2629743, 31556926]

#new safe -> 1
depositAmount = 10**6
moreThanDepoitAmount = [10**7, 10**8, 10**9]
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
    return deploy.deposit(depositLockTime, {'from': accounts[depositSignee], 'value': depositAmount})


chain = Chain()
deploymentTime2 = chain.time()
@pytest.fixture(autouse=True)
def deploy_newsafe2(deploy):
    return deploy.deposit(depositLockTime2, {'from': accounts[depositSignee2], 'value': depositAmount2})



'''TESTING DEPOSIT FUNCTION FOR SAFE 1'''



def test_exactSafe_id(deploy):
    '''check if the first id of the safe is one'''
    assert deploy.exactSafe(agreements_number)[0] == str(agreements_number)

def test_exactSafe_signee(deploy):
    '''check if the first signee of the safe is accounts[9]'''
    assert deploy.exactSafe(agreements_number)[1] == accounts[depositSignee]

def test_exactSafe_balances(deploy):
    '''check if the first balances of the safe is depositAmount'''
    assert deploy.exactSafe(agreements_number)[2] == depositAmount

def test_exactSafe_lockedUpTime(deploy):
    '''check if the first lockedUpTime of the safe is depositAmount'''
    assert deploy.exactSafe(agreements_number)[3] - 9 == depositLockTime + deploymentTime 

def test_deposit_0(deploy):
    '''Check if the require statement works correctly'''
    try:
        deploy.deposit(depositLockTime, {'from': accounts[depositSignee], 'value': 0})
        pytest.fail("The try-except concept has failed in test_deposit_0")
    except Exception as e:
       assert e.message[50:] == "Please deposit more than 0"
    


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
    assert deploy.exactSafe(agreements_number2)[3] == depositLockTime2 + deploymentTime2 + 11



'''TESTING MYSAFES FUNCTION'''



def test_mySafes_emits_correct_id_accounts_1(deploy):
    '''check if the mapping mySafes emits correct agreementId for the first element in the mapping of address signee'''
    assert deploy.mySafes(accounts[depositSignee], 0) == '1'

def test_mySafes_emits_correct_id_accounts_1_2nd(deploy):
    '''check if the mapping mySafes emits correct agreementId for the second element in the mapping of address signee'''
    deploy.deposit(depositLockTime, {'from': accounts[depositSignee], 'value': depositAmount})
    assert deploy.mySafes(accounts[depositSignee], 1) == '3'

def test_mySafes_emits_correct_id_accounts_2(deploy):
    '''check if the mapping mySafes is returning correctly the ids'''
    assert deploy.mySafes(accounts[depositSignee2], 0) == '2'



'''TESTING WITHDRAW FUNCTION'''



def test_withdraw_1st_require(deploy):
    '''check if signee is the same as the msg.sender'''
    try:
        deploy.withdraw(agreements_number, depositAmount, {'from': accounts[notDepositSignee]})
        pytest.fail("The try-except concept has failed in test_withdraw_1st_require")
    except Exception as e:
       assert e.message[50:] == "You aren't the signee"

def test_withdraw_2nd_require(deploy):
    '''check if lock up time has ended'''
    try:
        deploy.withdraw(agreements_number, depositAmount, {'from': accounts[depositSignee]})
        pytest.fail("The try-except concept has failed in test_withdraw_2nd_require")
    except Exception as e:
       assert e.message[50:] == "The lock up time hasn't ended yet"

@pytest.mark.parametrize("sleep_time", [sleeping_time[0], sleeping_time[1], sleeping_time[2], sleeping_time[3]])
@pytest.mark.parametrize("amount_sent", [moreThanDepoitAmount[0], moreThanDepoitAmount[1], moreThanDepoitAmount[2]])
def test_withdraw_3rd_require(deploy, sleep_time, amount_sent):
    '''check if the balance is big enough'''
    try:
        chain = Chain()
        chain.sleep(sleep_time)
        deploy.withdraw(agreements_number, amount_sent, {'from': accounts[depositSignee]})
        pytest.fail("The try-except concept has failed in test_withdraw_3rd_require")
    except Exception as e:
       assert e.message[50:] == "Not enough funds"

@pytest.mark.parametrize("sleep_time", [sleeping_time[0], sleeping_time[1], sleeping_time[2], sleeping_time[3]])
def test_withdraw_all(deploy, sleep_time):
    '''check if the balance is zero when everything is withdrawn'''
    chain = Chain()
    chain.sleep(sleep_time)
    deploy.withdraw(agreements_number, depositAmount, {'from': accounts[depositSignee]})
    assert deploy.exactSafe(agreements_number)[2] == 0
  
@pytest.mark.parametrize("sleep_time", [sleeping_time[0], sleeping_time[1], sleeping_time[2], sleeping_time[3]])
@pytest.mark.parametrize("less_amount", [depositAmount - 10**2, depositAmount - 10**3, depositAmount - 10**4])
def test_withdraw_less(deploy, sleep_time, less_amount):
    '''check if the balance is reduced when an amount is withdrawn'''
    funds = deploy.exactSafe(agreements_number)[2]
    chain = Chain()
    chain.sleep(sleep_time)
    deploy.withdraw(agreements_number, less_amount, {'from': accounts[depositSignee]})
    assert deploy.exactSafe(agreements_number)[2] == funds - less_amount

@pytest.mark.parametrize("sleep_time", [sleeping_time[0], sleeping_time[1], sleeping_time[2], sleeping_time[3]])
@pytest.mark.parametrize("_amount", [depositAmount, depositAmount - 10**2, depositAmount - 10**3, depositAmount - 10**4])
def test_withdraw_emit_event(deploy, sleep_time, _amount):
    '''check if the event is emited when we withdraw the balance'''
    chain = Chain()
    chain.sleep(sleep_time)
    function_initialize = deploy.withdraw(agreements_number, _amount, {'from': accounts[depositSignee]})
    assert function_initialize.events[0][0]['quantity'] == _amount



'''TEST GETMYNUMSAFES'''



@pytest.mark.parametrize("users", [7, 6, 5, 4, 3])
def test_getMyNumSafes_initialize_to_zero(deploy, users):
    '''check if the caller's getMyNumSafes is initialized to zero'''
    try:
        deploy.getMyNumSafes({'from': accounts[users]}) == 0
        pytest.fail("The try-except concept has failed in test_withdraw_3rd_require")
    except Exception as e:
       assert e.message[50:] == "You don't have any depozits"
@pytest.mark.aaa
@pytest.mark.parametrize("users", [7, 6, 5, 4, 3])
@pytest.mark.parametrize("loops", [2, 3, 4, 5, 6])
def test_getMyNumSafes_numbers(deploy, users, loops):
    '''check if the caller's getMyNumSafes returnes correct number'''
    for _ in range(1, loops):
        deploy.deposit(depositLockTime, {'from': accounts[users], 'value': depositAmount})
    deploy.getMyNumSafes({'from': accounts[users]}) == loops - 1