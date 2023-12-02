"""Configurations for the package"""

# ? Base url of the website
BASE_URL = "https://jamejamonline.ir/fa/news/"

# ? Start and end of dynamic id range
START = 1
# END = 1433528
END = 10

# ? Set the maximum number of concurrent calls per second
MAX_CALLS_PER_SECOND = 1024

# ? Database (postgresql offers better performance)
#! postgresql
# DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/db_name"

#! sqlite
DATABASE_URL = "sqlite+aiosqlite:///data.db"

# ? Logging
DEBUG = True
DATABASE_LOGGING = False
