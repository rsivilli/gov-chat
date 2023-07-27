#!/bin/sh -e
#
# https://github.com/starjuice/wait-for-entrypoint
#
# WAIT_FOR_SERVICES      - Space-delimited list of host:port TCP services.
#                          E.g. webserver:443 or 10.0.0.4:80.
# WAIT_FOR_SECONDS       - Seconds to wait for all services to become
#                          available. Defaults to infinity.
# WAIT_FOR_VERBOSE       - If "1", print message to stdout for each service.
# WAIT_FOR_AS_ENTRYPOINT - Unless "0", act as docker entrypoint for command-line
#                          arguments.
#

wait_forever() {
	host=${service%:*}
	port=${service#*:}
	if [ "${WAIT_FOR_VERBOSE}" = "1" ]; then
		echo Waiting for ${host}:${port}...
	fi
	if which nc >/dev/null 2>&1; then
		while ! nc $host $port >/dev/null 2>&1; do sleep 0.1; done
	elif which bash >/dev/null 2>&1; then
		while ! bash -c "echo > /dev/tcp/${host}/${port}" >/dev/null 2>&1; do sleep 0.1; done
	else
		echo $(basename $0): error: neither nc nor bash is available 1>&2
		exit 1
	fi
}

if [ "$1" = ":wait" ]; then
	for service in ${WAIT_FOR_SERVICES}; do
		wait_forever
	done
else
	if [ "${WAIT_FOR_SECONDS}" != "" -a "${WAIT_FOR_SECONDS}" != "infinity" ]; then
		timeout ${WAIT_FOR_SECONDS} $0 ":wait"
	else
		$0 ":wait"
	fi
	if [ "${WAIT_FOR_AS_ENTRYPOINT}" != "0" ]; then
		exec "$@"
	fi
fi