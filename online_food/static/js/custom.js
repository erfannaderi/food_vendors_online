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

    //hours jquery
    $('.add_hours').on('click', function (e) {
        e.preventDefault();
        var day = $('#id_day').val();
        var from_hours = $('#id_from_hours').val();
        var to_hours = $('#id_to_hours').val();
        var is_closed = $('#id_is_closed').prop('checked');
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        var url = $('#add_hour_url').val();
        console.log(day, from_hours, to_hours, is_closed, csrf);
        if (is_closed) {
            is_closed = 'True';
            condition = "day != ''";
        } else {
            is_closed = 'False';
            condition = "day != '' && from_hours != '' && to_hours != ''";
        }
        if (eval(condition)) {
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'day': day,
                    'from_hours': from_hours,
                    'to_hours': to_hours,
                    'is_closed': is_closed,
                    'csrfmiddlewaretoken': csrf,
                },
                success: function (response) {
                    if (response.status == 'success') {
                        if (response.is_closed == 'Closed') {
                            html = '<tr id="hour-' + response.pk + '"><td><b>' + response.day + '</b></td><td>Closed</td><td><a href="#" class="btn btn-danger remove_hours" data-url="/restaurant/opening-hours/remove/' + response.pk + '/">remove</a></td></tr>';
                            $(".opening_hours").append(html);
                            document.getElementById("open_hours").reset();
                        } else {
                            html = '<tr id="hour-' + response.pk + '"><td><b>' + response.day + '</b></td><td>' + response.from_hours + ' - ' + response.to_hours + '</td><td><a href="#" class="btn btn-danger remove_hours" data-url=" /restaurant/opening-hours/remove/' + response.pk + '/">remove</a></td></tr>';
                            $(".opening_hours").append(html);
                            document.getElementById("open_hours").reset();
                        }
                    } else {
                        swal(response.message, '', 'error')
                    }
                    console.log(response);
                },
                error: function (xhr, status, error) {
                    swal('Error', 'An error occurred while adding opening hours', 'error');
                }
            });
        } else {
            swal('Please fill all fields', '', 'error');
        }
    });
    // Removing opening hours (using event delegation)
    $(document).on('click', '.remove_hours', function (e) {
        e.preventDefault();
        var url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                if (response.status === 'success') {
                    $('#hour-' + response.pk).remove();
                }
            }
        });
    });
    //removing
    $('.remove_hours').on('click', function (e) {
        e.preventDefault();
        url = $(this).attr('data-url');
        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                if (response.status === 'success') {
                    document.getElementById('hour-' + response.pk).remove()
                }
            }
        })
    })
    //address jquery
    $('.add_address').on('click', function (e) {
        e.preventDefault();
        var address = $('#id_address').val();
        var country = $('#id_country').val();
        var state = $('#id_state').val();
        var city = $('#id_city').val();
        var pin_code = $('#id_pin_code').val();
        var latitude = $('#id_latitude').val();
        var longitude = $('#id_longitude').val();
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        var url = $('#add_address_url').val();
        console.log(address, country, state, city, pin_code, latitude, longitude, csrf);
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'address': address,
                'country': country,
                'state': state,
                'city': city,
                'pin_code': pin_code,
                'latitude': latitude,
                'longitude': longitude,
                'csrfmiddlewaretoken': csrf,
            },
            success: function (response) {
                // Handle the success response
                if (response.status === 'success') {
                    // Append the new address row to the table
                    var newRow = '<tr id="address-' + response.pk + '">' +
                        '<td><b>' + response.address + '</b></td>' +
                        '<td>' + response.country + '</td>' +
                        '<td>' + response.state + '</td>' +
                        '<td>' + response.city + '</td>' +
                        '<td>' + response.longitude + '</td>' +
                        '<td>' + response.latitude + '</td>' +
                        '<td><a href="#" class="btn btn-danger remove_address" ' +
                        'data-url="' + response.remove_url + '">remove</a></td>' +
                        '</tr>';
                    $('.new_address tbody').append(newRow);

                    // Clear the form fields
                    $('#new_address')[0].reset();
                } else {
                    // Handle the error response
                    console.error(response.message);
                }
                console.log(response);
            },
            error: function (xhr, status, error) {
                swal('Error', 'An error occurred while adding opening hours', 'error');
            }
        });
    });
    // delete address
    $(document).on('click', '.remove_address', function (e) {
        e.preventDefault();
        var url = $(this).attr('data-url');
        var $addressElement = $(this).closest('.address-row'); // Assuming the address element has a parent element with class 'address-row'

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                if (response.status === 'success') {
                    $addressElement.remove(); // Remove the address element from the DOM
                }
            }
        });
    });
    //add popup to address
    $(document).ready(function () {
        // Limit the display of the limited-content elements
        $('.limited-content').each(function () {
            var content = $(this).data('content');
            var limit = 50; // Define the limit of characters to display

            if (content.length > limit) {
                var limitedText = content.substring(0, limit) + '...';
                $(this).text(limitedText);
            }
        });

        // Show the pop-up when the Read More button is clicked
        $('.show-popup').on('click', function () {
            var content = $(this).prev('.limited-content').data('content');
            $('.popup-content').text(content);
            // Display the pop-up
            // You can use a modal or any other method to show the pop-up
            $('.popup-content').show();
        });
    });
    //closeing jquery
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