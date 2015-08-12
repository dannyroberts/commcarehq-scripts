COUCHDB=$1

function get-ids() {
  cat prod-stock-migration-0016.out | grep 'Problem Form IDs' | sed 's/Problem Form IDs: //' | sed 's/,/ /g' | xargs -n1 echo | sort
}

function get-received_on() {
  id=$1
  curl --basic $COUCHDB/commcarehq/$id |
    jsawk 'return this.received_on'
}

get-ids | while read id
do
  echo $id $(get-received_on $id)
done
