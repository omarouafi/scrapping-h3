FROM python:3.9-slim

RUN apt-get update && apt-get install -y wget unzip

RUN apt-get update \
    && apt-get install -y gnupg

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable



RUN apt-get install -y libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

CMD /wait-for-it.sh db:3307 -- python replicate_scrapping.py

