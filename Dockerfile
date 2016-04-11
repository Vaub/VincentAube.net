FROM nginx

RUN apt-get update && \
    apt-get -y install python-pip

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY . /tmp/
RUN pelican -t /tmp/theme /tmp/content && \
    cp -a /tmp/output/. /usr/share/nginx/html
