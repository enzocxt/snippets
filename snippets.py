#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import os
#import numpy as np
#from scipy import sparse


class Account(object):
    """A bank account that has a non-negative balance."""
    interest = 0.02     # class attribute

    def __init__(self, holder):
        self.balance = 0
        self.holder = holder

    def deposit(self, amount):
        """Increase the account balance by amount and return the new balance."""
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        """Decrease the account balance by amount and return the new balance."""
        if amount > self.balance:
            return 'Insufficient funds'
        self.balance -= amount
        return self.balance


acc = Account('Jim')
acc2 = Account('Bob')
print(hasattr(acc, 'balance'))
print(getattr(acc, 'balance'))
print(hasattr(Account, 'balance'))
print(getattr(Account, 'deposit'))

# <class 'function'>
print(type(Account.deposit))
# <class 'method'>
print(type(acc.deposit))
# 两种使用方式，和上面 hasattr(), getattr() 方法的使用类似
Account.deposit(acc, 1001)
acc.deposit(1000)

# 创建了 acc 的实例属性，它的修改不会改变类属性的值
acc.interest = 0.08
print(Account.interest)
# acc2 的实例属性不存在，所以使用的是 Account 的类属性
print(acc2.interest)


class CheckingAccount(Account):
    """A bank account that charges for withdrawals."""
    withdraw_charge = 1
    interest = 0.01

    def withdraw(self, amount):
        return Account.withdraw(self, amount + self.withdraw_charge)


ch = CheckingAccount('Tom')
print(ch.interest)


class SavingsAccount(Account):
    deposit_charge = 2

    def deposit(self, amount):
        return Account.deposit(self, amount - self.deposit_charge)


class AsSeenOnTVAccount(CheckingAccount, SavingsAccount):
    def __init__(self, account_holder):
        self.holder = account_holder
        self.balance = 1  # A free dollar!


such_a_deal = AsSeenOnTVAccount('John')
print(such_a_deal.balance)          # 1
print(such_a_deal.deposit(20))      # 19
print(such_a_deal.withdraw(5))      # 13
print(such_a_deal.deposit_charge)   # 2
print(such_a_deal.withdraw_charge)  # 1


from math import atan2, sin, cos
from fractions import gcd


def add_complex(z1, z2):
    return ComplexRI(z1.real + z2.real, z1.imag + z2.imag)

def mul_complex(z1, z2):
    return ComplexMA(z1.magnitude * z2.magnitude, z1.angle + z2.angle)


class ComplexRI(object):
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    @property
    def magnitude(self):
        return (self.real ** 2 + self.imag ** 2) ** 0.5

    @property
    def angle(self):
        return atan2(self.imag, self.real)

    def __add__(self, other):
        add_complex(self, other)

    def __mul__(self, other):
        mul_complex(self, other)

    def __repr__(self):
        return 'ComplexRI({0}, {1})'.format(self.real, self.imag)

class ComplexMA(object):
    def __init__(self, magnitude, angle):
        self.magnitude = magnitude
        self.angle = angle

    @property
    def real(self):
        return self.magnitude * cos(self.angle)

    @property
    def imag(self):
        return self.magnitude * sin(self.angle)

    def __add__(self, other):
        add_complex(self, other)

    def __mul__(self, other):
        mul_complex(self, other)

    def __repr__(self):
        return 'ComplexMA({0}, {1})'.format(self.magnitude, self.angle)


class Rational(object):
    def __init__(self, numer, denom):
        g = gcd(numer, denom)
        self.numer = numer // g
        self.denom = denom // g

    def __repr__(self):
        return 'Rational({0}, {1})'.format(self.numer, self.denom)


def add_rational(x, y):
    nx, dx = x.numer, x.denom
    ny, dy = y.numer, y.denom
    return Rational(nx * dy + ny * dx, dx * dy)

def mul_rational(x, y):
    return Rational(x.numer * y.numer, x.denom * y.denom)

def iscomplex(z):
    return type(z) in (ComplexRI, ComplexMA)

def isrational(z):
    return type(z) == Rational

def add_complex_and_rational(z, r):
    return ComplexRI(z.real + r.numer / r.denom, z.imag)

def add_ifelse(z1, z2):
    """Add z1 and z2, which may be complex or rational."""
    if iscomplex(z1) and iscomplex(z2):
        return add_complex(z1, z2)
    elif iscomplex(z1) and isrational(z2):
        return add_complex_and_rational(z1, z2)
    elif isrational(z1) and iscomplex(z2):
        return add_complex_and_rational(z2, z1)
    else:
        return add_rational(z1, z2)

def type_tag(x):
    return type_tag.tags[type(x)]
type_tag.tags = {ComplexRI: 'com', ComplexMA: 'com', Rational: 'rat'}

def add(z1, z2):
    types = (type_tag(z1), type_tag(z2))
    return add.implementations[types](z1, z2)
add.implementations = {('com', 'com'): add_complex,
                       ('com', 'rat'): add_complex_and_rational,
                       ('rat', 'com'): add_complex_and_rational,
                       ('rat', 'rat'): add_rational}

print(add(ComplexRI(1.5, 0), Rational(3, 2)))
print(add(Rational(5, 3), Rational(1, 2)))

