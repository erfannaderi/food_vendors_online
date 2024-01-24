let autocomplete;

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            //default in this app is "IN" - add your country code
            componentRestrictions: {'country': ['ir']},
        })
// function to specify what should happen when the prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry) {
        document.getElementById('id_address').placeholder = "Start typing...";
    } else {
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    geocoder.geocode({'address': address}, function (results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();
            console.log(results)

            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);
            $('#id_address').val(address);

        }
    })
    //loop through components for each component address
    for (var i = 0; i < place.address_components.length; i++) {
        for (var j = 0; j < place.address_components[i].types.length; j++) {
            // contry
            if (place.address_components[i].types[j] == 'country') {
                $('#id_country').val(place.address_components[i].long_name);
            }
            //state
            if (place.address_components[i].types[j] == 'administrative_area_level_1') {
                $('#id_state').val(place.address_components[i].long_name);
            }
            //city
            if (place.address_components[i].types[j] == 'locality') {
                $('#id_city').val(place.address_components[i].long_name);
            }
            //pin code
            if (place.address_components[i].types[j] == 'postal_code') {
                $('#id_pin_code').val(place.address_components[i].long_name);
            } else {
                $('#id_pin_code').val("");

            }
        }
    }
}


$(document).ready(function () {
    // add to cart
    $('.add-to-cart').on('click', function (e) {
        e.preventDefault();
        food_item_pk = $(this).attr('data-id');
        url = $(this).attr('data-url');

        // data={food_item_pk:food_item_pk}//data to store or send to django
        $.ajax({
            type: 'GET',
            url: url,
            // data:data,
            success: function (response) {
                console.log(response);
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function () {
                        window.location = '/login';
                    })
                }
                if (response.status == 'failed') {
                    swal(response.message, '', 'error');
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_counter']);
                    $('#qty-' + food_item_pk).html(response.qty);

                    // handle subtotal tax discount total
                    applyCartAmmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['discount'],
                        response.cart_amount['total'],
                    )
                }
            }
        });
    });
    //make the cart item quantity on a load
    $('.items_qty').each(function () {
        var the_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');
        $('#' + the_id).html(qty);
    });
    // decrease cart
    $('.decrease-cart').on('click', function (e) {
        e.preventDefault();
        food_item_pk = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_pk = $(this).attr('id')

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response);
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function () {
                        window.location = '/login';
                    })
                }
                if (response.status == 'failed') {
                    swal(response.message, '', 'error');
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_counter']);
                    $('#qty-' + food_item_pk).html(response.qty);
                    // handle subtotal tax discount total
                    applyCartAmmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['discount'],
                        response.cart_amount['total'],
                    )
                    if (window.location.pathname == '/cart/') {
                        removeCartItem(response.qty, cart_pk);
                        swal(response.message, '', 'success');
                        isEmpty();
                    }
                }
            }
        });
    });
    // delete
    $('.delete-cart').on('click', function (e) {
        e.preventDefault();
        var food_item_pk = $(this).attr('data-id');
        var url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response);
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function () {
                        window.location = '/login';
                    })
                }
                if (response.status == 'failed') {
                    swal(response.message, '', 'error');
                } else {
                    $('#qty-' + food_item_pk).html('0');
                    $('#cart_counter').html(response.cart_counter['cart_counter']);
                    swal(response.message, '', 'success');
                    // handle subtotal tax discount total
                    applyCartAmmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['discount'],
                        response.cart_amount['total'],
                    )
                    if (window.location.pathname == '/cart/') {
                        removeCartItem(0, food_item_pk)
                        isEmpty()
                    }
                }
            }
        });
    });

    // delete remove from cart
    function removeCartItem(cartItemQty, food_item_pk) {
        if (cartItemQty <= 0) {
            //removing item from cart
            document.getElementById('cart-item-' + food_item_pk).remove();

        }
    }

    // check if cart is empty
    function isEmpty() {
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if (cart_counter == 0) {
            document.getElementById('empty-cart').style.display = 'block';
        }
    }

    // apply cart ammounts
    function applyCartAmmounts(subtotal, tax, discount, total) {
        if (window.location.pathname == '/cart/') {
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#discount').html(discount)
            $('#total').html(total)
        }
    }
});
//
// function getCookie(name) {
//     const value = `; ${document.cookie}`;
//     const parts = value.split(`; ${name}=`);
//     if (parts.length === 2) return parts.pop().split(';').shift();
// }
//
// const csrfToken = getCookie('csrftoken');
// fetch(url, {
// method: 'GET',
// headers: {
// 'Content-Type': 'application/json',
// 'X-CSRFToken': csrfToken, // Include the CSRF token in the request headers
// },
// }).then(response => response.json())
// .then(data => {
// // Process the fetched data here
// console.log(data);}