import os

LOG_LOCATION = (
    "/var/log/pdf2ebook/pdf2ebook.log"
    if os.getenv("TEST_ENV", "False") == "False"
    else "/tmp/log/pdf2ebook/pdf2ebook.log"
)
