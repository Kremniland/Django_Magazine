from functools import wraps

def dec_summa(func):
    @wraps(func)
    def inner(*args,**kwargs):
        print(func(*args,**kwargs))
    return inner

@dec_summa
def summa(x, y):
    ''' Сумма двух чисел '''
    return x+y

print(summa.__doc__)
