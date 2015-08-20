# Usage:
# bash pull-domain-admins.sh ${commcarehq-sessionid-cookie} < domain-list.txt > domain-admins.txt
sessionid=$1
while read line
do
  domain=$line
  bash pull-domain-admins.sh $domain $sessionid
done
