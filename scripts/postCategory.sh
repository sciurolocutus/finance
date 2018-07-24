#!/bin/bash
jwt=$1
category="category.json"
if [[ ! -z "$2" ]]
	then category="$2"
fi
curl -X POST "http://127.0.0.1:5000/categories" -H "Authorization: JWT ${jwt}" -H 'Content-Type: application/json' -d @${category}
