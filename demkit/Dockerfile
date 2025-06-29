# Copyright 2023 University of Twente

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Use an official Python runtime as a parent image
FROM python:3.11.2-bullseye

# Install packages
RUN apt-get update && apt-get -y install git libzmq3-dev

WORKDIR /app/demkit
COPY demkit/requirements.txt . 
RUN pip install uv
RUN uv pip install -r requirements.txt --system

WORKDIR /app/demkit

# Copy the sources that we require
COPY demkit/conf /app/demkit/conf
COPY demkit/tmp /app/demkit/tmp
COPY demkit/tools /app/demkit/tools
COPY demkit/demkit.py /app/demkit/
COPY demkit/docker /app/demkit/docker

RUN mv /app/demkit/conf/usrconf.docker.py /app/demkit/conf/usrconf.py

RUN mkdir /app/demkit/components
RUN mkdir /zmq
RUN mkdir /app/workspace
RUN mkdir /scripts

WORKDIR /app/demkit/docker

# # Do some other things like copying the config internally
# RUN cp -f usrconf.py ../conf

WORKDIR /app/demkit/docker/scripts
RUN cp -Rf * /scripts

WORKDIR /app/demkit/
RUN rm -Rf docker

# Set the default environment variables
ENV DEMKIT_FOLDER=example
ENV DEMKIT_MODEL=demohouse
ENV DEMKIT_COMPONENTS=/app/demkit/components/

ENV DEMKIT_INFLUXURL=http://demkit_influxdb
ENV DEMKIT_INFLUXPORT=8086
ENV DEMKIT_INFLUXDB=dem
ENV DEMKIT_INFLUXUSER=demkit
ENV DEMKIT_INFLUXPASSWORD=WZ5LE3nblOQwpWHrr3m5
ENV DEMKIT_INFLUXTOKEN=-WF-JsrugNAZbl4mZJrfT3H6GNXdtNrRWXM-yzuECUJv8XiZqdan0tGq3MFnaEzDRIodcit3Sg0Qh6UiEKZsgg==

# Now setup DEMKit itself
WORKDIR /app/demkit

# Add volumes
VOLUME /app/demkit/components
VOLUME /app/workspace

ENV PATH="$PATH:/scripts"

EXPOSE 3001

# Run app.py when the container launches
CMD sh /scripts/autoexec.sh