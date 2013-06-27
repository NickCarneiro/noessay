# check every non-expired scholarhsip to see if it still exists
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "noessay.settings")

from search.models import *

