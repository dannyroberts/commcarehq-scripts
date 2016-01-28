user=$1
db=https://cloudant.com/db/commcarehq/commcarehq
curl -u $user "$db/_design/all_docs/_view/by_doc_type?descending=true&group=true&group_level=1"
