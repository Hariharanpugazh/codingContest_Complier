#!/bin/bash

LANGUAGE=$1
SOURCE_CODE=$2
INPUT_DATA=$3

case $LANGUAGE in
  "python")
    python3 "$SOURCE_CODE" < "$INPUT_DATA"
    ;;
  "c")
    gcc "$SOURCE_CODE" -o code && ./code < "$INPUT_DATA"
    ;;
  "cpp")
    g++ "$SOURCE_CODE" -o code && ./code < "$INPUT_DATA"
    ;;
  "java")
    javac "$SOURCE_CODE" && java Main < "$INPUT_DATA"
    ;;
esac
