class ScriptTimingValues:
    def __init__(self, LC, MS, Gradient, SPE):
        """
        This just holds the timing values of a script in an object.
        This makes it easier to access the values witout having to go back into the json file.
        Objects of this type are store in a list in high_level_script_reader.py so you can access
        past timing values

        Args:
            LC ([int]): [num seconds. Time before the end of the loop to turn on the LC]
            MS ([int]): [num seconds. Time after the start of the loop to turn on the MS]
            Gradient ([int]): [num seconds. Time of the gradient]
            SPE ([int]): [num seconds. Time of the SPE]
        """
        self.LC_time = LC
        self.MS_time = MS
        self.Gradient_time = Gradient
        self.SPE_time = SPE