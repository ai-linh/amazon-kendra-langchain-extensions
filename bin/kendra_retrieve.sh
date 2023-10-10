#!/bin/bash

aws kendra retrieve --index-id 8fd768a8-909c-4a3c-981c-fba69e7a3fe3 --page-size 1 --query-text "$*" --debug