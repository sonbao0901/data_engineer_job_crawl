from sqlalchemy import create_engine, text

conn = create_engine(db_conn).connect()

r = conn.execute(text("""
        SELECT schema_name 
        FROM information_schema.schemata 
        WHERE schema_name NOT LIKE 'pg_%' 
        AND schema_name != 'information_schema'
    """))

for row in r:
    print(row)
