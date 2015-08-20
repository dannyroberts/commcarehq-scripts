BEGIN;
  -- create backup table with same schema
  create table stock_stocktransaction__deleted as
    select * from stock_stocktransaction
    where (id) in {rows};

  delete from stock_stocktransaction
  where (id) in {rows};
END;
