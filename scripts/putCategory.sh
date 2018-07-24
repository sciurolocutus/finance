#!/bin/bash
jwt=$1
categoryId=1
if [[ ! -z "$2" ]]
	then categoryId="$2"
fi
category="category.json"
if [[ ! -z "$3" ]]
	then category="$3"
fi
curl -v -X PUT "http://127.0.0.1:5000/categories/${categoryId}" -H "Authorization: JWT ${jwt}" -H 'Content-Type: application/json' -d @${category}
