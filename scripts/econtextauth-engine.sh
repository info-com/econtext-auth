#!/bin/sh

### BEGIN INIT INFO
# Provides:          eContext Authentication/Authorization Engine
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start eContext Authentication/Authorization Engine at boot time
# Description:       Enable service provided by the eContext Authentication/Authorization Engine.
### END INIT INFO

###
#
###

export LC_ALL=en_US.UTF-8

dir="/opt/econtext-auth/"
cmd="/opt/econtext-auth/bin/econtextauth-engine -v"
user="econtext"

name=`basename $0`
pid_file="/tmp/$name.pid"
stdout_log="/var/log/$name.log"
stderr_log="/var/log/$name.err"

get_pid() {
    cat "$pid_file"
}

is_running() {
    [ -f "$pid_file" ] && ps `get_pid` > /dev/null 2>&1
}

case "$1" in
    start)
    if is_running; then
        echo "Already started (`get_pid`)"
    else
        echo "Starting $name"
        cd "$dir"
        if [ -z "$user" ]; then
            su $user -c '$cmd' >> $stdout_log 2>&1 &
        else
            $cmd >> $stdout_log 2>&1 &
        fi
    fi
    ;;
    stop)
    if is_running; then
        echo -n "Stopping $name.."
        kill `get_pid`
        for i in {1..10}
        do
            if ! is_running; then
                break
            fi

            echo -n "."
            sleep 1
        done
        echo

        if is_running; then
            echo "Not stopped; may still be shutting down or shutdown may have failed"
            exit 1
        else
            echo "Stopped"
            if [ -f "$pid_file" ]; then
                rm "$pid_file"
            fi
        fi
    else
        echo "Not running"
    fi
    ;;
    reload)
    if is_running; then
        current_pid=`get_pid`
        CURRENT_WORKERS=$((`eval /usr/bin/pgrep -P $current_pid | wc -l`))
        NEEDED_WORKERS=$((CURRENT_WORKERS * 2))
        pgrep_taxonomy="/usr/bin/pgrep -f $name | wc -l"
        echo "Current workers: ${CURRENT_WORKERS} - need ${NEEDED_WORKERS}"
        echo -n "Reloading $name.."
        kill -USR2 $current_pid

        while [ $((`eval $pgrep_taxonomy`)) -lt $NEEDED_WORKERS ]
        do
            echo -n "."
            sleep 1
        done
        echo

        echo "Stopping retired workers"
        kill -TERM $current_pid
    else
        echo "Not running"
    fi
    ;;
    restart)
    $0 stop
    sleep 1
    if is_running; then
        echo "Unable to stop, will not attempt to start"
        exit 1
    fi
    $0 start
    ;;
    status)
    if is_running; then
        echo "Running (`get_pid`)"
    else
        echo "Stopped"
        exit 1
    fi
    ;;
    *)
    echo "Usage: $0 {start|stop|reload|restart|status}"
    exit 1
    ;;
esac

exit 0
                                                                                                                                                                                                          120,1         Bot
