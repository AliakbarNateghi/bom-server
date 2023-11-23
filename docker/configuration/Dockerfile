FROM ubuntu:22.04
RUN echo 'APT::Install-Suggests "0";' >> /etc/apt/apt.conf.d/00-docker
RUN echo 'APT::Install-Recommends "0";' >> /etc/apt/apt.conf.d/00-docker

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y python3.10 python3-pip \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
    && python3 --version \
    && pip3 --version \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ENV HOME=/home/bom-server/
ENV APP_HOME=/bom-server
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
# RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

# WORKDIR /bom-server

# COPY ./static /bom-server/staticfiles/
COPY . /bom-server/

# ENV PIP_INDEX_URL=https://pypi.iranrepo.ir/simple
# RUN pip install --upgrade pip
# RUN pip install gunicorn

ADD ./requirements.txt /bom-server/
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install -r requirements.txt

# RUN python3 manage.py collectstatic --noinput


RUN chmod +x /bom-server/docker/configuration/server-entrypoint.sh
# RUN chmod +x /bom-server/docker/configuration/worker-entrypoint.sh