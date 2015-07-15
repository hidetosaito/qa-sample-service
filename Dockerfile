# To run this: sudo docker build .

FROM python:2.7.7

ADD . /code
WORKADR /code
RUN pip install -r requirements.txt
CMD python entry.py