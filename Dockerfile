FROM python:3

ADD src /src/
ADD requirements.txt /
ADD tag_252490.csv /

RUN pip install -r ./requirements.txt

CMD [ "python", "/src/crawl.py" ]