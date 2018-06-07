#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cleartax_assignments` package."""

import pytest
import json
import os

from cleartax_assignments import cleartax_assignments as ca


cur_path = os.path.dirname(__file__)


with open(os.path.join(cur_path, 'eg.json')) as file:
    input_1 = ca.JsonToExpression(json.load(file))
with open(os.path.join(cur_path, 'eg1.json')) as file:
    input_2 = ca.JsonToExpression(json.load(file))
with open(os.path.join(cur_path, 'eg2.json')) as file:
    input_3 = ca.JsonToExpression(json.load(file))

def test_to_string():
    assert input_1.to_string() == "(x * 10) + 1 = 21"
    assert input_2.to_string() == "((25 + 10) / 70) - (x / (3 + 6)) = 21"
    assert input_3.to_string() == "x = 21"

def test_change_sides():
    changed_input1 = ca.JsonToExpression(input_1.change_sides())
    changed_input2 = ca.JsonToExpression(input_2.change_sides())
    changed_input3 = ca.JsonToExpression(input_3.change_sides())

    assert changed_input1.to_string() == "x = (21 - 1) / 10"
    assert changed_input2.to_string() == "x = (((25 + 10) / 70) - 21) * (3 + 6)"
    assert changed_input3.to_string() == "x = 21"

def test_evaluate_eq():
    assert round(input_1.evaluate_eq(), 2) == 2.00
    assert round(input_2.evaluate_eq(), 2) == -184.50
    assert round(input_3.evaluate_eq(), 2) == 21.00

