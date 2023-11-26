

class SIPBagitTransformerService:
    """
    This class is responsible for transforming a project's SIP to the required bagit format.	
    """

    def __init__(self):
        pass

    def validate(self, input_data):
        raise NotImplementedError()

    def save(self, output_data):
        raise NotImplementedError()

    def transform(self, input_data):
        raise NotImplementedError()
