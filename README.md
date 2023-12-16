# WebEnsemble
Out of the box ensemble algorithms for regression problems with web-interface 

## Installation
To build, simply run
```
./scripts/build.sh
```
or
```
./scripts/d -b
```

## Run
To run program in attached mode, run
```
./scripts/run.sh
```
or
```
./scripts/d --debug -u
```
You can also combine it with program building (and any other flags):
```
./scripts/d --debug -bu
```
To run program in detached mode, run
```
./scripts/d -u
```
To attach to the detached program, run
```
./scripts/d -a
```
The server will be created on [http://localhost/](http://localhost/)

## Finish execution
To stop the attached running program, press Ctrl-C once. Do not press Ctrl-C multiple times, because it will cause the abortion of the program and you may lose your data. \
To stop the detached program, run
```
./scripts/d -s
```
