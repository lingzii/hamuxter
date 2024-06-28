# Multistage to build Hamuxter

# build python wheel
FROM python:3.11.9-slim-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libldap2-dev libsasl2-dev libssl-dev git

# install requirements
COPY ./server/requirements.txt .
RUN pip install --user -r requirements.txt

# build ffmpeg
FROM python:3.11.9-slim-bookworm AS ffmpeg-builder

ARG TARGETPLATFORM

COPY ./docker/ffmpeg_download.py .
RUN python ffmpeg_download.py $TARGETPLATFORM

# build final image
FROM python:3.11.9-slim-bookworm as hamuxter

ENV PYTHONUNBUFFERED 1

# copy build requirements
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# copy ffmpeg
COPY --from=ffmpeg-builder ./ffmpeg/ffmpeg /usr/bin/ffmpeg
COPY --from=ffmpeg-builder ./ffprobe/ffprobe /usr/bin/ffprobe

# install distro packages needed
RUN apt-get clean && apt-get -y update && \
    apt-get -y install --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# make folders
RUN mkdir /app /library /cache

# copy application into container
COPY ./server /app/server
COPY ./docker/run.sh /app

# volumes
VOLUME /library
VOLUME /cache

# start
WORKDIR /app
EXPOSE 8080

RUN chmod +x ./run.sh

CMD ["./run.sh"]