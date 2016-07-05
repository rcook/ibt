# ibt: The Isolated Build Tool

Simple wrappers around Docker etc. for fully isolated build environments

## What's the point of this?

Docker is great for building isolated environments for builds or applications.
For my tastes, however, it has a few usability issues associated with it:

* The commands are fiddly to use and difficult to remember
* Docker containers run as root by default resulting in files created on the
host as the root user, instead of the current user
* It's too easy to leave intermediate images and containers lying around

Note that this is a very personal list of perceived shortcomings. If these
aren't issues for you, then don't use this tool!

ibt makes Docker images and containers more development- and project-focused.
It encourages the following workflows:

* Editing of source files is carried out predominantly on the _host_ machine
* Building, running and debugging of targets is always carried out within the
Docker container
* Source code will typically be under the control of a VCS such as Git
* Source files should not be copied _en masse_ into the container
* Output files from builds etc. should be exposed directly to the host

## Standard commands

* `up`: creates Docker image for the project
* `destroy`: destroys the project's Docker image
* `run`: runs a command inside a Docker container
* `script`: runs a script inside a Docker container
* `shell`: runs an interactive shell inside a Docker container
* `status`: shows project status

## `Ibtfile` settings

* `docker-image`: specifies base Docker image for project
* `forwarded-ports`: (optional) one or more host:container port pairs to
configure port forwarding
* `aliases`: (optional) one or more project-specific command aliases

## Sample project

### Create Docker images

All build commands will run inside a fully isolated Debian-based Docker
container as specified by the project configuration in `Ibtfile`. First, create
the base Docker images:

```bash
$ cd docker-images/debian-gcc
$ make build
$ cd ../debian-gcc-python
$ make build
```

This creates `debian-gcc` which contains basic build tools, CMake and gdb and
`debian-gcc-python` which extends this with the addition of Python 2.7.

### Aliases

Once this is done, the following commands (configured as aliases in `Ibtfile`)
can be run to configure/make/run the project code:

* `ibt cmake`: generates CMake build directory
* `ibt make`: runs `make` inside CMake build directory
* `ibt exec`: runs target binary
* `ibt debug`: starts gdb and loads target binary

### Example workflow

```bash
$ ibt up
Building Docker image ibt-789dbc504a0690d786ddd43474dfbcc5
$ ibt cmake
-- The C compiler identification is GNU 4.9.2
-- The CXX compiler identification is GNU 4.9.2
-- Check for working C compiler: /usr/bin/cc
-- Check for working C compiler: /usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++
-- Check for working CXX compiler: /usr/bin/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Configuring done
-- Generating done
-- Build files have been written to: /ibt/build
$ ibt make
Scanning dependencies of target hello-world
[100%] Building CXX object CMakeFiles/hello-world.dir/hello-world.cpp.o
Linking CXX executable hello-world
[100%] Built target hello-world
$ ibt exec first second third
Hello world
argc=4
argv[0] = ./hello-world
argv[1] = first
argv[2] = second
argv[3] = third
$ ibt status
ibt: The Isolated Build Tool

Project information:
  Project directory:   /home/user/src/ibt
  Working directory:   /home/user/src/ibt
  Project ID:          789dbc504a0690d786ddd43474dfbcc5
  Configuration file:  /home/user/src/ibt/Ibtfile
  Temporary directory: /home/user/src/ibt/.ibt
User information:
  UID:                 1002
  GID:                 1002
Docker information:
  Docker image ID:     ibt-789dbc504a0690d786ddd43474dfbcc5
IBT status:
  Temporary directory: exists
  Docker image:        built

Project aliases:
  cmake = run 'cd /ibt && if [ ! -d build ]; then mkdir build; fi && cd build && cmake -DCMAKE_BUILD_TYPE=Debug ..'
  debug = shell /bin/sh -c 'cd /ibt/build && gdb ./hello-world'
  exec = run 'cd /ibt/build && ./hello-world'
  make = run 'cd /ibt/build && make'

$ ibt destroy
Destroying Docker image ibt-789dbc504a0690d786ddd43474dfbcc5
```

## Licence

Released under MIT License
Copyright (C) 2016, Richard Cook. All rights reserved.
