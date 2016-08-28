from parsley import makeGrammar as make_grammar


class Parser:
    GRAMMAR = '''
        expr   = ws expr2:left ws lowp*:right ws -> calculate(left, right)
        expr2  = value:left highp*:right -> calculate(left, right)
        value  = user | parens
        parens = '(' ws expr:e ws ')' -> e

        highp = ws (and | or)
        lowp  = ws (xor | sub)

        and = '&' ws value:n -> ('&', n)
        or  = '|' ws value:n -> ('|', n)
        xor = '^' ws expr2:n -> ('^', n)
        sub = '-' ws expr2:n -> ('-', n)

        user = '@' <alpha+>:user '.' <operations>:op  -> fetch(user, op)
        alpha = (letterOrDigit | '_')+
        operations = ('friend' ('z' | 's')| 'followers' | 'all' | 'ego')
    '''

    def __init__(self, fetch, calculate):
        self.fetch = fetch
        self.calculate = calculate

    def execute(self, query):
        functions = {
            'fetch': self.fetch,
            'calculate': self.calculate
        }
        grammar = make_grammar(self.GRAMMAR, functions)
        return grammar(query).expr()
