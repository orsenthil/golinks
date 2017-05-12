FROM muhammadhanif/crud-flask-mysql
MAINTAINER senthil kumaran <senthil@uthcode.com>
RUN apt-get update
RUN apt-get install -qyy \
    -o APT::Install-Recommends=false -o APT::Install-Suggests=false \
    build-essential \
    libncursesw5-dev \
    libreadline-dev \
    libssl-dev \
    libgdbm-dev \
    libc6-dev \
    libsqlite3-dev \
    tk-dev \
    libbz2-dev \
    liblzma-dev \
    python3 \
    python3-dev \
    libmysqlclient-dev \
    libffi6 \
    openssl \
    ssh \
    git \
    vim \
    emacs \
    apt-transport-https \
    ca-certificates \
    docker.io

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["golinks.py", "runserver"]
