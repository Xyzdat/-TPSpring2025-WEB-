select o_id, o_date, cost , bunchorder.bo_id, couriers.courier_name, client.username from client_order
join couriers on couriers.courier_id = client_order.courier_id
JOIN bunchorder on bunchorder.order_id = client_order.o_id
join client on client.client_id = client_order.client_id
where couriers.courier_name = "$username"
