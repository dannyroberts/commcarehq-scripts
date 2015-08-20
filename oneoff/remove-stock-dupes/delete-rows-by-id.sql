BEGIN;
  -- create backup table with same schema
  create table stock_stocktransaction__deleted as
  select * from stock_stocktransaction
  where (report_id) in {rows};

  create table stock_stockreport__deleted as
  select * from stock_stockreport
  where (id) in {rows};

  delete from stock_stocktransaction
  where (report_id) in {rows};

  delete from stock_stockreport
  where (id) in {rows};
END;
