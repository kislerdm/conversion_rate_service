#! /bin/bash

# builder&runner for the services
# Dmitry Kisler © 2019
# admin@dkisler.com

SCRIPT_BASE_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
source ${SCRIPT_BASE_PATH}/.env_pipelines.sh

SERVICES='both'
BUILD_ONLY=0
FORCE=0

msg () {
    echo "$(date +"%Y-%m-%d %H:%M:%S") $1"
}

usage () {
    cat <<HELP_USAGE
    Service builder&launcher
    
    Run: sh $0 [--service --build_only --force]
    
    --service what services to build. Options: train, serve, both. [default: ${SERVICES}]
    --build_only build service images without spinning containers. Options: 0 - no, 1 - yes. [default: ${BUILD_ONLY}]
    --force force rebuild. Options: 0 - no, 1 - yes, [default: ${FORCE}]

HELP_USAGE
}

# parse arguments
while [ "$1" != "" ]; do
    case $1 in
        --build_only )          shift
                                BUILD_ONLY=$1
                                ;;
        --service )             shift
                                SERVICES=$1
                                ;;
        --force )               shift
                                FORCE=$1
                                ;;                                                                    
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

if [[ "${BUILD_ONLY}" != "0" && "${BUILD_ONLY}" != "1" ]]; then 
    usage
    exit 0
fi

if [[ "${FORCE}" != "0" && "${FORCE}" != "1" ]]; then 
    usage
    exit 0
fi

if [[ "${SERVICES}" != "both" && 
      "${SERVICES}" != "train" && 
      "${SERVICES}" != "serve" ]]; then
    usage
    exit 0
fi

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
    if [[ "${OS}" == "OSX" ]]; then
        open https://docs.docker.com/docker-for-mac/install/
        elif [[ "${OS}" == "LINUX" ]]; then
        xdg-open https://docs.docker.com/install/linux/docker-ce/ubuntu/
        elif [[ "${OS}" == "WINDOWS" ]]; then
        start https://docs.docker.com/docker-for-windows/install/
    fi
}

docker_compose_web () {
    msg "docker-compose not installed. See https://docs.docker.com/compose/install/"
    if [[ "${OS}" == "OSX" ]]; then
        open https://docs.docker.com/compose/install/
        elif [[ "${OS}" == "LINUX" ]]; then
        xdg-open https://docs.docker.com/compose/install/
        elif [[ "${OS}" == "WINDOWS" ]]; then
        start https://docs.docker.com/compose/install/
    fi
}

check_docker_ver () {
    (docker -v > /dev/null) || (docker_web; exit 1)
    (docker-compose -v > /dev/null) || (docker_compose_web; exit 1)
}

# verify docker
msg "Verify docker installation"
check_docker_ver
if [[ "$?" == "0" ]]; then msg "OK"; 
else msg "Missing required docker version, please check requirements";
fi

# build services
if [[ "${SERVICES}" == "both" ]]; then
    SERVICES=(train serve)
else
    SERVICES=(${SERVICES})
fi

for service in ${SERVICES[@]}; do
    cd ${SCRIPT_BASE_PATH}/app
    if [ ! -f compose-${service}.yaml ]; then
        msg "Compose file compose-${service}.yaml not found"
        cd ${SCRIPT_BASE_PATH}
        exit 1
    fi
    if [ ${BUILD_ONLY} -eq 1 ]; then
        docker-compose -f compose-${service}.yaml build
    else
        if [ ${FORCE} -eq 1 ]; then 
            docker-compose -f compose-${service}.yaml up --build
        else
            docker-compose -f compose-${service}.yaml up
        fi
    fi
    cd ${SCRIPT_BASE_PATH}
done

if [[ "$?" == "0" ]]; then
  msg "Done!"
fi