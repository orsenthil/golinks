FROM python:3.6
MAINTAINER Senthil Kumaran <senthil@uthcode.com>
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["golinks.py", "runserver]
