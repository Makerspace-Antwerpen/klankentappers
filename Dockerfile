FROM balenalib/%%BALENA_MACHINE_NAME%%-debian-python:3.9.1

RUN install_packages curl wget build-essential libelf-dev awscli bc flex libssl-dev python bison alsa-utils libportaudio2 libsndfile1

#TODO pip modules still need to be adapted for full use of the repo
RUN pip install sounddevice configparser numpy rx scipy paho-mqtt adafruit-python-shell

COPY ./src /usr/src/app
WORKDIR /usr/src/app

# build the kernel module for the i2s mic
ENV VERSION '2.47.0+rev1.prod 2.50.4+rev1.prod'
ENVUDEV = on
RUN BALENA_MACHINE_NAME=%%BALENA_MACHINE_NAME%% ./build.sh build --device %%BALENA_MACHINE_NAME%% --os-version "$VERSION" --src example_module



CMD ["python3", "/usr/src/app/recordEvents.py"]
#CMD [ "balena-idle" ]
