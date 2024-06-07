import itertools

def message_simplify(text):
    return ''.join(
        ch for ch, _ in itertools.groupby(text)
    )
