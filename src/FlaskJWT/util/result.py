class Result:
    def __init__(self, success, value, error):
        self.success = success
        self.error = error
        self.value = value

    @staticmethod
    def success(value=None):
        return Result(True, value=value, error=None)

    @staticmethod
    def fail(errorMessage):
        return Result(False, value=None, error=errorMessage)
 
