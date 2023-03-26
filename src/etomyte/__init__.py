import os
class App(object):
    def __init__(self, appfolder):
        self.appfolder=appfolder
    def run(self):
        parsedoc()

    def parsedoc(self, doc:str="index"):
        print(os.path.join([self.appfolder, "cnt"]))
    