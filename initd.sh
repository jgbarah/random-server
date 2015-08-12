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

LOGFILE="/var/log/random-server-logger"
echo $LOGFILE
touch $LOGFILE

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting random server "
    echo -n "Starting... " >> $LOGFILE
    date --iso-8601="seconds" >> $LOGFILE
    /usr/bin/python  /home/jgb/random-server/random-server-logger.py 2>&1 >> $LOGFILE &

    ;;
  stop)
    echo $LOGFILE
    echo "Stopping random server"
    echo -n "Stopping... " >> $LOGFILE
    date --iso-8601="seconds" >> $LOGFILE
    /usr/bin/pkill "/usr/bin/python /home/jgb/random-server/random-server-logger.py"

    ;;
  *)
    echo "Usage: /etc/init.d/random-server {start|stop}"
    exit 1
    ;;
esac

exit 0
