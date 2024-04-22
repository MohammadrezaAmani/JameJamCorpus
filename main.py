import asyncio
import logging
import time

from jamejam.db.crud import remove_duplicates
from jamejam.scrap import main
from jamejam.utils.save import to_file

start = time.time()
if __name__ == "__main__":
    logging.info("GET DATA...")
    asyncio.run(main())

    logging.info("SOLVE DUPLICATES...")
    remove_duplicates()

    logging.info("SAVE TO FILE...")
    asyncio.run(to_file("data.csv"))
print(time.time() - start)
