FROM debian

RUN echo 'deb http://ftp.debian.org/debian/ stretch main' >> /etc/apt/sources.list

RUN apt-get update -y && apt-get install -y \
  cmake \
  g++-5 \
  gdb

RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 1
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 1
RUN update-alternatives --install /usr/bin/cpp cpp-bin /usr/bin/cpp-5 1
RUN update-alternatives --set g++ /usr/bin/g++-5
RUN update-alternatives --set gcc /usr/bin/gcc-5
RUN update-alternatives --set cpp-bin /usr/bin/cpp-5
