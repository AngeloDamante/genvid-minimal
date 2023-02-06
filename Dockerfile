FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true
ENV GENVID_DIR="/genvid"

# add USER
ARG CNT_USER="GENVID"
RUN useradd -m -s /bin/bash ${CNT_USER}

# add utility layer
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y --no-install-recommends \
    nano \
    wget \
    curl \
    xz-utils

# add python layer
ENV PYTHONPATH "${PYTHONPATH}:${GENVID_DIR}"
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.8 \
    python3-pip \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# add layer for vision
RUN apt-get -y update && apt-get install -y ffmpeg libsm6 libxext6

# add layer for repo requirements
COPY ["requirements.txt", "${GENVID_DIR}/requirements.txt"]
RUN pip3 install -r ${GENVID_DIR}/requirements.txt

# add scripts
COPY ["create_random_route.py", "${GENVID_DIR}/create_random_route.py"]
COPY ["create_random_sequence.py", "${GENVID_DIR}/create_random_sequence.py"]
COPY ["create_video.py", "${GENVID_DIR}/create_video.py"]
COPY ["generate_random_dataset.py", "${GENVID_DIR}/generate_random_dataset.py"]

# add videos for quick example
ADD https://github.com/fabian57fabian/genvid-minimal/releases/download/video2/backgrounds1.tar.xz /
RUN mkdir -p $GENVID_DIR/backgrounds
RUN tar -xf backgrounds1.tar.xz -C ${GENVID_DIR}/backgrounds

# permits
RUN chmod -R 777 ${GENVID_DIR}
RUN chown -R ${CNT_USER}:${CNT_USER} ${GENVID_DIR}