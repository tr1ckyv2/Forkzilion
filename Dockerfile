# inherit prebuilt image
FROM ubuntu:20.04

# env setup
RUN mkdir /Fizilion && chmod 777 /Fizilion
ENV PATH="/Fizilion/bin:$PATH"
WORKDIR /Fizilion

RUN echo deb http://us.archive.ubuntu.com/ubuntu/ focal universe > /etc/apt/sources.list.d/docker.list
RUN apt-get update && DEBIAN_FRONTEND="noninteractive" TZ="Asia/Ho_Chi_Minh" apt-get install -y tzdata
RUN apt-get install -y --no-install-recommends \
    curl \
    git \
    gcc \
    g++ \
    build-essential \
    gnupg2 \
    unzip \
    wget \
    ffmpeg \
    jq \
    libpq-dev \
    neofetch \
    python3-pip \
    python3-psycopg2

# clone repo
RUN git clone https://github.com/DunggVN/Forkzilion -b DunggVNTest /Fizilion

# Copies session and config(if it exists)
COPY ./sample_config.env ./userbot.session* ./config.env* /Fizilion/

# install required pypi modules
RUN pip install pip
RUN pip install -r requirements.txt

# Finalization
CMD ["python3","-m","userbot"]
