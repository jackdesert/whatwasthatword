#! /bin/bash

# this script is just a wrapper around dick so that it
# will start up again immediately if it ever dies
# Kind of like what a unicorn server would do
#
# The proper way to invoke this script is to call
#   nohup script/run_dick_indefinitely.sh &

# This reminder only displays in the terminal if you forget to invoke with 'nohup'
echo "REMINDER: call this with 'nohup' and a trailing '&'"

while true; do
  cd /home/dev/dick
  python3 dick-merriam.py
  sleep 2
  mkdir -p log
  echo "dick restarted `date`" >> log/dick_restart.log
done


