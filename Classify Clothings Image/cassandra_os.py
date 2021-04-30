from cassandra.cluster import Cluster
from cassandra.policies import RoundRobinPolicy


def create_key_space(keyspacename, ster):
    session = ster.connect()
    return session


def connect_key_space():
    ster = Cluster(contact_points=['127.0.0.1'],
                   port=9042,
                   load_balancing_policy=RoundRobinPolicy())
    keyspacename = "test"
    session = ster.connect(keyspace=keyspacename)
    return session


def print_key_spaces(ster):
    print(ster.metadata.keyspaces)



def print_tables(ster,keyspacename):
    print(ster.metadata.keyspaces[keyspacename].tables)



def exist_table(table_name, keyspacename):
    ster = Cluster(contact_points=['127.0.0.1'],
                   port=9042,
                   load_balancing_policy=RoundRobinPolicy())
    session = ster.connect()
    print(ster.metadata.keyspaces[keyspacename].tables.keys())
    session.shutdown()
    if table_name in ster.metadata.keyspaces[keyspacename].tables.keys():
        return True
    return False


def exist_keyspace(keyspace):
    ster = Cluster(contact_points=['127.0.0.1'],
                   port=9042,
                   load_balancing_policy=RoundRobinPolicy())
    session = ster.connect()
    print(ster.metadata.keyspaces.keys())
    session.shutdown()
    if keyspace in ster.metadata.keyspaces.keys():
        return True
    return False


def keyandspace():
    ster = Cluster(contact_points=['127.0.0.1'],
                   port=9042,
                   load_balancing_policy=RoundRobinPolicy())
    session = ster.connect()
    if not exist_keyspace("test"):
        session.execute("CREATE KEYSPACE test WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};")

    if not exist_table("picrecog", "test"):
        session.execute('create table test.picrecog(inserttime varchar,predictres int,filepath varchar primary key);')
    session.shutdown()


def insert_data(filepath, crtime, predictres):
    keyandspace()
    session = connect_key_space()
    sql = 'insert into picrecog(filepath,inserttime,predictres) values(%s, %s, %s)'
    session.execute(sql, (filepath, crtime, predictres))
    session.shutdown()


def showdata():
    keyandspace()
    session = connect_key_space()
    sql = 'select * from picrecog'
    rs = session.execute(sql)
    session.shutdown()
    return rs

rr = showdata()
print(rr.current_rows)
