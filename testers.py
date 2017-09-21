#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test module to test the catalog application
    when run drops all tables and populates user table
    with user test1 category table with "Bedroom" as a
    item in the table with id 1 and similiarly creates
    three items in bedroom category viz Bed,Table and chairs
    with ids 1,2,3 respectively.The module would serve for code
    reviewers or anyone interested to see the local file permissions
    systems working on the site """

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, Catalog_Item, User
import time

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
test_database = ""


# object which holds all data that is to be populated
# in the database
db_object = {"User":
             [{"test1":
              [{"id": 1}, {"name": "test1"}, {"email": "test1@test.com"}]
               }
              ], "category_items": [
                                    {"Bed": [{"id": 1},
                                     {"image":
                                      "http://content.blueport.com/ProductImages/0/332756.jpg"}]},
                                    {"Tables": [{"id": 2},
                                     {"image":
                                      "http://www.ikea.com/PIAimages/0470421_PE612777_S5.JPG"}]},
                                    {"Chairs": [{"id": 3},
                                     {"image":
                                      "http://www.ikea.com/PIAimages/0105948_PE253720_S5.JPG"}]}
                                    ], "category": [{"Bedroom": [{"id": 1},
                                                    {"image": "http://www.ikea.com/ms/media/cho_room/20171/sleeping/20171_cosl06a/20171_cosl06a_01_PH137675.jpg"}]}
                                                    ]
             }


def initialise_test_run():
    """function to initialise database
       this function wont work  if you logged in first using your credentials
       and are registered since your username will have id=1 which will
       conflict and raise sql error
       so only run this module at the start or it wont work"""
    insert_category()
    insert_category_items()
    # print test_database
    return


# inserts the user test1 in users table
def populate_user_database():
    count = 0
    for items in enumerate(db_object["User"]):
        user = db_object["User"][count].keys()[0]
        id = db_object["User"][count][user][0]["id"]
        email = db_object["User"][count][user][2]["email"]
        count = count + 1
        # print user, id, email
        query = User(id=id, name=user, email=email)
        session.add(query)
        session.commit()
        print "User table populated"
    return query


# inserts the category "Bedroom" and assigns creator as "test1"
def insert_category():
    category = db_object["category"]
    test_user = populate_user_database()
    for items in category:
        name = category[0].keys()[0]
        id = category[0][name][0]["id"]
        image = category[0][name][1]["image"]
    query = Catalog(id=id, name=name, user=test_user, image=image)
    session.add(query)
    session.commit()
    print "Category created"
    return query


# inserts the category items bed,chair,table under user
# test 1 and parent Bedroom
def insert_category_items():
    category_items = db_object["category_items"]
    category = session.query(Catalog).first()
    test_user = session.query(User).first()
    count = 0
    for items in category_items:
        name = category_items[count].keys()[0]
        id = category_items[count][name][0]["id"]
        image = category_items[count][name][1]["image"]
        query = Catalog_Item(id=id, name=name,
                             user=test_user, image=image, catalog=category)
        session.add(query)
        session.commit()
        count = count + 1
    print "Category Items Populated"
    return


# deletes all the tables
def drop_all_tables():
    Catalog_Item.__table__.drop(engine)
    Catalog.__table__.drop(engine)
    User.__table__.drop(engine)
    print "Everything dropped"
    Base.metadata.create_all(engine)

# uncomment it to delete all tables
# please do not use this while you are still logged in
# comment out if__name__=__main__ block
# before using this
# drop_all_tables()


# a quick check to see the items in table
# just pass table name as a argument to the function
# and uncomment the function call below.
def print_table(table):
    print "printing"
    query = session.query(table).all()
    print query
    for items in query:
        print items.id, items.name

# calling function print table
# uncomment it and pass table name as argument
# print_table(Catalog_Item)


# deletes test user and all the entries that it created
def delete_test_user():
    query_user_id = session.query(User).filter(User.name == "test1").first()
    # print query_user_id.id
    query_category = session.query(Catalog).filter(
        Catalog.creator == query_user_id.id).all()
    # print query_category[0].name
    # print test_database
    query_category_items = session.query(Catalog_Item).all()
    # print query_category_items[0].name
    session.delete(query_user_id)
    # delete all the items under catalog that is deleted.
    # for eg..first delete bed under bedroom if bedroom is
    # going to be deleted,which is the case if it was created by
    # user test1.Since anyone can add items to category.This will
    # also include items you created under category created by user test1.
    for entries in query_category_items:
        print entries.name
        for c_entries in query_category:
            print "checking" + entries.name + "in" + c_entries.name
            if (entries.catalog_relation == c_entries.id):
                print "entry found" + entries.name + "in" + c_entries.name
                session.delete(entries)
                print "deleting"
    for entries in query_category:
        session.delete(entries)
    session.commit()
    return

# when this module is run as main,it populates the database if
# it is empty or it deletes everything created by the user test1.
# we assume here none of our users will be  named test1 in future.
# TODO: we can generate a random number and text and substitute it with
# user name test1 in db_object creating minimal chances of conflict.
if __name__ == '__main__':
    try:
        query = session.query(User).filter(
            User.name == 'test1').first()
        # print query
        if query is not None:
            test_database = True
        else:
            test_database = False
        print test_database
    except:
        print "Fatal error"
    if test_database is False:
        print "populating test entities in database"
        initialise_test_run()
    else:
        delete_test_user()
        print "deleting test entities from database"
