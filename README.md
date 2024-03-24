# Datac Consumer


## Install Poetry
```
$ curl -sSL https://install.python-poetry.org | python3 -
$ export PATH="/home/pi/.local/bin:$PATH"
```

## Start Application

``` 
$ Poetry install
$ nohup poetry run python3 src/main.py > datac-consumer.log 2>&1 </dev/null &
```

## Monitor Datac-Consumer Process

Use the `datac-consumer-monitor.sh` script in order to monitor the datac-consumer process. It checks the status of the datac-consumer process every 30 seconds. If the process is not running due to a failure, the script will restart it. 

```
nohup ./datac-consumer-monitor.sh > /dev/null 2>&1 &
```

The script creates a log file like this:

```
$ cat datac_consumer_monitor.log
2024-03-24 13:46:40 - OK
2024-03-24 13:47:10 - OK
2024-03-24 13:47:40 - Started the process
2024-03-24 13:48:11 - OK
2024-03-24 13:48:41 - OK
```


