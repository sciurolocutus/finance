#!/bin/bash
username=$1
password=$2
echo curl -v -X POST 'http://127.0.0.1:5000/auth' -H "Content-Type: application/json" -d "\"{\"username\": \"${username}\", \"password\": \"${password}\"}\""
curl -v -X POST 'http://127.0.0.1:5000/auth' -H "Content-Type: application/json" -d "{\"username\": \"${username}\", \"password\": \"${password}\"}"

