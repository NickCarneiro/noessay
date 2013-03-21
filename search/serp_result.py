# encapsulates a Scholarship model, includes metadata such as scholarship_key not found in the model
class SerpResult:
    def __init__(self, scholarship_key=None, scholarship_model=None):
        self.scholarship_key = scholarship_key
        self.scholarship_model = scholarship_model
        self.snippet = scholarship_model.description[:250]
        if scholarship_model is not None:
            self.deadline = scholarship_model.deadline
        self.source = scholarship_model.organization
        self.href = scholarship_model.third_party_url
        self.title = scholarship_model.title