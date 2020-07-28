window.onload = function () {
    console.log('DOM loaded');
    // let basketList = document.querySelector('.basket_list');
    // basketList.onchange = function () {};
    $('.users_list').on('click', '.btn-danger', function (event) {
        console.log(event.target);
    })
};

// body > div > div.users_list > div:nth-child(2) > div.col-lg-2.user_role > a.btn.btn-danger