from budget import Category, create_spend_chart
import pytest

@pytest.fixture
def food():
    food = Category("Food")
    return food

@pytest.fixture
def entertainment():
    entertainment = Category("Entertainment")
    return entertainment

@pytest.fixture
def business():
    business = Category("Business")
    return business

def test_deposit(food):
    food.deposit(900, "deposit")
    assert food.ledger[0] == {"amount": 900, "description": "deposit"}, 'Expected `deposit` method to create a specific object in the ledger instance variable.'


def test_deposit_no_description(food):
    food.deposit(45.56)
    assert food.ledger[0] == {"amount": 45.56, "description": ""}, 'Expected calling `deposit` method with no description to create a blank description.'

def test_withdraw(food) :
    food.deposit(900, "deposit")
    food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
    assert food.ledger[1] == {"amount": -45.67, "description": "milk, cereal, eggs, bacon, bread"}, 'Expected `withdraw` method to create a specific object in the ledger instance variable.'

def test_withdraw_no_description(food):
    food.deposit(900, "deposit")
    good_withdraw = food.withdraw(45.67)
    assert food.ledger[1] == {"amount": -45.67, "description": ""}, 'Expected `transfer` method to return `True`.'
    assert good_withdraw == True, 'Expected `withdraw` method with no description to create a blank description.'

def test_get_balance(food):
    food.deposit(900, "deposit")
    food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
    assert food.get_balance() == 854.33, 'Expected balance to be 854.33'

def test_transfer(food, entertainment):
    food.deposit(900, "deposit")
    food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
    good_transfer = food.transfer(20, entertainment)
    assert food.ledger[2] == {"amount": -20, "description": "Transfer to Entertainment"}, 'Expected `transfer` method to create a specific ledger item in food object.'
    assert good_transfer == True, 'Expected `transfer` method to return `True`.'
    assert entertainment.ledger[0] == {"amount": 20, "description": "Transfer from Food"}, 'Expected `transfer` method to create a specific ledger item in entertainment object.'


def test_check_funds(food):
    food.deposit(10, "deposit")
    assert food.check_funds(20) == False, 'Expected `check_funds` method to be False'
    assert food.check_funds(10) == True, 'Expected `check_funds` method to be True'

def test_withdraw_no_funds(food):
    food.deposit(100, "deposit")
    good_withdraw = food.withdraw(100.10)
    assert good_withdraw == False, 'Expected `withdraw` method to return `False`.'

def test_transfer_no_funds(food, entertainment):
    food.deposit(100, "deposit")
    assert food.transfer(200, entertainment) == False, 'Expected `transfer` method to return `False`.'

def test_to_string(food, entertainment):
    food.deposit(900, "deposit")
    food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
    food.transfer(20, entertainment)
    assert str(food) == f"*************Food*************\ndeposit                 900.00\nmilk, cereal, eggs, bac -45.67\nTransfer to Entertainme -20.00\nTotal: 834.33", 'Expected different string representation of object.'

def test_create_spend_chart(food, entertainment, business):
    food.deposit(900, "deposit")
    entertainment.deposit(900, "deposit")
    business.deposit(900, "deposit")
    food.withdraw(105.55)
    entertainment.withdraw(33.40)
    business.withdraw(10.99)
    expected = "Percentage spent by category\n100|          \n 90|          \n 80|          \n 70|    o     \n 60|    o     \n 50|    o     \n 40|    o     \n 30|    o     \n 20|    o  o  \n 10|    o  o  \n  0| o  o  o  \n    ----------\n     B  F  E  \n     u  o  n  \n     s  o  t  \n     i  d  e  \n     n     r  \n     e     t  \n     s     a  \n     s     i  \n           n  \n           m  \n           e  \n           n  \n           t  "
    assert create_spend_chart([business, food, entertainment]) == expected, 'Expected different chart representation. Check that all spacing is exact.'