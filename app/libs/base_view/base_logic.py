class BaseLogic(object):
    def __init__(self, depends):
        self.request = depends.request
        self.managers = depends.request.app.state.managers
        # TODO 利用 denpendencies 机制，将 连接池/response/background_tasks 附到 self
