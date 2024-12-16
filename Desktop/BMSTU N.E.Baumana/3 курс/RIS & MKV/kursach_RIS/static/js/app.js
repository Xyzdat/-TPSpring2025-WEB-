// document.addEventListener("DOMContentLoaded", function () {
//     const dateInput = document.querySelector('input[name="date"]'); // Найти поле даты
    
//     if (dateInput) {
//         const today = new Date();
//         today.setDate(today.getDate()); // Завтрашний день
        
//         // Преобразуем дату в формат YYYY-MM-DD
//         const minDate = today.toISOString().split('T')[0];
        
//         // Устанавливаем минимальную дату
//         dateInput.setAttribute('min', minDate);
//     }
// });

document.addEventListener("DOMContentLoaded", function () {
    const dateInput = document.getElementById('delivery-date');
    const today = new Date();
    today.setDate(today.getDate());
    today.setMinutes(today.getMinutes() - today.getTimezoneOffset()); // UTC fix
    const minDateTime = today.toISOString().slice(0, 16); // Format YYYY-MM-DDTHH:MM
    dateInput.setAttribute('min', minDateTime);

    dateInput.addEventListener('input', function () {
        const selectedDateTime = new Date(this.value);
        const selectedDate = selectedDateTime.toISOString().split('T')[0];
        const now = new Date();
        
        // Ограничения времени
        const minTime = "07:30";
        const maxTime = "23:00";

        if (selectedDate === now.toISOString().split('T')[0]) {
            // Если дата - сегодняшняя, устанавливаем минимальное время на сейчас
            let currentTime = now.getHours().toString().padStart(2, '0') + ":" + now.getMinutes().toString().padStart(2, '0');
            if (currentTime < minTime) currentTime = minTime; // Сравнение с 7:30
            this.min = `${selectedDate}T${currentTime}`;
        } else {
            // Если другая дата, устанавливаем фиксированные границы времени
            this.min = `${selectedDate}T${minTime}`;
            this.max = `${selectedDate}T${maxTime}`;
        }
    });
});



// const burger = document.querySelector('.burger');

// burger.addEventListener('click', () => {
//   burger.classList.toggle('active');
// });

// document.addEventListener("DOMContentLoaded", () => {
//     const burgerButton = document.getElementById("burgerButton");
//     burgerButton.addEventListener("click", () => {
//       burgerButton.classList.toggle("open");
//     });
//   });


document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn_decrease, .btn_increase').forEach(button => {
        button.addEventListener('click', (event) => {
            // Находим текущий элемент корзины
            const cartItem = event.target.closest('.cart_item');
            const itemId = cartItem.getAttribute('data-id');
            const quantityInput = cartItem.querySelector('.quantity_input');
            const currentQuantity = parseInt(quantityInput.value);

            const ButtonElement = event.target.closest('.btn_decrease, .btn_increase');
            if (!ButtonElement) return;

            // Проверяем, какая кнопка нажата
            const isIncrease = ButtonElement.classList.contains('btn_increase');
            const isDecrease = ButtonElement.classList.contains('btn_decrease');

            let newQuantity = currentQuantity;

            if (isIncrease) {
                newQuantity++;
            } else if (isDecrease && currentQuantity > 1) {
                newQuantity--;
            }

            // Обновляем количество в интерфейсе
            quantityInput.value = newQuantity;

            // Обновляем стоимость товара
            const itemCostElement = cartItem.querySelector('.item_cost');
            const costPerItem = parseFloat(itemCostElement.getAttribute('data-cost-per-item'));
            itemCostElement.textContent = `Цена: ${costPerItem * newQuantity} ₽`;

            // Обновляем количество на сервере
            updateCartOnServer(itemId, newQuantity);
            recalculateTotalSum();
        });
    });
});

// Функция для обновления количества на сервере
function updateCartOnServer(itemId, newQuantity) {
    fetch('/shop/update_cart_quantity', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item_id: itemId, quantity: newQuantity }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Server updated successfully:', data);
            } else {
                console.error('Server update failed:', data);
            }
        })
        .catch(error => console.error('Fetch error:', error));
}


function recalculateTotalSum(){
    let total = 0;

    document.querySelectorAll('.cart_item').forEach(item => {
        const quantity = parseInt(item.querySelector('.quantity_input').value, 10);
        const cost = parseFloat(item.querySelector('.item_cost').getAttribute('data-cost-per-item'));
        total += quantity * cost;
    });

    document.getElementById('total_sum').textContent = `Общая стоимость заказа: ${total} ₽`;
}




document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.del_from_cart').forEach(button => {
        button.addEventListener('click', (event) => {
            // Находим текущий элемент корзины
            const cartItem = event.target.closest('.cart_item');
            const itemId = cartItem.getAttribute('data-id');
            
            const ButtonEvent = event.target.closest('.del_from_cart');
            // Проверяем, какая кнопка нажата
            if(!ButtonEvent) return;
            const isIncrease = ButtonEvent.classList.contains('del_from_cart');

            if (isIncrease) {
                fetch('/shop/remove_from_cart', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ item_id: itemId }),
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            console.log('Server updated successfully:', data);
                            const cartItem = event.target.closest('.cart_item');
                            cartItem.remove();
                            recalculateTotalSum();
                           
                        } else {
                            console.error('Server update failed:', data);
                        }
                    })
                    .catch(error => console.error('Fetch error:', error));
            } 

        });
    });
});


document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.button_to_cart').forEach(button => {
        button.addEventListener('click', (event) => {
            // Находим текущий элемент корзины
            const cartItem = event.target.closest('.flower');
            const itemId = cartItem.getAttribute('flower-id');

            const ButtonEvent = event.target.closest('.button_to_cart');
            // Проверяем, какая кнопка нажата
            if(!ButtonEvent) return;
            // Проверяем, какая кнопка нажата
            const isIncrease = ButtonEvent.classList.contains('button_to_cart');

            if (isIncrease) {
                fetch('/shop/add_to_order_btn', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ item_id: itemId }),
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            const flowerElement = event.target.closest('.flower');
                            const flowerId = flowerElement.getAttribute('.flower-id');
                            console.log('Server updated successfully:', data);
                                // Заменить кнопку на сообщение
                            flowerElement.querySelector('.add_to_cart').innerHTML = '<h5 class="message_after_insert">✔ В корзине</h5>';
                        } else {
                            console.error('Server update failed:', data);
                        }
                    })
                    .catch(error => console.error('Fetch error:', error));
            } 

        });
    });
});

    



