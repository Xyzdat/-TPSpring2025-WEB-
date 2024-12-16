INSERT into client_order
(`o_date`,`cost`,`client_id`,`courier_id`,`delivery_date`,`delivery_adres`)
VALUES(NOW(),"$cost","$user_id",NULL, "$date", "$adres");