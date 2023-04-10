class TestTask:
    def __init__(self, task, args):
        self.testTask = task(args)

    def runTest(self, image):
        self.testTask.startEnhanceThread(image)

