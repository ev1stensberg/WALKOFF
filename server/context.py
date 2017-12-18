class Context(object):
    def __init__(self):
        """Initializes a new Context object. This acts as an interface for objects to access other event specific
            variables that might be needed.
        """
        import core.controller

        self.controller = core.controller.controller


running_context = Context()
