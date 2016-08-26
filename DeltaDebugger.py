#
# Finish the delta debug function ddmin
#


import re

test_count = 0


def test(s):
    global test_count
    test_count += 1
    print test_count, repr(s), len(s)
    s_merged = "".join(s)
    if re.search("<SELECT[^>]*>", s_merged) >= 0:
        print "FAIL"
        return "FAIL"
    else:
        print "PASS"
        return "PASS"


def ddmin(s, foo):
    # assert test(s) == "FAIL"

    n = 2  # Initial granularity
    while len(s) >= 2:
        start = 0
        subset_length = len(s) / n
        some_complement_is_failing = False

        while start < len(s):
            complement = s[:start] + s[start + subset_length:]
            if foo(complement) == "FAIL":
                s = complement
                n = max(n - 1, 2)
                some_complement_is_failing = True
                break

            start += subset_length

        if not some_complement_is_failing:
            if n == len(s):
                break
            n = min(n * 2, len(s))
    return s


# UNCOMMENT TO TEST
print ddmin('<SELECT>foo</SELECT>', test)
print ddmin(['<SELECT>', 'foo', '</SELECT>'], test)
