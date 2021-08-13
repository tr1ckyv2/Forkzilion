# inherit prebuilt image
FROM prajwals3/projectfizilion:latest

# env setup
RUN mkdir /Fizilion && chmod 777 /Fizilion
ENV PATH="/Fizilion/bin:$PATH"
WORKDIR /Fizilion
RUN apk add megatools

# clone repo
RUN git clone https://github.com/DunggVN/ProjectFizilion -b DunggVN-Branch /Fizilion

# Copies session and config(if it exists)
COPY ./sample_config.env ./userbot.session* ./config.env* /Fizilion/

# create virtualenv
RUN pip3 install virtualenv
RUN virtualenv -p /usr/lib/python3.9 venv
RUN . ./venv/bin/activate
# install required pypi modules
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Finalization
CMD ["python3","-m","userbot"]
