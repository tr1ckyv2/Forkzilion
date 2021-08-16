# inherit prebuilt image
FROM python:3.9-slim-buster

# env setup
RUN mkdir /Fizilion && chmod 777 /Fizilion
ENV PATH="/Fizilion/bin:$PATH"
WORKDIR /Fizilion

RUN echo deb http://http.us.debian.org/debian/ testing non-free contrib main > /etc/apt/sources.list && \
    apt -qq update
RUN apt -qq install -y --no-install-recommends \
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
    libpq-dev

# clone repo
RUN git clone https://github.com/DunggVN/ProjectFizilion -b DunggVNTest /Fizilion

# Copies session and config(if it exists)
COPY ./sample_config.env ./userbot.session* ./config.env* /Fizilion/

# install required pypi modules
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Finalization
CMD ["python3","-m","userbot"]
