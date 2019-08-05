import logging



#def use_logging(fun):
#    def wrapper(*arg, **kwargs):
#        logging.warn("%s is running" % fun.__name__)
#        return fun(*arg, **kwargs)
#    return wrapper

def use_logging(func):
    print("%s was decorated." % func.__name__)    
    def wrapper(*arg, **kwargs):
        logging.warn("%s is running" % func.__name__)
        return func(*arg, **kwargs)
    return wrapper

@use_logging
def bar():
    print("i am bar")

print("before call decorated function.")
bar()
