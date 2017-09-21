# !/usr/bin/env python
# -*- coding: UTF-8 -*-


# returns the current datetime
def _get_date():
    import datetime
    return datetime.datetime.now()


# trivial solution for unique ids to be used
# in database
def unique_id_generator():
    import uuid
    return str(uuid.uuid4())

# print _get_date()

