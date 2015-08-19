select domain, case_id, product_id, section_id, date, form_id
from stock_stockreport as rpt, stock_stocktransaction as txn
where domain = 'moko' and rpt.id = txn.report_id
order by domain, case_id, product_id, section_id, date, form_id;
