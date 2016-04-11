FROM nginx

RUN apt-get update && \
    apt-get -y install python-pip

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY . /tmp/
RUN cd /tmp/ && \
    pelican -t /tmp/theme -s /tmp/publishconf.py -o /usr/share/nginx/html /tmp/content
