from pyquil.gates import STANDARD_INSTRUCTIONS

from pprint import pprint

from .templates import if_template, clear_template
from .utils     import named_uuid

def create_if(cond, a, b):
    return if_template.format(
            cond=cond,
            a=generate_single(a),
            b=generate_single(b),
            first=named_uuid('first'),
            end=named_uuid('end'))

def create_clear(q, scratch=63):
    return clear_template.format(q=q, scratch_bit=scratch, uuid=named_uuid('qubit-{}'.format(q)))

def build(stack):
    definitions = dict()
    def insert_defs(items):
        for item in items:
            try:
                yield definitions[item]
            except KeyError:
                yield item
            except TypeError:
                yield item
    for expression in stack:
        assert len(expression) > 0, 'Error: parsed empty list {}'.format(item)
        head = expression[0]
        upper = head.upper()
        if upper in STANDARD_INSTRUCTIONS:
            expression[0] = upper
            if upper == 'MEASURE':
                yield '{} {} [{}]'.format(*insert_defs(expression))
            else:
                yield ' '.join(insert_defs(expression))
        elif head == 'if':
            yield create_if(*(insert_defs(expression[1:])))
        elif head == 'def':
            assert len(expression) == 3, 'Def expressions should take the form (def var val)'
            definitions[expression[1]] = expression[2]
        elif head == 'clear':
            assert len(expression) == 2, 'Clean expressions should look like: (clear q)'
            yield create_clear(expression[1])
        elif head == 'flip':
            assert len(expression) == 1 or len(expression) == 2, 'Flip requires either zero or one argument'
            if len(expression) == 1:
                yield ''
            else:
                yield ''
            print(expression)
            yield '# FLIP {}'
        else:
            print('No generation branch for:')
            print(head)
            1/0

def generate_single(expression):
    return generate([expression])

def generate(stack):
    pprint(stack)
    return '\n'.join(build(stack))
