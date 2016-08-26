#!/usr/bin/env python
# Simple debugger
# See instructions around line 34
import sys

"""import readline"""


# Our buggy program
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


# main program that runs the buggy program
def main():
    remove_html_markup('"<b>foo</b>"')


"""
Our traceit function
Improve the traceit function to watch for variables in the watchpoint
dictionary and print out (literally like that):
event, frame.f_lineno, frame.f_code.co_name
and then the values of the variables, each in new line, in a format:
somevar ":", "Initialized"), "=>", repr(somevalue)
if the value was not set, and got set in the line, or
somevar ":", repr(old-value), "=>", repr(new-value)
when the value of the variable has changed.
If the value is unchanged, do not print anything.
"""


def debug(command, my_locals):
    global stepping
    global breakpoints
    global watchpoints

    if command.find(' ') > 0 and command[0] != 'd':
        arg = command.split(' ')[1]
    elif command.startswith('d'):
        d_type, d_arg = command.split(' ')[1], command.split(' ')[2]
        arg = None
    else:
        arg = None

    if command.startswith('s'):  # step
        stepping = True
        return True
    elif command.startswith('c'):  # continue
        stepping = False
        return True
    elif command.startswith('p'):  # print
        if arg:
            if arg in my_locals:
                print arg, "=", repr(my_locals[arg])
            else:
                print "No such variable:", arg
        else:
            print my_locals
        return False
    elif command.startswith('b'):  # breakpoint
        if not arg:
            print "You must supply a line number"
        else:
            breakpoints[int(arg)] = True
        return True
    elif command.startswith('w'):  # watch variable
        if not arg:
            print "You must supply a variable name"
        else:
            watchpoints[arg] = []
        return True
    # PS1 CODE
    elif command.startswith('d'):  # delete watch/break point
        if (d_type == 'b' and not isinstance(int(d_arg), int)) or (d_type == 'w' and not isinstance(d_arg, str)) or (
                    d_type not in 'bw'):
            print 'Incorrect command'
            raise RuntimeError
        if d_type == 'b':
            d_arg = int(d_arg)
            try:
                breakpoints.pop(d_arg)
                pass
            except:
                print 'No such breakpoint defined'
        else:
            try:
                watchpoints.pop(d_arg)
            except:
                print 'is not defined as watchpoint'
        return True
    elif command.startswith('q'):  # quit
        print "Exiting my-spyder..."
        sys.exit(0)
    else:
        print "No such command", repr(command)
    return False


def input_command():
    # command = raw_input("(my-spyder) ")
    global commands
    command = commands.pop(0)
    return command


"""
Our traceit function
"""


def traceit(frame, event, trace_arg):
    global stepping
    global watchpoints

    if event == 'line':
        # print '***',event, frame.f_lineno, frame.f_code.co_name
        if stepping or breakpoints.has_key(frame.f_lineno):
            resume = False
            while not resume:
                command = input_command()
                resume = debug(command, frame.f_locals)
        if len(watchpoints) != 0:
            out = ''
            for var, arg in frame.f_locals.iteritems():
                if var in watchpoints:
                    watchpoints[var].append(arg)
                    if len(watchpoints[var]) == 1:
                        out += var + " : Initialized => " + repr(arg)
                    elif watchpoints[var][-1] != watchpoints[var][-2]:
                        out += var + " :" + repr(watchpoints[var][-2]) + " => " + repr(arg)
            if out != '':
                print event, frame.f_lineno, frame.f_code.co_name
                print out
    return traceit


# globals
breakpoints = {}
watchpoints = {"quote": []}
watch_values = {}
stepping = True

commands = ["w c", "c", "c", "w out", "c", "c", "c", "q"]

# Using the tracer
sys.settrace(traceit)
main()
sys.settrace(None)

# with the commands = ["w c", "c", "c", "w out", "c", "c", "c", "q"],
# the output should look like this (line numbers may be different):
# line 26 main {}
# line 10 remove_html_markup
# quote : Initialized => False
# line 13 remove_html_markup
# c : Initialized => '"'
# line 19 remove_html_markup
# quote : False => True
# line 13 remove_html_markup
# c : '"' => '<'
# line 21 remove_html_markup
# out : '' => '<'
# Exiting my-spyder...
