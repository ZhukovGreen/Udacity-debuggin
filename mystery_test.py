import random
import re


def test(s):
    # print s, len(s)
    if re.search("<SELECT[^>]*>", s) >= 0:
        return "FAIL"
    else:
        return "PASS"
# def test(s):
#     if s.find("ab11cd") > -1 or s.find("abcd") > -1 or s.find('gab11') > -1:
#         return "FAIL"
#     else:
#         return "PASS"


def ddmin(s, test_foo):
    resume_1 = True
    counter_1 = 0
    result = []
    ini_s = s
    while resume_1:
        s = ini_s
        resume_2 = True
        counter_2 = 0
        potential_result = ''
        slicer_min = None
        slicer_max = None
        while resume_2:
            slicer = random.choice(range(1, len(s)))
            if test_foo(s[: slicer]) == 'FAIL' and test_foo(s[slicer:]) == 'PASS':
                s = s[: slicer]
                slicer_min = None
                slicer_max = None
            elif test_foo(s[slicer:]) == 'FAIL' and test_foo(s[: slicer]) == 'PASS':
                s = s[slicer:]
                slicer_min = None
                slicer_max = None
            else:
                if slicer_min > slicer or slicer_min == None:
                    slicer_min = slicer
                if slicer_max < slicer or slicer_max == None:
                    slicer_max = slicer
                if not s[slicer_min - 1:slicer_max + 1] == potential_result:
                    potential_result = s[slicer_min - 1:slicer_max + 1]
                    counter_2 = 0
                else:
                    counter_2 += 1
                if counter_2 > 1000:
                    resume_2 = False
        if s not in result:
            result.append(s)
            counter_1 = 0
        else:
            counter_1 += 1
        if counter_1 > 1000:
            break

    return result


# html_input = 'asdfdslfmngladfgab11cddfsfdsfabcddfadfsdkjfdlksgjdfslgjdfnneureuhdsadl'
html_input = '<SELECT>foo</SELECT>'

print ddmin(html_input, test)

# while True:
#     try:
#         result = ddmin(html_input, test)
#         assert result=="<SELECT>"
#     except AssertionError:
#         print result
#         break
