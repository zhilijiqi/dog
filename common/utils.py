__doc__="""π§æﬂ¿‡"""
def check_attr(obj=None,attr_name=None):
    if obj is None or attr_name is None:
        return None
    elif hasattr(obj, attr_name):
        return getattr(object, attr_name)
    
def call_attr_func(obj=None,attr_name=None,*args):
    func = check_attr(obj, attr_name);
    if func:
        return func(*args)

    