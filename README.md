# ibt

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
