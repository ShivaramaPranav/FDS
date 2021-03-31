#
# Use this to create a DB
#
from web.models import *
from web import db

db.create_all()