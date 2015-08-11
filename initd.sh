#! /bin/sh

### BEGIN INIT INFO
# Provides:          random-server
# Required-Start:    $local_fs $network
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: random-server
# Description:       random-server
### END INIT INFO

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting random server "
    
    /usr/bin/python  /home/jgb/random-server/servidor-http-random-logger.py > /var/log/random-server

    ;;
  stop)
    echo "Stopping randome server"

    /usr/bin/killall servidor-http-random-logger.py
    ;;
  *)
    echo "Usage: /etc/init.d/random-server {start|stop}"
    exit 1
    ;;
esac

exit 0
