# ibt: The Isolated Build Tool

Simple wrappers around Docker etc. for fully isolated build environments

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

Once this is done, the following commands (configured as aliases in `Ibtfile`)
can be run to configure/make/run the project code:

* `ibt cmake`: generates CMake build directory
* `ibt make`: runs `make` inside CMake build directory
* `ibt exec`: runs target binary
* `ibt debug`: starts gdb and loads target binary

## Licence

Released under MIT License
Copyright (C) 2016, Richard Cook. All rights reserved.
