FROM python:3

ADD src /
ADD requirements.txt /

RUN pip install -r ./requirements.txt

CMD [ "python", "./src/crawl.py" ]