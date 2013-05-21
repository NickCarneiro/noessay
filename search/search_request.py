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

    def get_base_url(self, start):
        url = '/search?q=' + self.keyword
        if self.location is not None:
            url += '&l=' + self.location
        if self.no_essay_required is not None:
            url += '&ne=true'
        if self.deadline is not None:
            url += '&d=' + self.deadline
        if self.ethnicity_restriction is not None:
            url += '&e=' + str(self.ethnicity_restriction)
        if self.gender_restriction is not None:
            url += '&g=' + str(self.gender_restriction)
        if start is not None and start > 0:
            url += '&start=' + str(start)
        return url