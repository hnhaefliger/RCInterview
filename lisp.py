def tokenize(expression):
    '''
    Break expression down into individual terms.
    '''
    expression = expression.replace('(', ' ( ').replace(')', ' ) ').split()
    return expression

def read(tokens):
    '''
    Create AST from expression.
    '''
    token = tokens.pop(0)

    if token == '(': # Start a sub-tree.
        ast = []

        try: # Will cause an index error if there are too many '(' in expression due to searching for ')' in empty list.
            while tokens[0] != ')':
                ast.append(read(tokens))

        except:
            raise SyntaxError('Unmatched "(".')

        del tokens[0]
        return ast

    elif token == ')':
        raise SyntaxError('Unexpected ")".')

    return token

def parse_lisp(expression):
    '''
    Return the AST for a lisp expression.
    '''
    return read(tokenize(expression))

print(read(tokenize('(first (list 1 (+ 2 3) 9))')))
