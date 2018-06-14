class BaseClient(object):
    """
    Base superclass for a sensor client.
    """

    def start(self, *args, **kwargs):
        """
        Perform any stateful initialization procedures.
        """
        pass

    def read(self, *args, **kwargs):
        """
        Read a message from the sensor.
        """
        pass

