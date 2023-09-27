FROM ubuntu:22.04
RUN echo 'APT::Install-Suggests "0";' >> /etc/apt/apt.conf.d/00-docker
RUN echo 'APT::Install-Recommends "0";' >> /etc/apt/apt.conf.d/00-docker
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update \
    && apt-get install -y python3.10 \
    && apt-get install -y python3-pip \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /bom-server

# COPY ./static /bom-server/staticfiles/
COPY . /bom-server/

RUN ls -ltrh

ENV PIP_INDEX_URL=https://pypi.iranrepo.ir/simple
# RUN pip install --upgrade pip
RUN pip install gunicorn

ADD ./requirements.txt /bom-server/
RUN pip install --no-cache-dir -r requirements.txt

# RUN python3 manage.py collectstatic --noinput

RUN chmod +x /bom-server/docker/configuration/server-entrypoint.sh
RUN chmod +x /bom-server/docker/configuration/worker-entrypoint.sh