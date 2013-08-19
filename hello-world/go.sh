#!/usr/bin/env bash

# Pre-reqs:
#   - in a virtualenv with flow (we can make a script in the top level
#                                examples that does this setup)
#   - redis-server in path, version >= $REQUIRED_REDIS_VERSION
#   - FLOW_RABBITMQ_HOST set
REQUIRED_REDIS_VERSION=2.6



set -o errexit

cleanup() {
    kill $(jobs -p) &> /dev/null || true
    rabbitmqadmin -H $FLOW_RABBITMQ_HOST delete vhost name=$RMQ_VHOST &> /dev/null || true
}
trap cleanup EXIT



# Verify pre-reqs
if [ -z $FLOW_RABBITMQ_HOST ]; then
    echo "FLOW_RABBITMQ_HOST not set -- please set it to a rabbitmq hostname" 1>&2
    exit 1
fi

REDIS_VERSION=$(redis-server --version | sed -rn 's/.* v=([[:digit:]]+\.[[:digit:]]+)\.[[:digit:]]+.*/\1/p')
if [ -z $REDIS_VERSION ]; then
    echo "Could not determine version of redis-server in path (requires >= $REQUIRED_REDIS_VERSION)" 1>&2
    exit 1
elif [ 0 -ne `echo "$REDIS_VERSION < $REQUIRED_REDIS_VERSION" | bc` ]; then
    echo "redis-server version too low (requires >= $REQUIRED_REDIS_VERSION)" 1>&2
    exit 1
fi

# Attempt to verify we're in our own virtualenv
if [ ! -w `which flow` ]; then
    echo "flow executable not writable, this suggests you are not running a flow virtualenv" 1>&2
    exit 1
fi


python setup.py develop


TEMPDIR=`mktemp -d`

REDIS_SOCKET_PATH=${TEMPDIR}/redis.sock
redis-server `pwd`/config/redis.conf --unixsocket $REDIS_SOCKET_PATH > /dev/null &

# XXX Dynamically generate the vhost?
RMQ_VHOST=hello-world
rabbitmqadmin -H $FLOW_RABBITMQ_HOST declare vhost name=$RMQ_VHOST > /dev/null
rabbitmqadmin -H $FLOW_RABBITMQ_HOST declare permission vhost=$RMQ_VHOST \
    user=guest configure='.*' write='.*' read='.*' > /dev/null


# write temporary config
FLOW_CONFIG_FILE=${TEMPDIR}/flow.yaml
echo "amqp:" > $FLOW_CONFIG_FILE
echo "    hostname: $FLOW_RABBITMQ_HOST" >> $FLOW_CONFIG_FILE
echo "    vhost: $RMQ_VHOST" >> $FLOW_CONFIG_FILE
echo >> $FLOW_CONFIG_FILE
echo "redis:" >> $FLOW_CONFIG_FILE
echo "    unix_socket_path: $REDIS_SOCKET_PATH" >> $FLOW_CONFIG_FILE



export FLOW_CONFIG_PATH=$TEMPDIR:`pwd`/config

flow configure-rabbitmq
flow orchestrator &
flow hello-world


sleep 1
