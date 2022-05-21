window.onload = function hello () {
    var _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    var quantity_arr = [];
    var price_arr = [];

    var total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());

    var order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    var order_total_price = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;

    for (var i = 0; i < total_forms; i++) {
        _quantity = parseInt($('input[name=orderitems-' + i + '-quantity').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));

        quantity_arr[i] = _quantity
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }

        $('.order_form').on('click', 'input[type=number]', function () {
            var target = event.target;

            orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
//            console.log(orderitem_num)
            if (price_arr[orderitem_num]) {
                orderitem_quantity = parseInt(target.value);
                delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
                quantity_arr[orderitem_num] = orderitem_quantity;
                orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
            }
        });

        $('.order_form').on('click', 'input[type=checkbox]', function () {

            var target = event.target;

            orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
            if (target.checked) {
                delta_quantity = -quantity_arr[orderitem_num];
            } else {
                delta_quantity = quantity_arr[orderitem_num];
            }
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        });

        function orderSummaryUpdate(orderitem_price, delta_quantity) {
            delta_cost = orderitem_price * delta_quantity;
            order_total_price = Number((order_total_price + delta_cost).toFixed(2));

            order_total_quantity = order_total_quantity + delta_quantity;

            $('.order_total_quantity').html(order_total_quantity.toString());
            $('.order_total_cost').html(order_total_price.toString());
        }
    }

    function deleteOrderItem(row) {
        var target_name = row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    }

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });

    $('.order_form select').change(function () {
        var target = event.target;
        var order_raw = target.parentNode.parentNode
        var orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
        var price_prev = price_arr[orderitem_num];
//        console.log(price_prev)
        var price_td = order_raw.querySelector(".td3")
        price_td.innerHTML = '';
        delta_quantity = parseInt(order_raw.querySelector("input[type=number]").value)
        order_raw.querySelector("input[type=number]").value = 0;
        var selected_item = $("option:selected", target);
        var selected_product_id = target.value;
//        console.log(selected_product_id);
        $.ajax({
            url: "/products/product/price/" + selected_product_id + "/",

            success: function (data) {
                var price_html = document.createElement("span")
                price_html.classList.add('orderitems-' + orderitem_num + '-product')
                price_html.textContent = data.result + " руб."
                price_td.appendChild(price_html)
                price_arr[orderitem_num] = data.result
                quantity_arr[orderitem_num] = 0
                if (delta_quantity){
                    orderSummaryUpdate(price_prev, (-delta_quantity))
                }

//                console.log(data.result)
//                $(price_td).html(data.result);
            },
        });

        event.preventDefault();
    })
}
