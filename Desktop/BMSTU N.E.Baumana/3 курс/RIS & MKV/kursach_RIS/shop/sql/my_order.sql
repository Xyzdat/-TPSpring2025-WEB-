select o_id ,client_order.cost, client_order.delivery_date from client_order

where client_order.client_id = "$user_id" 