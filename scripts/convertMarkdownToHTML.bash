#!/bin/bash

pandoc -f markdown -t html $1 > $2
