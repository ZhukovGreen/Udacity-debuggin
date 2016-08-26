#!/usr/bin/env python
# Simple Daikon-style invariant checker
# Andreas Zeller, May 2012
# Complete the provided code around lines 28 and 44
# Do not modify the __repr__ functions.
# Modify only the classes Range and Invariants,
# if you need additional functions, make sure
# they are inside the classes.

import sys
import math
import random


def square_root(x, eps=0.00001):
    assert x >= 0
    y = math.sqrt(x)
    assert abs(square(y) - x) <= eps
    return y


def square(x):
    return x * x


# The Range class tracks the types and value ranges for a single variable.
class Range:
    def __init__(self):
        self.min = None  # Minimum value seen
        self.max = None  # Maximum value seen
        self.type = None
        self.set = set()

    # Invoke this for every value
    def track(self, value):
        if self.min > value or self.min == None:
            self.min = value
        if self.max < value or self.max == None:
            self.max = value
        self.set.add(value)
        self.type = type(value)

    # YOUR CODE

    def __repr__(self):
        return repr(self.min) + ".." + repr(self.max) + ".." + repr(self.type) + ".." + repr(self.set)


# The Invariants class tracks all Ranges for all variables seen.
class Invariants:
    def __init__(self):
        # Mapping (Function Name) -> (Event type) -> (Variable Name)
        # e.g. self.vars["sqrt"]["call"]["x"] = Range()
        # holds the range for the argument x when calling sqrt(x)
        self.vars = {}
        self.functions = {}
        self.events = {}
        self.values = {}

    def track(self, frame, event, arg):
        if event == "call" or event == "return":
            if not self.vars.has_key(frame.f_code.co_name):
                self.vars[frame.f_code.co_name] = {}
            if not self.vars[frame.f_code.co_name].has_key(event):
                self.vars[frame.f_code.co_name][event] = {}
            for var, val in frame.f_locals.iteritems():
                if not self.vars[frame.f_code.co_name][event].has_key(var):
                    self.vars[frame.f_code.co_name][event][var] = Range()
                self.vars[frame.f_code.co_name][event][var].track(val)
            if event == 'return':
                if not self.vars[frame.f_code.co_name][event].has_key('ret'):
                    self.vars[frame.f_code.co_name][event]['ret'] = Range()
                self.vars[frame.f_code.co_name][event]['ret'].track(arg)

    # YOUR CODE HERE.
    # MAKE SURE TO TRACK ALL VARIABLES AND THEIR VALUES
    # If the event is "return", the return value
    # is kept in the 'arg' argument to this function.
    # Use it to keep track of variable "ret" (return)

    def __repr__(self):
        # Return the tracked invariants
        s = ""
        for function, events in self.vars.iteritems():
            for event, vars in events.iteritems():
                s += event + " " + function + ":\n"
                # continue

                for var, range in vars.iteritems():
                    s += "    assert "
                    if range.min == range.max:
                        s += var + " == " + repr(range.min)
                    else:
                        s += repr(range.min) + " <= " + var + " <= " + repr(range.max)
                    s += "\n"
        return s


invariants = Invariants()


def traceit(frame, event, arg):
    invariants.track(frame, event, arg)
    return traceit


# Tester. Increase the range for more precise results when running locally
sys.settrace(traceit)
eps = 0.000001
for i in range(1, 10):
    r = int(random.random() * 1000)  # An integer value between 0 and 999.99
    z = square_root(r, eps)
    z = square(z)

# for r in [3, 0, 10]:
#     z = square_root(r, eps)
#     z = square(z)

sys.settrace(None)
print invariants

"""
"assert -10 <= x <= 3", "assert 0 <= ret <= 20", "assert 0.0 <= ret <= 0.544"
"""
