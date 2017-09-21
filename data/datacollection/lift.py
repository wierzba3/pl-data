class Lift(object):
    """Represents a lift type"""

    def __init__(self):
        self.weight_class = None
        self.lift_type = None
        self.weight_lifted = None
        self.name = None
        self.date = None
        self.source = None

    def __str__(self):
        return "Weight class = {}, Lift type = {}, Weight lifted = {}kg, Name = {}, Date = {}". \
            format(self.weight_class, self.lift_type, self.weight_lifted, self.name, self.date)


