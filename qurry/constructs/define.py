from ..datatypes import update_definitions
from ..datatypes import Datatype

from pprint import pprint

def process_type(body, kernel):
    if len(body) == 1:
        body = body[0]
    head, *rest = body
    if head in kernel.definitions and isinstance(kernel.definitions[head], Datatype):
        print(kernel.definitions[head])
        return kernel.definitions[head].instance(head, *rest)
    else:
        raise ValueError('Cannot process type {}'.format(head))

def define(*expression, kernel=None):
    name, *rest = expression
    if name not in kernel.definitions:
        kernel.definitions[name] = process_type(rest, kernel)
        print('Kernel definitions:')
        print(kernel.definitions)
    else:
        raise ValueError('{} is already defined'.format(name))
    return ''
