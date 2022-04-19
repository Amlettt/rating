$(document).ready(function() {
    $('input[name="tab_btn"]').click(function(){
        var target = $('#page-' + $(this).val());
        var target2 = $('#title-' + $(this).val());
    
        $('.page').not(target).hide(0);
        target.fadeIn(500);
        $('.title').not(target2).hide(0);
        target2.fadeIn(500);
    });

    //открытие меню с протоколами
    $('.header__menu-burger').click(function() {
        $('.header__menu-burger').toggleClass('open-menu');
        $('.widget').toggleClass('open-menu');
        $('.page').toggleClass("disable-hover"); // убираем для всей формы активность чтобы на нажатия не реагировало когда всплыл ответ от бд
        $('.switch').toggleClass("disable-hover"); // убираем для всей формы активность чтобы на нажатия не реагировало когда всплыл ответ от бд
        // $('body').toggleClass('fixed-page');
    });
});