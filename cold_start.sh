#! /bin/bash

# builder of the services
# Dmitry Kisler © 2019
# admin@dkisler.com

SCRIPT_BASE_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

PORT_NOTEBOOK=9999
PATH_TO_NOTEBOOK=analytics/analytics.ipynb

msg () {
    echo "$(date +"%Y-%m-%d %H:%M:%S") $1"
}

get_os () {
    case "$OSTYPE" in
        solaris*) echo "SOLARIS" ;;
        darwin*)  echo "OSX" ;;
        linux*)   echo "LINUX" ;;
        bsd*)     echo "BSD" ;;
        msys*)    echo "WINDOWS" ;;
        *)        echo "unknown: $OSTYPE" ;;
    esac
}

OS=$(get_os)

docker_web () {
    msg "docker not installed. See https://docs.docker.com/install"
    if [ '${OS}' == 'OSX' ]; then
        open https://docs.docker.com/docker-for-mac/install/
        elif [ '${OS}' == 'LINUX' ]; then
        xdg-open https://docs.docker.com/install/linux/docker-ce/ubuntu/
        elif [ '${OS}' == 'WINDOWS' ]; then
        start https://docs.docker.com/docker-for-windows/install/
    fi
}

docker_compose_web () {
    msg "docker-compose not installed. See https://docs.docker.com/compose/install/"
    if [ '${OS}' == 'OSX' ]; then
        open https://docs.docker.com/compose/install/
        elif [ '${OS}' == 'LINUX' ]; then
        xdg-open https://docs.docker.com/compose/install/
        elif [ '${OS}' == 'WINDOWS' ]; then
        start https://docs.docker.com/compose/install/
    fi
}

check_docker_ver () {
    (docker -v > /dev/null) || (docker_web; exit 1)
    (docker-compose -v > /dev/null) || (docker_compose_web; exit 1)
}

run_docker_jupyter() {
    docker run -d \
    -v ${PWD}:/transfer \
    -p ${PORT_NOTEBOOK}:8888 \
    -t analytics/jupyter:1

    if [ $? -eq 0 ]; then
      url="http://localhost:${PORT_NOTEBOOK}/lab/tree/${PATH_TO_NOTEBOOK}"
      msg "Click ${url} to launch a notebook"

      if [ ${OS} == 'OSX' ]; then
          open ${url}
      elif [ ${OS} == 'LINUX' ]; then
          xdg-open ${url}
      elif [ ${OS} == 'WINDOWS' ]; then
          start ${url}
      else
        msg "Cannot open jupyter-lab in browser. Please try manually"
      fi

    fi
}

# verify docker
check_docker_ver || exit 1

# build service images
msg "Build docker images"
docker-compose -f ${SCRIPT_BASE_PATH}/cold-start.yaml build

# smoke test
msg "Run end2end smoke test"
sh smoke_test/runner.sh

msg "Launch jupyter-lab with analytics notebook"
run_docker_jupyter
#
msg "Happy task evaluation! :) 
Feel free to drop a line on admin@dkisler.com in case of questions."
