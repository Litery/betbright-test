#!/usr/bin/env bash
while true; do
    printf "$ ";
    read var;
    python betbright/application/cli.py $var;
done
