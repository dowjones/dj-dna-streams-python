#!/usr/bin/env bash

# NOTE: 2017-01-28: fleschec: Run this only if advised by Dow Jones Data Engineering support.

USER_KEY=$1
SUBSCRIPTION_ID=$2
ENV=$3

${USER_KEY:?"Need to set USER_KEY environment variable."}
${SUBSCRIPTION_ID:?"Need to set SUBSCRIPTION_ID environment variable."}
${ENV:?"Need to set ENV environment variable."}

TIMEOUT=180 # NOTE: 2017-01-25: fleschec: In seconds
NAME="dj-dna-streaming-python-asdvkds-for-testing-only"

run_docker() {
  echo "Current directory: $(pwd)"

  docker stop $NAME
  docker rm $NAME

  # NOTE: 2017-01-28: fleschec: This step could be placed in its own method and a timeout set on that method. If it takes too long
  # then we can time it out; then immediately fail the test.
  docker build -f ./DockerfileDemo . -t $NAME-tag
  build_return_code=$?

  docker run \
  --name=$NAME \
  -e USER_KEY=$USER_KEY \
  -e SUBSCRIPTION_ID=$SUBSCRIPTION_ID \
  -e EXTRACTION_API_HOST="https://extraction-api-dot-djsyndicationhub-$ENV.appspot.com" \
  -e QUIET_DEMO=true \
  $NAME-tag
}

stop_docker() {
  echo
  echo "Stopping the docker container $NAME..."
  echo
  docker stop $NAME
}

# NOTE: 2017-01-28: fleschec: Monitor running background process. Times out eventually.
waitThen() {
  local funcOnTimeout=$1
  local elapsed_time=0
  while :
  do
      # NOTE: 2017-01-28: fleschec: Get all the system processes, filter by process id; ignore the grep process, and do not print to screen.
      ps ax | grep $pid | grep -v grep >> /dev/null

      # NOTE: 2017-01-28: fleschec: Get the output of hte last command.
      ret=$?
      if [ "$ret" != "0" ]
      then
          echo "Test fails! Monitored pid ended. This means that the process appears to have ended prematurely."
          exit 1
          break
      fi
      sleep 5

      elapsed_time=$(($elapsed_time + 5))

      echo
      echo "elapsed_time (seconds): $elapsed_time"
      echo

      # NOTE: 2017-01-28: fleschec: If elapsed time is greater than the allowed maximum time, then stop.
      if [ $elapsed_time -gt $TIMEOUT ]
      then
        echo "Test successful! Timing out. Shutting down ...".
        $funcOnTimeout
        exit 0
        break
      fi
  done
}

# NOTE: 2017-01-28: fleschec: Script to run in background (&)
run_docker &

# NOTE: 2017-01-28: fleschec: Process ID of the most recently started process.
pid=$!

waitThen stop_docker