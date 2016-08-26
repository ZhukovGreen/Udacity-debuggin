# Your task for this assignment is to combine the principles that you learned
# in unit 3, 4 and 5 and create a fully automated program that can display
# the cause-effect chain automatically.
# In problem set 4 you created a program that generated cause chain
# if you provided it the locations (line and iteration number) to look at.
# That is not very useful. If you know the lines to look for changes, you
# already know a lot about the cause. Instead now, with the help of concepts
# introduced in unit 5 (line coverage), improve this program to create
# the locations list automatically, and then use it to print out only the
# failure inducing lines, as before.
# See some hints at the provided functions, and an example output at the end.
import sys
import copy
import math


# buggy program
def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:

        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif c == '"' or c == "'" and tag:
            quote = not quote
        elif not tag:
            out = out + c

    return out


failing_path = {}


def failing_run_trace(frame, event, arg):
    global failing_path
    if event == 'line':
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        if failing_path:
            iteration = max(failing_path[filename].iterkeys())
        else:
            iteration = 1

        if not failing_path.has_key(filename):
            failing_path[filename] = {}
        if iteration not in failing_path[filename]:
            failing_path[filename][iteration] = []
        if lineno in failing_path[filename][iteration]:
            iteration += 1
            failing_path[filename][iteration] = []

        failing_path[filename][iteration].append(lineno)
    return failing_run_trace


def failing_run():
    sys.settrace(failing_run_trace)
    remove_html_markup(html_fail)
    sys.settrace(None)
    return failing_path


def ddmin(s):
    # you may need to use this to test if the values you pass actually make
    # test fail.
    # assert test(s) == "FAIL"

    n = 2  # Initial granularity
    while len(s) >= 2:
        # print 'new run 1', s
        start = 0
        subset_length = len(s) / n
        some_complement_is_failing = False
        while start < len(s):
            # print 'new run 2'
            complement = s[:start] + s[start + subset_length:]
            # print 'complement ', complement
            if test(complement) == "FAIL":
                s = complement
                n = max(n - 1, 2)
                some_complement_is_failing = True
                break

            start += subset_length

        if not some_complement_is_failing:
            if n == len(s):
                break
            n = min(n * 2, len(s))
    # print 'final cause is: ', s
    return s


# Use this function to record the covered lines in the program, in order of
# their execution and save in the list coverage
coverage = {}


def traceit(frame, event, arg):
    global coverage

    # YOUR CODE HERE
    if event == "line":
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        if coverage:
            iteration = max(coverage[filename].iterkeys())
        else:
            iteration = 1

        if not coverage.has_key(filename):
            coverage[filename] = {}

        if not coverage[filename].has_key(iteration):
            coverage[filename][iteration] = {}

        if lineno in coverage[filename][iteration].iterkeys():
            iteration += 1
            coverage[filename][iteration] = {}

        coverage[filename][iteration][lineno] = True
    return traceit


# We use these variables to communicate between callbacks and drivers
the_line = None
__the_lines_history = None
the_iteration = None
the_cur_iter = None
the_state = {}
the_diff = None
the_diff_history = None
the_input = None


# Stop at THE_LINE/THE_ITERATION and store the state in THE_STATE
def trace_fetch_state(frame, event, arg):
    global the_line
    global the_iteration
    global the_state
    if frame.f_lineno == the_line:
        the_iteration -= 1
        if the_iteration == 0:
            the_state = copy.deepcopy(frame.f_locals)
            the_line = None  # Don't get called again
            return None  # Don't get called again
    return trace_fetch_state


# Get the state at LINE/ITERATION
def get_state(input, line, iteration):
    global the_line
    global the_iteration
    global the_state

    the_state = {}
    the_line = line
    the_iteration = iteration
    sys.settrace(trace_fetch_state)
    y = remove_html_markup(input)
    sys.settrace(None)

    return the_state


# Stop at THE_LINE/THE_ITERATION and apply the differences in THE_DIFF
def trace_apply_diff(frame, event, arg):
    global the_line
    global the_diff
    global the_diff_history
    global the_iteration
    global the_cur_iter
    global __the_lines_history

    __the_lines_history.append(frame.f_lineno)
    the_cur_iter = max(__the_lines_history.count(frame.f_lineno), the_cur_iter)

    # for i, cover in the_diff_history.items():
    #     for l, d in cover.items():
    #         if i == the_cur_iter and l == frame.f_lineno:
    #             try:
    #                 d.remove([a for a in d if 's' in a][0])
    #                 d.remove([a for a in d if 'out' in a][0])
    #                 d.remove([a for a in d if 'c' in a][0])
    #             except:
    #                 pass
    #             print 'updated with ', d, i, l
    #             frame.f_locals.update(d)

    if frame.f_lineno == the_line and the_iteration == the_cur_iter:
        frame.f_locals.update(the_diff)
        the_line = None
        # print 'last time', the_diff, the_iteration, frame.f_lineno
        return None  # Don't get called again

    return trace_apply_diff


# Testing function: Call remove_html_output, stop at THE_LINE/THE_ITERATION,
# and apply the diffs in DIFFS at THE_LINE
def test(diffs):
    # print '\n\ntest started!!!!\n'
    global the_diff
    global the_input
    global the_line
    global the_iteration
    global __the_lines_history
    global the_cur_iter

    line = the_line
    iteration = the_iteration
    __the_lines_history = []
    the_cur_iter = 1

    the_diff = diffs
    # print 'inside test', (the_diff, the_line, the_iteration)
    # print the_diff
    sys.settrace(trace_apply_diff)
    y = remove_html_markup(the_input)
    sys.settrace(None)

    the_line = line
    the_iteration = iteration

    if y.find('<') == -1:
        return "PASS"
    else:
        # print '\ntest failed!!!!\n'
        return "FAIL"


def phi(n11, n10, n01, n00):
    try:
        return ((n11 * n00 - n10 * n01) /
                math.sqrt((n10 + n11) * (n01 + n00) * (n10 + n00) * (n01 + n11)))
    except:
        return -1


# Run the program with each test case and record
# input, outcome and coverage of lines
def run_tests(inputs):
    runs = []
    for input in inputs:
        global coverage
        coverage = {}
        sys.settrace(traceit)
        result = remove_html_markup(input)
        sys.settrace(None)
        if result.find('<') == -1:
            outcome = "PASS"
        else:
            outcome = "FAIL"

        runs.append((input, outcome, coverage))
    return runs


# Create empty tuples for each covered line
def init_tables(runs):
    tables = {}
    for (input, outcome, coverage) in runs:
        for filename, iterations in coverage.iteritems():
            for iteration, lines in iterations.iteritems():
                for line in lines.keys():
                    if not tables.has_key(filename):
                        tables[filename] = {}
                    if not tables[filename].has_key(iteration):
                        tables[filename][iteration] = {}
                    if not tables[filename][iteration].has_key(line):
                        tables[filename][iteration][line] = (0, 0, 0, 0)
    return tables


# Compute n11, n10, etc. for each line
def compute_n(tables, runs):
    for filename, iterations in tables.iteritems():
        for iteration, lines in iterations.iteritems():
            for line in lines.keys():
                (n11, n10, n01, n00) = tables[filename][iteration][line]
                for (input, outcome, coverage) in runs:
                    if coverage.has_key(filename) and coverage[filename].has_key(iteration) and coverage[filename][
                        iteration].has_key(line):
                        # Covered in this run
                        if outcome == "FAIL":
                            n11 += 1  # covered and fails
                        else:
                            n10 += 1  # covered and passes
                    else:
                        # Not covered in this run
                        if outcome == "FAIL":
                            n01 += 1  # uncovered and fails
                        else:
                            n00 += 1  # uncovered and passes
                tables[filename][iteration][line] = phi(n11, n10, n01, n00)
    return tables


def make_locations(coverage):
    # YOUR CODE HERE
    # This function should return a list of tuples in the format
    # [(line, iteration), (line, iteration) ...], as auto_cause_chain
    # expects.
    locations = []
    runs = run_tests([html_fail, html_pass])
    tables = init_tables(runs)

    resume = True
    for filename, iterations in compute_n(tables, runs).iteritems():
        for iteration, lines_phi in iterations.iteritems():
            for line, phi in lines_phi.iteritems():
                if phi > 0 and resume:
                    # locations.append((line - 1, iteration))
                    locations.append((line, iteration))
                    if line == 32:
                        resume = False
    # print locations
    return locations


def auto_cause_chain(locations):
    global html_fail, html_pass, the_input, the_line, the_iteration, the_diff, failing_path, the_diff_history

    failing_path = failing_run()

    print "The program was started with", repr(html_fail)
    diffs = {}
    # Test over multiple locations
    pr_line = None
    pr_iteration = None
    for filename, cover in failing_path.items():
        for iteration, lines in cover.items():
            for line in lines:
                # Get the passing and the failing state
                state_pass = get_state(html_pass, line, iteration)
                state_fail = get_state(html_fail, line, iteration)

                # print iteration, line, 'P: ', state_pass, 'F: ', state_fail

                if pr_line == None:
                    pr_line = line
                    pr_iteration = iteration

                if pr_iteration not in diffs:
                    diffs[pr_iteration] = {}
                diffs[pr_iteration][pr_line] = []
                # Compute the differences
                for var in state_fail.keys():
                    # print line, var, state_pass, state_fail
                    if not state_pass.has_key(var) or state_pass[var] != state_fail[var]:
                        diffs[pr_iteration][pr_line].append((var, state_fail[var]))
                pr_line = line
                pr_iteration = iteration

        # Minimize the failure-inducing set of differences
        # Since this time you have all the covered lines and iterations in
        # locations, you will have to figure out how to automatically detect
        # which lines/iterations are the ones that are part of the
        # failure chain and print out only these.
        the_input = html_pass
        # You will have to use the following functions and output formatting:
        #    cause = ddmin(diffs)
        #    # Pretty output
        #    print "Then", var, "became", repr(value)
        the_diff_history = diffs
        # print the_diff_history
        for line, iteration in locations:
            the_iteration = iteration
            the_line = line
            cause = ddmin(diffs[iteration][line])
            # print cause
            # Pretty output
            print "Then, in Line " + repr(line) + " (iteration " + repr(iteration) + "),",
            for (var, value) in cause:
                print var, 'became', repr(value)

        print "Then the program failed."


###### Testing runs

# We will test your function with different strings and on a different function
html_fail = '"<b>foo</b>"'
html_pass = "'<b>foo</b>'"

# This will fill the coverage variable with all lines executed in a
# failing run
# coverage = {}
# sys.settrace(traceit)
# remove_html_markup(html_fail)
# sys.settrace(None)

locations = make_locations(coverage)
auto_cause_chain(locations)

# The coverage :
# [8, 9, 10, 11, 12, 14, 16, 17, 11, 12... # and so on
# The locations:
# [(8, 1), (9, 1), (10, 1), (11, 1), (12, 1)...  # and so on
# The output for the current program and test strings should look like follows:
"""
The program was started with '"<b>foo</b>"'
Then s became '"<b>foo</b>"'
Then c became '"'
Then quote became True
...
"""
