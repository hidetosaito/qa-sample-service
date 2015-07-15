# To run this: sudo docker build .

FROM python:2.7.7

# Bundle app source
ADD . /code

# install dependency
WORKDIR /code
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Run
CMD ["python", "entry.py"]



