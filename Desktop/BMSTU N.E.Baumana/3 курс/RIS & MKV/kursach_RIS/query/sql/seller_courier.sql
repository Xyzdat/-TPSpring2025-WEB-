select couriers.courier_name from couriers
join client_order on couriers.courier_id = client_order.courier_id
WHERE client_order.o_date = "$date"