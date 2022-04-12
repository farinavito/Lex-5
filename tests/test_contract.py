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

@pytest.fixture(autouse=True)
def deploy(Funds):
    return Funds

@pytest.fixture(autouse=True)
def deploy_newsafe(deploy):
    return deploy.deposit(depositAmount, depositLockTime, {'from': accounts[depositSignee]})
