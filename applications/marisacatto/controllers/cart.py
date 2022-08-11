
def index():
    return 0
def show():

    if not session.cart:
        session.cart = None
        session.balance = 0

    return 0