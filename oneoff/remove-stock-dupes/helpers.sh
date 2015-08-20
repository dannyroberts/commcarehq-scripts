function psql_commcarehq() {
  psql $PSQL_ARGS commcarehq
}

function remove-header-and-footer() {
  sed 1,2d | sed '$d' | sed '$d'
}

function get-unique-duplicates() {
  uniq -c | grep '^ *[^1 ]' | sed 's/^ *[0-9]* *//'
}

function unpad-psql-table() {
  sed 's/^ *//' | sed 's/ *$//' | sed 's/ *| */|/g'
}

function rows-to-tuple-tuple() {
  unpad-psql-table | sed 's/^\(.*\)$/'"('\1')/" | sed "s/|/','/g" | python -c "import sys; print '(' + ','.join(sys.stdin.readlines()) + ')'"
}

function render-sql-template-from-rows() {
  python -c 'import sys; print open("'"$1"'").read().format(rows=sys.stdin.read()),'
}

function mark-duplicates() {
  skip_columns=$1
  f=$(python -c "print $skip_columns + 1")
  while read line
  do
    CURRENT_LINE=$(echo $line | cut -d'|' -f$f-)
    if [[ $CURRENT_LINE = $PREV_LINE ]]
    then
      echo '✗' $line
    else
      echo '✓' $line
    fi
    PREV_LINE=$CURRENT_LINE
  done
}

function pull-report-id-field-from-dupe-rows() {
  grep '^✗' | unpad-psql-table | cut -d'|' -f2
}
