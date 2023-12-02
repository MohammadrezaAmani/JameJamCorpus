import asyncio
import logging
from package_name.scrap import main
from package_name.utils.save import to_file
from package_name.db.crud import remove_duplicates

if __name__ == "__main__":
    logging.info("GET DATA...")
    asyncio.run(main())

    logging.info("SOLVE DUPLICATES...")
    remove_duplicates()

    logging.info("SAVE TO FILE...")
    asyncio.run(to_file("data.csv"))
