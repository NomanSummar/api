DATABASE_SERVICE = "sqlite3"

if DATABASE_SERVICE == "mysql":
    SYM = "%s"
elif DATABASE_SERVICE == "postgresql":
    SYM = "%s"
elif DATABASE_SERVICE == "sqlite3":
    SYM = "?"

MS = '%s'
