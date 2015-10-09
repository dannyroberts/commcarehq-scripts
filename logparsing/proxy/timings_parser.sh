# usage:
# $ bash parse.sh production-timing.log
#
# file should be in format of file found at
# hqproxy4.internal.commcarehq.org:/home/cchq/www/production/log/production-timing.log

file=$1

cat $file |
  sed -E 's:/a/[0-9a-z-]+:/a/*:' |
  sed -E 's:/modules-[0-9]+:/modules-*:' |
  sed -E 's:/forms-[0-9]+:/forms-*:' |
  sed -E 's:/form_data/[a-z0-9-]+:/form_data/*:' |
  sed -E 's:/uuid\:[a-z0-9-]+:/uuid\:*:' |
  sed -E 's:/[-0-9a-f]{10,}:/*:g' |
  sed -E 's:/[0-9]+:/*:g' |
  sed 's:HTTP/1.[10] ::' |
  grep -v '^GET /static/' |
  grep -v '^quit' |
  grep -v '^G ' |
  sed 's:?[^ ]*::' |  # remove everything between '?' and ' '
  sed 's/\ /,/g' # replace spaces with commas, export to CSV for excel and make pivot table
