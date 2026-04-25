
from postgres_DB import PostgresDB
from subanta import parse_subanta
from tinanta import parse_tinanta


def load_sub_tin():
    db = PostgresDB()

    if db.initialize_database("sub_tin_db.sql"):
        parse_subanta(db.get_connection())
        parse_tinanta(db.get_connection())

def main():
    load_sub_tin()

if __name__ == '__main__':
    main()