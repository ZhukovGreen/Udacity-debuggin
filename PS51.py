import sys
import math

# INSTRUCTIONS !
# This provided, working code calculates phi coefficients for each code line.
# Make sure that you understand how this works, then modify the traceit
# function to work for function calls instead of lines. It should save the
# function name and the return value of the function for each function call.
# Use the mystery function that can be found at line 155 and the
# test cases at line 180 for this exercise.
# Modify the provided functions to use this information to calculate
# phi values for the function calls as described in the video.
# You should get 3 phi values for each function - one for positive values (1),
# one for 0 values and one for negative values (-1), called "bins" in the video.
# When you have found out which function call and which return value type (bin)
# correlates the most with failure, fill in the following 3 variables,
# Do NOT set these values dynamically.
answer_function = "f3"  # One of f1, f2, f3
answer_bin = -1  # One of 1, 0, -1
answer_value = 0.8165  # precision to 4 decimal places.

# global variable to keep the coverage data in
coverage = {}
function_subtypes = ['positive', 'negative', 'zero']


# Tracing function that saves the coverage data
# To track function calls, you will have to check 'if event == "return"', and in
# that case the variable arg will hold the return value of the function,
# and frame.f_code.co_name will hold the function name
def traceit(frame, event, arg):
    global coverage

    if event == "return":
        filename = frame.f_code.co_filename
        functionname = frame.f_code.co_name
        if not coverage.has_key(filename):
            coverage[filename] = {}
        if functionname != 'mystery':
            coverage[filename][functionname] = arg
    return traceit


# Calculate phi coefficient from given values
def phi(n11, n10, n01, n00):
    return ((n11 * n00 - n10 * n01) /
            math.sqrt((n10 + n11) * (n01 + n00) * (n10 + n00) * (n01 + n11)))


# Print out values of phi, and result of runs for each covered line
def print_tables(tables):
    for filename, function_subtypes in tables.iteritems():
        print(filename)
        for function_subtype, functions in function_subtypes.iteritems():
            print(function_subtype)
            for function, vals in functions.iteritems():
                (n11, n10, n01, n00) = vals
                try:
                    factor = phi(n11, n10, n01, n00)
                    prefix = "%+.4f%2d%2d%2d%2d" % (factor, n11, n10, n01, n00)
                except:
                    prefix = "       %2d%2d%2d%2d" % (n11, n10, n01, n00)
                print(prefix, "    ", function)


# Run the program with each test case and record
# input, outcome and coverage of lines
def run_tests(inputs):
    runs = []
    for input in inputs:
        global coverage
        coverage = {}
        sys.settrace(traceit)
        result = mystery(input)
        sys.settrace(None)
        runs.append((input, result, coverage))
    return runs


# Create empty tuples for each covered line
def init_tables(runs):
    tables = {}
    for (input, outcome, coverage) in runs:
        for filename, functions in coverage.iteritems():
            if filename not in tables:
                tables[filename] = {}
            for function in functions.keys():
                for function_subtype in function_subtypes:
                    if function_subtype not in tables[filename]:
                        tables[filename][function_subtype] = {}
                    tables[filename][function_subtype][function] = (0, 0, 0, 0)
    return tables


# Compute n11, n10, etc. for each line
def compute_n(tables):
    for filename, function_subtypes in tables.iteritems():
        for function_subtype, functions in function_subtypes.iteritems():
            for function in functions.keys():
                (n11, n10, n01, n00) = tables[filename][function_subtype][function]
                for (input, outcome, coverage) in runs:
                    # Covered in this run
                    if function_subtype == 'positive':
                        if outcome == "PASS" and coverage[filename][function] > 0:
                            n10 += 1
                        elif outcome == "PASS" and coverage[filename][function] <= 0:
                            n00 += 1
                        elif outcome == "FAIL" and coverage[filename][function] > 0:
                            n11 += 1
                        elif outcome == "FAIL" and coverage[filename][function] <= 0:
                            n01 += 1
                    elif function_subtype == 'negative':
                        if outcome == "PASS" and coverage[filename][function] < 0:
                            n10 += 1
                        elif outcome == "PASS" and coverage[filename][function] >= 0:
                            n00 += 1
                        elif outcome == "FAIL" and coverage[filename][function] < 0:
                            n11 += 1
                        elif outcome == "FAIL" and coverage[filename][function] >= 0:
                            n01 += 1
                    else:
                        if outcome == "PASS" and coverage[filename][function] == 0:
                            n10 += 1
                        elif outcome == "PASS" and coverage[filename][function] != 0:
                            n00 += 1
                        elif outcome == "FAIL" and coverage[filename][function] == 0:
                            n11 += 1
                        elif outcome == "FAIL" and coverage[filename][function] != 0:
                            n01 += 1

                tables[filename][function_subtype][function] = (n11, n10, n01, n00)
    return tables


# Now compute (and report) phi for each line. The higher the value,
# the more likely the line is the cause of the failures.

# These are the test cases


###### MYSTERY FUNCTION

def mystery(magic):
    assert type(magic) == tuple
    assert len(magic) == 3

    l, s, n = magic

    r1 = f1(l)

    r2 = f2(s)

    r3 = f3(n)

    if -1 in [r1, r2, r3]:
        return "FAIL"
    elif r3 < 0:
        return "FAIL"
    elif not r1 or not r2:
        return "FAIL"
    else:
        return "PASS"


# These are the input values you should test the mystery function with
inputs = [([1, 2], "ab", 10),
          ([1, 2], "ab", 2),
          ([1, 2], "ab", 12),
          ([1, 2], "ab", 21),
          ("a", 1, [1]),
          ([1], "a", 1),
          ([1, 2], "abcd", 8),
          ([1, 2, 3, 4, 5], "abcde", 8),
          ([1, 2, 3, 4, 5], "abcdefgijkl", 18),
          ([1, 2, 3, 4, 5, 6, 7], "abcdefghij", 5)]


def f1(ml):
    if type(ml) is not list:
        return -1
    elif len(ml) < 6:
        return len(ml)
    else:
        return 0


def f2(ms):
    if type(ms) is not str:
        return -1
    elif len(ms) < 6:
        return len(ms)
    else:
        return 0


def f3(mn):
    if type(mn) is not int:
        return -1
    if mn > 10:
        return -100
    else:
        return mn


runs = run_tests(inputs)
tables = init_tables(runs)
tables = compute_n(tables)
print_tables(tables)
