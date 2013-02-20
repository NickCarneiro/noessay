# encapsulates a Scholarship model, includes metadata such as scholarship_key not found in the model
class SerpResult:
    def __init__(self, scholarship_key=None, scholarship_model=None):
        self.scholarship_key = scholarship_key
        self.scholarship_model = scholarship_model