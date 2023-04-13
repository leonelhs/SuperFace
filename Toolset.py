class Toolset:
    def __init__(self, args):
        self.args = args
        self.__instances = {}
        self.progressBar = None
        self.showMessage = None
        self.twinViewer = None

    def newInstance(self, name, instance):  # deliberate use of a mutable default arg
        if name not in self.__instances:
            self.__instances[name] = instance(self.args)
        return self.__instances[name]

    def setControls(self, controls):
        self.progressBar = controls[0]
        self.showMessage = controls[1]
        self.twinViewer = controls[2]

    def preInit(self, message):
        self.showMessage("", message)
        self.progressBar.show()
