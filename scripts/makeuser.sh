#!/bin/bash
username=$1
password=$2
curl -v -X POST 'http://127.0.0.1:5000/register' -d username=${username} -d password=${password}
