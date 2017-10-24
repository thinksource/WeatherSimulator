class NetError(Exception):
    """Exception raised for errors for network

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message,errorcode):
        super(NetError, self).__init__(message)
        self.errorcode=errorcode

class DataFormatError(Exception):
    """Exception for DataFormat"""

    def __init__(self, message):
        super(DataFormatError, self).__init__(message)
