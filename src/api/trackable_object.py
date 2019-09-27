class TrackableObject():

    def __init__(self,name):
        self._name=name
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        self._name = new_name

    def track(self):
        """
        Method used to track objects
        Retruns:
            latitude, longitude - tuple of ints
        """
        pass
