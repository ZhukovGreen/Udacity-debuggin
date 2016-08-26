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
    print remove_html_markup('xyz')
    print remove_html_markup('"<b>foo</b>"')
    print remove_html_markup("'<b>foo</b>'")


"""
Our debug function
Improve and expand the debug function to accept a new command:
a delete command 'd <type> <argument>', where <type> is either b for breakpoint,
or w for watchpoint. The following argument should be either a number
for the breakpoint or a string for the watchpoint.
If there is mismatch between type and argument, you should print out
"Incorrect command".
In the case of "d b <argument>" you should delete that breakpoint from the
breakpoint dictionary, or print "No such breakpoint defined", repr(argument)
In case of watchpoint, you should delete the watchpoint if such variable exists,
or print: variable, "is not defined as watchpoint"
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
    elif command.startswith('b'):  # breakpoint
        if not arg:
            print "You must supply a line number"
        else:
            breakpoints[int(arg)] = True
    elif command.startswith('w'):  # watch variable
        if not arg:
            print "You must supply a variable name"
        else:
            watchpoints[arg] = True
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

    if event == 'line':
        if stepping or breakpoints.has_key(frame.f_lineno):
            resume = False
            print event, frame.f_lineno, frame.f_code.co_name, frame.f_locals
            while not resume:
                command = input_command()
                resume = debug(command, frame.f_locals)
    return traceit


# globals
breakpoints = {24: True}
watchpoints = {'out': True}
stepping = False

commands = ["p", "c", "c", "c", "q"]

# Using the tracer
sys.settrace(traceit)
main()
sys.settrace(None)
