FROM python:3.6-slim

# Install Python tools (git + pipenv)
RUN apt-get update && apt-get install -y git
RUN pip install pipenv

# Install gcloud tools
# (commands taken from https://cloud.google.com/storage/docs/gsutil_install#deb)
RUN apt-get update && apt-get install -y lsb-release apt-transport-https curl gnupg git
RUN export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && apt-get install -y google-cloud-sdk

# Install pyflame (for statistical profiling) if this script is run with PROFILE_CPU flag
ARG INSTALL_CPU_PROFILER="false"
RUN if [ "$INSTALL_CPU_PROFILER" = "true" ]; then \
        apt-get update && apt-get install -y autoconf automake autotools-dev g++ pkg-config python-dev python3-dev libtool make && \
        git clone https://github.com/uber/pyflame.git /pyflame && cd /pyflame && git checkout "v1.6.7" && \
        ./autogen.sh && ./configure && make && make install && \
        rm -rf /pyflame; \
    fi
    
# Set working directory
WORKDIR /app

# Install project dependencies.
ADD Pipfile /app
ADD Pipfile.lock /app
RUN pipenv sync

# Make a directory for intermediate data
RUN mkdir /data

# Copy the rest of the project
ADD project_test /app/project_test
ADD code_schemes/*.json /app/code_schemes/
ADD test_pipeline.py /app
