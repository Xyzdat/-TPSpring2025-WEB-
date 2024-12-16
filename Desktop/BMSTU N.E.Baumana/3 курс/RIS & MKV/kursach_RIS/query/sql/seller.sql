select o_id, o_date, cost, client_id, couriers.courier_name, delivery_date, delivery_adres from client_order
LEFT join couriers on couriers.courier_id = client_order.courier_id
WHERE o_date = "$date"