# SYSTEM_MANAGER.create_keyspace('stack_overflow',  strategy_options={"replication_factor": "1"})
# SYSTEM_MANAGER.create_column_family('stack_overflow', 'users')
# SYSTEM_MANAGER.create_column_family('stack_overflow', 'posts')

import gzip
from xml.dom.minidom import parse, parseString
import pycassa

f = gzip.open('Users.xml.gz')
f.readline()
f.readline()

pool = pycassa.pool.ConnectionPool('stack_overflow')
cf_users = pycassa.columnfamily.ColumnFamily(pool, 'users')


l = f.readline()
row_num = 0
users_batch = {}
while l != None:
    row_num += 1

    row = f.readline()        #wczytaj kolejny wiersz
    dom = parseString(row)    #parsuj xml
    row_node = dom.firstChild #pierwszy potomek to atrybut row

    row_key =  unicode(row_node.attributes['Id'].value)

    user = { } #pusty slownik

    for attr_key in row_node.attributes.keys():
        user[attr_key] = row_node.attributes[attr_key].value.encode('ascii', 'ignore') #konwerxja utf-8 --> ascii

    #dodawaj w batchach po 200 uzytkownikow
    users_batch[row_key] = user

    if len(users_batch) % 200 == 0:
        cf_users.batch_insert(users_batch)
        users_batch = {}
        print row_num
    # cf_users.insert(row_key, user)

    l = f.readline()
