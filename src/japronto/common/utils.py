def unique_func_name(func):
    return "%s.%s" % (func.__module__, func.__name__)
