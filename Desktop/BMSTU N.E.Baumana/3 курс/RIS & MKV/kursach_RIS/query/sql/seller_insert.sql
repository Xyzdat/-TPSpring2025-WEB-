UPDATE `flower_delivery`.`client_order`
SET courier_id = "$courier_id"
WHERE o_id = "$o_id";