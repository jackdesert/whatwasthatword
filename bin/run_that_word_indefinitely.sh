#! /bin/bash

# this script is just a wrapper around that-word so that it
# will start up again immediately if it ever dies
# Kind of like what a unicorn server would do
#
# The proper way to invoke this script is to call
#   nohup script/run_that_word_indefinitely.sh &

# This reminder only displays in the terminal if you forget to invoke with 'nohup'
echo "REMINDER: call this with 'nohup' and a trailing '&'"

while true; do
  cd /home/dev/whatwasthatword
  sudo uwsgi --plugin=python3 -s /tmp/whatwasthatword.sock --manage-script-name --mount /=wsgi:app --uid www-data --gid www-data
  sleep 2
  mkdir -p log
  echo "that-word restarted `date`" >> log/that_word_restart.log
done


