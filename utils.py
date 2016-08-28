import re
from time import time
from contextlib import contextmanager
import inspect

@contextmanager
def timer(log):
    start = time()
    fname = inspect.currentframe().f_back.f_back.f_code.co_name
    yield
    dur = time()-start
    #log('{fname} executed in {time}'.format(fname=fname, time=dur))


def divide(list_, size):
    r = [list_[i:i+size] for i in xrange(0, len(list_), size)]
    return r


def naive_parentheses(input):
    '''
    returns True if paratheses match using a type-3 parser
    input: string
    '''

    stack = []
    check = lambda: stack == [] or stack is None

    for letter in input:
        if letter == '(':
            stack.append('(')
        elif letter == ')':
            try:
                if stack[-1] == '(':
                    stack.pop()
            except IndexError:
                return False

    return check()


def naive_tokenenizer(input):
    '''
    returns an array of [user_name, action]
    input: string
    '''
    no_ops = re.sub(r'\(|\)|\^|&|\||\-|[ ]+|\n', '', input)
    normalized = re.sub(' +', ' ', no_ops)
    return [user.split('.') for user in
            filter(None, normalized.split('@'))]


def naive_syntax(input):
    '''
    returns True if the input is a valid pair of screen_name and action
    input: [string, string] => [screen_name, action]
    '''
    if len(input) == 0:
        return False

    ops = ['followers', 'friends', 'mutual', 'all', 'ego']

    for calculate in input:
        if len(calculate) != 2 or calculate[1] not in ops:
            return False

    return True
