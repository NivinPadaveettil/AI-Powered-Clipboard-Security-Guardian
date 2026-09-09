
from src.database.sqlite_logger import logger


print("=" * 60)
print("Clipboard Detection History")
print("=" * 60)

history = logger.fetch_all()

if not history:
    print("No clipboard detection history found.")
else:
    for row in history:
        print(row)

