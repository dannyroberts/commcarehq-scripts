domain=$1
sessionid=$2
echo $domain $(
  curl -b "sessionid=$sessionid" https://www.commcarehq.org/a/$domain/api/v0.5/web-user/ |
    jsawk "return this.objects" |
    jsawk '
      if (this.is_admin) {
        if (this.first_name || this.last_name) {
          return this.first_name + " " + this.last_name + " <" + (this.email || this.username) + ">";
        } else {
          return this.email || this.username;
        }
      } else {
        return;
      }
    '
)
