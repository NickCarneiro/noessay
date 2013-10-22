from models import Scholarship

__author__ = 'gaurav'

from pyquery import PyQuery as pq
import requests

def parseIndividualPage(id):
    page = requests.get("http://www.aie.org/Scholarships/detail.cfm?id={}".format(id))
    document = pq(page.text)
    article = document('article')
    title = article('h1')
    elements = article.children()
    scholarship_data = dict()

    header = ""
    data = ""
    for element in elements:
        pq_element = pq(element)
        raw_html_of_element = str(pq_element)
        if raw_html_of_element.startswith("<h4>"):
            if len(header) > 0 and len(data) > 0:
                scholarship_data[header] = data
            header = pq_element.text()
            data = ""
        else:
            data_to_append = pq_element.text()
            if data_to_append:
                data_to_append = data_to_append.replace('\r\n\\', '\n')
                data += data_to_append + "\n"

    for key in scholarship_data:
        print(key + ": " + scholarship_data[key])

    scholarship = Scholarship(title=title, street_address=scholarship_data["Sponsor information"],
                              sponsored=False,
                              )


parseIndividualPage(15000)