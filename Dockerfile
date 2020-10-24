FROM jrottenberg/ffmpeg:4.3.1-ubuntu1804
LABEL authors="Selenium <selenium-developers@googlegroups.com>"
LABEL authors="Gabriel Meghnagi <gabrielmeghnagi@outlook.it>"

#================================================
# Customize sources for apt-get
#================================================
RUN  echo "deb http://archive.ubuntu.com/ubuntu bionic main universe\n" > /etc/apt/sources.list \
  && echo "deb http://archive.ubuntu.com/ubuntu bionic-updates main universe\n" >> /etc/apt/sources.list \
  && echo "deb http://security.ubuntu.com/ubuntu bionic-security main universe\n" >> /etc/apt/sources.list

# No interactive frontend during docker build
ENV DEBIAN_FRONTEND=noninteractive \
    DEBCONF_NONINTERACTIVE_SEEN=true
EXPOSE 5000
#========================
# Supervisor
#========================
RUN apt-get -qqy update \
    && apt-get -qqy --no-install-recommends install \
    gcc python3-dev curl wget vim python3.6 python3-pip supervisor x11-xserver-utils \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/* 
RUN pip3 install setuptools \
    && pip3 install psutil flask python-dotenv

#======================================
# Add Supervisor configuration file
#======================================
COPY supervisord.conf /etc
COPY ./src/ /opt/bin/

RUN mkdir -p /var/run/supervisor /var/log/supervisor /videos \
    && cd /opt/bin/tester \ 
    && pip3 install -e . \
    && ln -s /videos /opt/bin/tester/tester/static/videos

WORKDIR /opt/bin/tester
ENTRYPOINT ["/opt/bin/entry_point.sh"]
CMD ["/opt/bin/entry_point.sh"]
