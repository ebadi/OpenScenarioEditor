FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    git \
    libcairo2-dev \
    libdcmtk-dev \
    libgdal-dev \
    libgl1-mesa-dev \
    libgstreamer1.0-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    libpng-dev \
    libpoppler-dev \
    libpoppler-glib-dev \
    libpthread-stubs0-dev \
    libtiff-dev \
    libxinerama-dev \
    libxrandr-dev \
    libxml2-dev \
    pkg-config \
    python3-pip \
    python3-pyqt5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Build esmini (latest) — heavy step in its own layer for caching
RUN git clone --depth 1 https://github.com/esmini/esmini.git /tmp/esmini \
    && mkdir /tmp/esmini/build \
    && cd /tmp/esmini/build \
    && cmake ../ -DUSE_OSG=true -DCMAKE_BUILD_TYPE=Release \
    && make -j$(nproc) install \
    && mkdir -p /app/esmini \
    && cp /tmp/esmini/build/EnvironmentSimulator/Libraries/esminiLib/libesminiLib.so /app/esmini/ \
    && cp /tmp/esmini/build/EnvironmentSimulator/Libraries/esminiRMLib/libesminiRMLib.so /app/esmini/ \
    && cp -r /tmp/esmini/resources/ /app/esmini/resources/ \
    && rm -rf /tmp/esmini

# Copy application source last to maximise cache reuse on code changes
COPY . .

CMD ["python3", "OpenScenarioEditor.py"]
