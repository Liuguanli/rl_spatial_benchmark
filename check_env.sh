#!/bin/bash

declare -A libraries=(
    [spatialindex]="/home/$(whoami)/usr"
    [geos]="/usr/local"
)

# Iterate through the libraries associative array
for library in "${!libraries[@]}"; do
    INSTALL_PREFIX=${libraries[$library]}
    echo -e "${NC}Checking ${library} in ${INSTALL_PREFIX}..."

    # Check include directory
    if [ -d "${INSTALL_PREFIX}/include/${library}" ]; then
        echo -e "${NC}${library} include directory exists."
    else
        echo -e "${RED}${library} include directory does not exist.${NC}"
        exit 1
    fi

    # Check lib directory for .so files
    if ls ${INSTALL_PREFIX}/lib/lib${library}*.so 1> /dev/null 2>&1; then
        echo -e "${NC}${library} library files exist."
    else
        echo -e "${RED}${library} library files do not exist.${NC}"
        exit 1
    fi
done
