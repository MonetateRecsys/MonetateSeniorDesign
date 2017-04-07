from lettuce import *
from cf_test import data_loader

@step('I connect to the database')
def have_the_filename(step):
    world.conn = data_loader.get_connection()

@step('The connection is valid')
def connect_to_it(step):
    assert world.conn != None



@step('I run load data')
def run_load_data(step):
    data_loader.init_database(world.conn)
    data_loader.load_fake_data(world.conn)

@step('The database wont be empty')
def database_wont_be_empty(step):
    c = world.conn.cursor()
    c.execute('''SELECT * FROM products''')
    assert len(c.fetchall()) > 0