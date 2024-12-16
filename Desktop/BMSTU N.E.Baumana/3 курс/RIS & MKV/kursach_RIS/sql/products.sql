select o_id, o_date, bo_id, couriers.courier_name, client.name from client_order
join couriers on couriers.courier_id = client_order.courier_id
join client on client.client_id = client_order.client_id
where couriers.courier_name = "$courier_name"
