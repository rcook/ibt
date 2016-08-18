# IBT: Isolated Build Tool

Project- and build-oriented tool for working with [Docker][docker] images and
containers

## What's the point of this tool?

Docker is great for building isolated environments for builds or applications.
For my tastes, however, there are a few usability issues associated with it:

* The commands are fiddly to use and difficult to remember
* Docker containers run as root by default resulting in files created on the
host as the root user, instead of the current user
* It's too easy to leave intermediate images and containers lying around

Note that this is a very personal list of perceived shortcomings. If these
aren't issues for you, then don't use this tool!

IBT makes Docker images and containers more development- and project-focused.
It encourages the following workflows:

* Editing of source files is carried out predominantly on the _host_ machine
* Building, running and debugging of targets is always carried out within the
Docker container
* Source code will typically be under the control of a VCS such as Git
* Source files should not be copied _en masse_ into the container
* Output files from builds etc. should be exposed directly to the host

You'll notice that the commands strongly resemble those of [Vagrant][vagrant].
This is not completely accidental. The workflows described above strongly
resemble Vagrant workflows where `up`, `destroy`, `run` correspond closely to
`up`, `destroy` and `ssh`.

## Installation

Ensure you have a working [Python 2.7][python] installation on the host machine
as well as [Docker][docker]. Simply clone this repository and symlink the `ibt`
script into a directory on your search path. These instructions assume that the
`bin` directory within your home directory is on the search path:

```bash
$ git clone https://github.com/rcook/ibt.git
$ ln -sf $PWD/ibt/ibt $HOME/bin/ibt
```

You may need to install [pip][pip] and the YAML and Colorama packages as
follows:

```bash
$ python get-pip.py --user
$ pip install --user pyyaml
$ pip install --user colorama
```

## Standard commands

* `destroy`: destroys the project's Docker image
* `help`: display help
* `run`: runs a command inside a Docker container
* `script`: runs a script inside a Docker container
* `shell`: runs an interactive shell inside a Docker container
* `status`: shows project status
* `up`: creates Docker image for the project after optionally building base
Docker image

## `Ibtfile` settings

Configuration for any given project is driven by the contents of the `Ibtfile`
settings file which should be placed in the root directory of the project.
Alternatively, an `.ibtprojects` file placed in the user's home directory can
be used to specify the location of the `Ibtfile` for zero or more project root
directories for situations where the IBT configuration must be kept out of the
source tree.

* `aliases`: (optional) one or more project-specific command aliases
* `docker`: specifies base Docker image information for project including
`image` and `build`
* `ports`: (optional) one or more host port-container port pairs to
configure port forwarding
* `volumes`: (optional) one or more additional volumes to mount inside
container

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

See contents of `example` subdirectory.

```bash
$ cd example/
$ ibt up
Building Docker image ibt-789dbc504a0690d786ddd43474dfbcc5
$ ibt cmake
-- The C compiler identification is GNU 5.4.0
-- The CXX compiler identification is GNU 5.4.0
-- Check for working C compiler: /usr/bin/cc
-- Check for working C compiler: /usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
-- Check for working CXX compiler: /usr/bin/g++
-- Check for working CXX compiler: /usr/bin/g++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done
-- Generating done
-- Build files have been written to: /example/build
$ ibt make
Scanning dependencies of target hello-world
[ 50%] Building CXX object CMakeFiles/hello-world.dir/hello-world.cpp.o
[100%] Linking CXX executable hello-world
[100%] Built target hello-world
$ ibt exec first second third
Hello world
argc=4
argv[0] = ./hello-world
argv[1] = first
argv[2] = second
argv[3] = third
$ ibt status
IBT: Isolated Build Tool

Project information:
  Project directory:   /home/user/src/ibt/example
  Working directory:   /home/user/src/ibt/example
  Project ID:          789dbc504a0690d786ddd43474dfbcc5
  Configuration file:  /home/user/src/ibt/example/Ibtfile
  Temporary directory: /home/user/src/ibt/example/.ibt
User information:
  User:                user (1002)
  Group:               user (1002)
Docker container information:
  Docker image ID:     ibt-789dbc504a0690d786ddd43474dfbcc5
  Project directory:   /example
  Temporary directory: /example/.ibt
IBT status:
  Temporary directory: exists
  Docker image:        built

Project aliases:
  cmake = run 'cd $IBTPROJECTDIR && mkdir -p build && cd build && cmake -DCMAKE_BUILD_TYPE=Debug ..'
  debug = shell /bin/sh -c 'cd $IBTPROJECTDIR/build && gdb ./hello-world'
  exec = run 'cd $IBTPROJECTDIR/build && ./hello-world'
  make = run 'cd $IBTPROJECTDIR/build && make'

$ ibt destroy
Destroying Docker image ibt-789dbc504a0690d786ddd43474dfbcc5
```

## Licence

Released under MIT License

Copyright &copy; 2016, Richard Cook. All rights reserved.

[docker]: https://www.docker.com/
[pip]: https://pip.pypa.io/en/stable/installing/
[python]: https://www.python.org/downloads/
[vagrant]: https://www.vagrantup.com/
