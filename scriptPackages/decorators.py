import functools


def catch(f):
    '''
    Catches every not-managed exception in a function.
    '''
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(e)
            return None
    return wrapper
