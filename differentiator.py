def tokenize(expression):
    '''
    Break expression down into array.
    '''
    return expression.replace('+', ' + ').replace('-', ' - ').replace('*', ' * ').replace('^', ' ^ ').split()

def differentiate_tokens(expression):
    '''
    Very basic symbolic differentiator.
    '''
    if len(expression) % 6 != 5:
        raise SyntaxError('Invalid expression')

    try:
        for i in range(0, len(expression), 6):
            expression[i] = str(int(expression[i]) * int(expression[i+4]))
            expression[i+4] = str(int(expression[i+4]) - 1)

    except:
        raise SyntaxError('Invalid expression')

    return ' '.join(expression)

def differentiate(expression):
    return differentiate_tokens(tokenize(expression))

print(differentiate('5*x^2 + 4*x^1'))
