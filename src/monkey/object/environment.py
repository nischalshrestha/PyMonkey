class Environment:
    outer = None # pointer to enclosing Environment
    store = {} # str

    def __init__(self, store, outer):
        self.store = store
        self.outer = outer
    
    def get(self, name):
        obj = None
        if name in self.store:
            obj = self.store[name]
        elif self.outer != None:
            obj = self.outer.get(name)
        return obj
    
    def set_name(self, name, value):
        self.store[name] = value
        return value

def new_environment():
    return Environment({}, None)
