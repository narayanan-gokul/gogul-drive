from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session


engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# Does not commit the transaction by default.
with engine.connect() as conn:
    result = conn.execute(text("SELECT 'Hello world'"))
    print(result.all())

# Committing transactions:
# The SQL statement is executed repeatedly for each of the items in the second
# parameter.
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 2}, {"x": 2, "y": 4}],
    )
    conn.commit()

# The with block acts as a transaction block:
# Commits the commands within the context block automatically
# Rolls back the transaction in case of an exception within the block
# Parameters are named and a dictionary is expected with the correct values
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 5, "y": 6}, {"x": 7, "y": 8}],
    )

# Using results:
# The result object that is returned is a iterable collection of row objects
# Each row object is equivalent to a named tuple.
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x} y: {row.y}")

# ORM uses Session objects to carry out transactions:
with Session(engine) as session:
    result = session.execute(text("Select x, y FROM some_table WHERE x > :x"), {"x": 2})
    for row in result:
        print(f"x: {row.x} y: {row.y}")

# Manual commits are required:
with Session(engine) as session:
    session.execute(text("UPDATE some_table SET y = :y WHERE x = :x"), {"x": 2, "y": 3})
    session.commit()
    result = session.execute(text("SELECT x, y FROM some_table WHERE x = :x"), {"x": 2})
    for x, y in result:
        print(f"x: {x} y: {y}")
