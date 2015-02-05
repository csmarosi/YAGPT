#!/bin/sh

echo >| main.log
#TODO: it is confusing how non-interactiveness is handled between different
# version of gdb, especially when to flush output; therefore this hack:
nohup gdb --pid $(ps -ef | awk '/ ..[m]ain.out/{print $2}') < main.gdb 2>&1 >> main.log &
tail -f main.log
