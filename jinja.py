# jinja functions


# check if any item in 'a' is found in 'b'
def foundin(a, b):
    return bool(len(set(a).intersection(b)))


def notfoundin(a, b):
    return len(set(a).symmetric_difference(b)) == len(set(a+b))
