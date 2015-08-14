# Usage:
# bash get_revs_for_doc.sh https://commcarehq.cloudant.com/commcarehq/pillowtop_corehq.pillows.sofabed.CaseDataPillow.hqdb0

function cache_curl() {
  url=$1
  cachefile=$(echo $url | md5).cache
  if [ -f $cachefile ]
  then
    cat $cachefile
  else
    curl $url | tee $cachefile
  fi
}

doc_url=$1
cache_curl $doc_url?revs_info=true | jsawk '
  for (var i = 0; i < this._revs_info.length; i++) {
    var revs_info = this._revs_info[i];
    if (revs_info.status === "available") {
      out(revs_info.rev);
    }
  };
  return
'
