# -*- coding: utf-8 -*-

"""Main module."""

class JsonToExpression():

    operators = {'equal': "=", "add": "+",
                 "subtract": "-", "multiply": "*", "divide": "/"}
    opposite_operators = {'add': 'subtract', 'subtract': 'add',
                          "multiply": "divide", "divide": "multiply"}


    def __init__(self, json_self):
        """ Initialize with JSON in form of python dictionary object."""
        self.data = json_self

    def to_string(self):
        """ Return string formed from dictionary object."""
        if (type(self.data['lhs']) is dict) and (self.data['op'] != 'equal'):
            lhs = '(' + JsonToExpression(self.data['lhs']).to_string() + ')'
        elif type(self.data['lhs']) is dict:
            lhs = JsonToExpression(self.data['lhs']).to_string()
        else:
            lhs = str(self.data['lhs'])
        if (type(self.data['rhs']) is dict) and (self.data['op'] != 'equal'):
            rhs = '(' + JsonToExpression(self.data['rhs']).to_string() + ')'
        elif type(self.data['rhs']) is dict:
            rhs = JsonToExpression(self.data['rhs']).to_string()
        else:
            rhs = str(self.data['rhs'])
        string = lhs + ' ' + self.operators[self.data['op']] + ' ' + rhs
        return (string)


    def change_sides(self):
        """ Transform input dictionary object so that only x remains on the lhs and return it. """
        left = self.data['lhs']
        right = self.data['rhs']
        if left == 'x':
            return self.data

        # if x in left subtree of lhs, follow this form and opposite operator
        #   lhs       rhs         lhs     rhs
        #  /  \        |    =>     |     /  \
        # x    a       b           x    a    b
        if 'x' in str(left['lhs']):
            right = {"lhs": right}
            right['op'] = self.opposite_operators[left['op']]
            right['rhs'] = left['rhs']
            left = left['lhs']
        # if x in right subtree of lhs, depends on operator of lhs
        else:
            # if + or *, follow this form and opposite operator
            #   lhs       rhs         lhs     rhs
            #  /  \        |    =>     |     /  \
            # a    x       b           x    b    a
            if left['op'] == 'add' or left['op'] == 'multiply':
                right = {"lhs": right}
                right['rhs'] = left['lhs']
                right['op'] = self.opposite_operators[left['op']]
                left = left['rhs']
            # else, follow this form and same operator
            #   lhs       rhs         lhs     rhs
            #  /  \        |    =>     |     /  \
            # a    x       b           x    a    b
            else:
                right = {"rhs": right}
                right['lhs'] = left['lhs']
                right['op'] = left['op']
                left = left['rhs']

        if left == 'x':
            return({"lhs": left, "rhs": right, 'op': self.data['op']})
        else:
            return(JsonToExpression({"lhs": left, "rhs": right, 'op': self.data['op']}).change_sides())


    def evaluate_eq(self):
        """ Return the result of the expression in the input dictionary. """
        # if complete equation, find x, evaluate right hand side
        if self.data['op'] == 'equal':
            self.data = JsonToExpression(self.data).change_sides()
            self.data = self.data['rhs']
        # evaluate the expressions, if present
        if type(self.data) is dict:
            # evaluate sub-tree, if necessary
            if type(self.data['lhs']) is dict:
                self.data['lhs'] = float(JsonToExpression(self.data['lhs']).evaluate_eq())
            if type(self.data['rhs']) is dict:
                self.data['rhs'] = float(JsonToExpression(self.data['rhs']).evaluate_eq())
            # perform operations
            if self.data['op'] == 'add':
                return (self.data['lhs'] + self.data['rhs'])
            elif self.data['op'] == 'subtract':
                return (self.data['lhs'] - self.data['rhs'])
            elif self.data['op'] == 'multiply':
                return (self.data['lhs'] * self.data['rhs'])
            else:
                return (self.data['lhs'] / self.data['rhs'])
        else:
            return self.data