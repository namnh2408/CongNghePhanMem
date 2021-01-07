function addToCart(id, fullname, price) {
    fetch('/api/cart', {
        method: 'post',
        body: JSON.stringify({
            "id": id,
            "fullname": fullname,
            "price": price
        }),
        headers: {
            'Context-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        var cart = document.getElementById("cart-info");
        cart.innerText = `Cart-${data.total_quantity}`;
        console.info(data);
    }).catch(err => {
        console.log(err);
    });

    // promise --> await/async
}

function pay() {
    fetch('/api/pay', {
        method: 'post',
        headers: {
            'Context-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert(data.message);
        location.reload();
    }).catch(err => {
        location.href = '/payment';
    });
}