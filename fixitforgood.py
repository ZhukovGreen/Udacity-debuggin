#
# Modify `remove_html_markup` so that it actually works!
#

def remove_html_markup(s):
    tag = False
    quote = False
    out = ""
    open_quote = ""
    for c in s:
        # print c, tag, quote
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif (c == '"' or c == "'") and tag:
            if not quote:
                quote = True
                open_quote = c
            elif quote and c == open_quote:
                quote = False
        elif not tag:
            out = out + c

    return out


def test():
    assert remove_html_markup('<a href="don' + "'" + 't!">Link</a>') == "Link"


test()
