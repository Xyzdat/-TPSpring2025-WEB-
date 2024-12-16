select client_order.cost, client_order.delivery_date , bunchs.img_src ,bunchs.b_name, bunchorder.price from bunchorder
join bunchs using (b_id)
join client_order on client_order.o_id = bunchorder.order_id
where bunchorder.order_id = "$order_id" and client_order.client_id = "$user_id"