import itertools

def message_simplify(text):
    return ''.join(
        ch for ch, _ in itertools.groupby(text)
    )

def place_trade():
    pass

def move_sl():
    pass

def close_trade():
    pass

