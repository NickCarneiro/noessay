class SearchRequest:
    def __init__(self, keyword="", location="", no_essay_required=False,
                 deadline=None,
                 ethnicity_restriction=None,
                 gender_restriction=None):
        self.location = location
        self.keyword = keyword
        self.no_essay_required = no_essay_required
        self.deadline = deadline
        self.ethnicity_restriction = ethnicity_restriction
        self.gender_restriction = gender_restriction