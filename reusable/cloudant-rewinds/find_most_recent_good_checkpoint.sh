# Usage:
# bash find_most_recent_good_checkpoint.sh 55000000 https://commcarehq.cloudant.com/commcarehq < pillow_checkpoint_ids | tee checkpoints_to_use.txt
# where pillow_checkpoint_ids looks like
#
# $ cat pillow_checkpoint_ids
# pillowtop_mvp_docs.pillows.MVPCaseIndicatorPillow.hqdb0
# pillowtop_corehq.pillows.log.PhoneLogPillow.hqdb0
# pillowtop_corehq.pillows.sofabed.CaseDataPillow.hqdb0
# pillowtop_corehq.pillows.reportcase.ReportCasePillow.8c10a7564b6af5052f8b86693bf6ac07.hqdb0
# pillowtop_corehq.pillows.application.AppPillow.fe975a5128b655ba175ac81b035498d0.hqdb0

MIN_SEQ_INT=$1
DB_URL=$2

while read line
do
  doc_id=$line
  doc_url=$DB_URL/$doc_id
  echo $doc_id
  bash get_revs_for_doc.sh $doc_url | python scan_revs.py $MIN_SEQ_INT $doc_url
done
