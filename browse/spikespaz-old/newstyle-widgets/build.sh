#! /bin/sh
ldc2 example.d -i -O3 -release
[ -e example.obj ] && rm example.obj
[ -e example.o ] && rm example.o
