class ConversionNode(object):
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)
