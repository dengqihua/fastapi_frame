class BaseLogic(object):
    def __init__(self, depends):
        self.request = depends.request
        self.managers = depends.request.app.state.managers

