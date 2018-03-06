FROM python:3

ADD src /


CMD [ "python", "./src/crawl.py" ]