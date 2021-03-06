# IBT: Isolated Build Tool

[![View on PyPI](https://img.shields.io/pypi/v/ibt.svg)](https://pypi.python.org/pypi/ibt)
[![Licence](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/rcook/ibt/master/LICENSE)

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

Ensure you have a working [Python 2.7][python] installation:

```bash
pip install --user ibt
```

You can also clone from this repository and perform a dev install:

```bash
git clone https://github.com/rcook/ibt.git
cd ibt
pip install --user -e .
```

Note that Pip installs scripts to `$HOME/.local/bin` by default (varies based on platform), so make sure that this path is available on the system search path (via the `PATH` environment variable). You can do this by appending this in your `.bashrc` or other shell configuration script:

```bash
echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
```

## Standard commands

* `destroy`: destroys the project's Docker image
* `help`: display help
* `info`: shows system and project information
* `run`: runs a command inside a Docker container
* `script`: runs a script inside a Docker container
* `shell`: runs an interactive shell inside a Docker container
* `up`: creates Docker image for the project after optionally building base Docker image

All commands have available to them the following environment variables:

* `IBTALIASARGS`: additional arguments passed on the command line to aliases
* `IBTPROJECTDIR`: the current project directory in the container
* `IBTUSER` and `USER`: the user name

## `Ibtfile` settings

Configuration for any given project is driven by the contents of the `Ibtfile`
settings file which should be placed in the root directory of the project.
Alternatively, an `.ibtprojects` file placed in the user's home directory can
be used to specify the location of the `Ibtfile` for zero or more project root
directories for situations where the IBT configuration must be kept out of the
source tree.

* `aliases`: (optional) one or more project-specific command aliases
* `docker`: specifies base Docker image information for project including
* `env_vars`: (optional) one or more environment variables to define inside
container
`image` and `build`
* `ports`: (optional) one or more host port-container port pairs to
* `container-project-dir`: (optional) specifies directory to which project
directory is mapped in container
configure port forwarding
* `volumes`: (optional) one or more additional volumes to mount inside
container

### Environment variable settings

The environment section contain multiple environment variables to be set in the container. 
The key represents the environment variable to be created. The value contains either the value or a reference to
a substitution. A Substitution value starts with a `$` and is resolved against the environment variable map. If the variable 
is not found, the environment variable is looked up on the host.   
    
```yaml
env_vars:
    ARTIFACTORY_APIKEY: $ARTIFACTORY_APIKEY
    ARTIFACTORY_USER: BOB_THE_BUILDER
    COMPOSITE_KEY: $ARTIFACTORY_USER@$HOST
```

### Volumes settings

The volume section contains multiple keys and values. 
The key refers to a path on the host and the value contains the path in the container. 

```yaml
volumes:  
   host-path: container-path
```

Key and values support variable expansion like the environment variables.

```yaml
volumes:  
   $HOME/.kube: /home/$USER/.kube
   $HOME/.aws: /home/$USER/.aws
```

## Sample project

### Create Docker images

All build commands will run inside a fully isolated Debian-based Docker container as specified by the project configuration in `Ibtfile`. First, create the base Docker images:

```bash
cd docker
pushd debian-gcc
make build
popd
pushd debian-gcc-python
make build
popd
pushd debian-gcc6
make build
popd
docker images
```

This creates `debian-gcc` which contains basic build tools, CMake and gdb and `debian-gcc-python` which extends this with the addition of Python 2.7. `debian-gcc6` includes the GCC 6 toolchain. The last command will list locally available Docker images which will now include `ibt/debian-gcc` and `ibt/debian-gcc-python` etc.

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
-- The C compiler identification is GNU 6.3.0
-- The CXX compiler identification is GNU 6.3.0
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
$ ibt info
IBT: Isolated Build Tool
https://github.com/rcook/ibt

System information:
  Docker:              installed

Context information:
  Working directory:   /home/user/src/ibt/example
  User:                user (1002)
  Group:               group (1003)

Project information:
  Project directory:   /home/user/src/ibt/example
  Project ID:          789dbc504a0690d786ddd43474dfbcc5
  Configuration file:  /home/user/src/ibt/example/Ibtfile
  Temporary directory: /home/user/src/ibt/example/.ibt

Project user information:
  User:                user (1002)
  Group:               group (1003)

Docker container information:
  Docker image ID:     ibt-789dbc504a0690d786ddd43474dfbcc5
  Project directory:   /example
  Temporary directory: /example/.ibt
  Docker base image:   ibt/debian-gcc6

IBT status:
  Temporary directory: exists
  Docker image:        built

Project aliases:
  cmake = run 'cd $IBTPROJECTDIR && mkdir -p build && cd build && cmake -DCMAKE_BUILD_TYPE=Debug ..'
  debug = shell /bin/sh -c 'cd $IBTPROJECTDIR/build && gdb ./hello-world'
  exec = run 'cd $IBTPROJECTDIR/build && ./hello-world'
  make:
  - cd $IBTPROJECTDIR/build
  - make
$ ibt destroy
Destroying Docker image ibt-789dbc504a0690d786ddd43474dfbcc5
```

## Developer guide

[See developer guide][developer-guide]

## Licence

Released under MIT License

Copyright &copy; 2016, Richard Cook. All rights reserved.

[developer-guide]: DEV.md
[docker]: https://www.docker.com/
[pip]: https://pip.pypa.io/en/stable/installing/
[python]: https://www.python.org/downloads/
[vagrant]: https://www.vagrantup.com/
[virtualenv]: https://virtualenv.pypa.io/en/stable/
