#!/bin/bash - 
#===============================================================================
#
#          ENV_FILE: npm-insteller.sh
# 
#         USAGE: ./npm-insteller.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YuShan Huang, samhuang749@gmail.com
#  ORGANIZATION: 
#       CREATED: 2022/04/07
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

# check .env.local file and cp to current directory
ENV_FILE=../my_env/.env.local
if [ -f "$ENV_FILE" ]; then
    echo "$ENV_FILE exists."
    cp "$ENV_FILE" .
else
    echo "$ENV_FILE does not exist."  
fi

npm install
npm run build
cp -r ./dist/* ./volume-to-host
tail -f /dev/null