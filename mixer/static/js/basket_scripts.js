window.onload = function () {
    console.log('DOM loaded');
    // let basketList = document.querySelector('.basket_list');
    // basketList.onchange = function () {};
    $('.basket_list').on('change', 'input[type=number]', function (event) {
        console.log(event.target);
        $.ajax({
            url: '/basket/change/' + event.target.name + '/quantity/' + event.target.value + '/',
            success: function (data) {
                console.log(data)
                $('.basket_list').html(data.result);
            }
        });

    })
};
// body > div > div.basket_list > div:nth-child(3) > input[type=number]