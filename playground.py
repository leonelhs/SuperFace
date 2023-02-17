def anonymous(callback, param):
    print(param)
    callback(param)


anonymous((lambda a: print(a)), "parameter")
