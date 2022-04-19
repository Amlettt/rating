$(document).ready(function() {

    var jsonData = {};
    var tab; // заголовок вкладки
    var tableContent; // блок содержащий контент вкладки
    var group = 0; // открытая сейчас группа спортсменов в браузере

    tableContent = $('.table-content');
    tab = $('.tab');

    bdLoad();
    hideTabsContent(1); //скрыть при загрузке все таблицы кроме первой(0)
 
    // переключаем вкладки таблиц
    $('.tab').on("click", function(event) {
        for (var i = 0; i < tab.length; i++) {
            if ($(this)[0] == tab[i]) {
                showTabsContent(i);
                break;
            }
        }
    });

    // загрузка рейтинга спортсменов
    function bdLoad(){
        $.ajax({
        type: "POST",
        url: "load_db.php",
        // dataType: "json",
        data: {
            a: 'a', 
            b: 'b',
            c: 'c'
        },
        success: function(response){
            jsonData = JSON.parse(response);  // раскодируем json данные
            jsonData = sort_vichet(jsonData);  // сортируем спортсменов по очкам с вычетом
            showSportsmen(0, 'a_elite');
        }
        });
    }
    

    // скрыть все таблицы начиная с a
    function hideTabsContent(a) {
        for (var i = a; i < tableContent.length; i++) {
            $(tableContent[i]).removeClass('show');
            $(tableContent[i]).addClass('hide');
            $(tab[i]).removeClass('whiteborder');
        }
    }

    // показать таблицу под номером b
    function showTabsContent(b){
        if ( $(tableContent[b]).hasClass('hide')) {
            hideTabsContent(0);
            $(tab[b]).addClass('whiteborder');
            $(tableContent[b]).removeClass('hide');
            $(tableContent[b]).addClass('show');

            let cls = '';
            if (b == 0){cls = 'a_elite';}
            else if (b == 1){cls = 'b_adult';}
            else if (b == 2){cls = 'b_veteran';}
            else if (b == 3){cls = 'b_teenager';}
            else if (b == 4){cls = 'c_kid';}

            showSportsmen(b, cls); 
        }
    }

    //показать спортсменов во вкладке b
    function showSportsmen(b, cls){

        group = cls;
        $('.group-'+ cls).find('tbody tr').remove(); // чистим поля чтоб не накладывались друг на друга

        let j = 1;
        $.each(jsonData[b], function(index, value){
            if($('.checkbox-ya input[type=checkbox]').prop('checked')){
                if(value[2] == "Ж"){
                    // подсвечиваем 3 лучших места
                    // if(j < 4){
                    //     $('.group-'+ cls).find('tbody').append('<tr class="champions"></tr>');
                    // }
                    // else {
                    //     $('.group-'+ cls).find('tbody').append('<tr></tr>');
                    // }
                    $('.group-'+ cls).find('tbody').append('<tr></tr>');
                    $('.group-'+ cls).find('tr:last').append('<td class="td">'+ (j) +'</td>');
                    $('.group-'+ cls).find('tr:last').append('<td class="td fio" style="text-align: left; padding-left: 20px;">'+ value[0] + '</td>');
                    $('.group-'+ cls).find('tr:last').append('<td class="td"><button class="btn stat-btn" id="statistic" title="Статистика спортсмена">+</button></td>'); 
                    $('.group-'+ cls).find('tr:last').append('<td class="td years">'+ value[1] +'</td>');
                    $('.group-'+ cls).find('tr:last').append('<td class="td">'+ value[3] +'</td>');
                    $('.group-'+ cls).find('tr:last').append('<td class="td">'+ value[4] +'</td>');
                    $('.group-'+ cls).find('tr:last').append('<td class="td points_vichet">'+ parseFloat(value[6], 10) +'</td>');
                    // $('.group-'+ cls).find('tr:last').append('<td class="td td-img-change-place" title="Изменние позиции в рейтинге">'+ placeChange(value[5]) +'</td>'); // стрелки изменнения в рейтинге, верх вниз
                    if(b == 4){
                        if(j == 2){
                        $('.group-'+ cls).find('tr:last').append('<td ><img class="img_place" src="img/cup1.png" height="50px" width="33px"></td>');
                        }
                        else if(j == 3) {
                            $('.group-'+ cls).find('tr:last').append('<td ><img class="img_place" src="img/cup2.png" height="50px" width="33px"></td>');
                        }
                        else if(j == 4) {
                            $('.group-'+ cls).find('tr:last').append('<td ><img class="img_place" src="img/cup3.png" height="50px" width="33px"></td>');   
                        }
                    }
                    else {
                        if(j == 1){
                        $('.group-'+ cls).find('tr:last').append('<td ><img class="img_place" src="img/cup1.png" height="50px" width="33px"></td>');
                        }
                        else if(j == 2) {
                            $('.group-'+ cls).find('tr:last').append('<td ><img class="img_place" src="img/cup2.png" height="50px" width="33px"></td>');
                        }
                        else if(j == 3) {
                            $('.group-'+ cls).find('tr:last').append('<td ><img class="img_place" src="img/cup3.png" height="50px" width="33px"></td>');   
                        }
                    }
           
                    j++; 
                }                    
            }
            else {
                if(value[2] == "М"){
                    // подсвечиваем 3 лучших места
                    // if(j < 4){
                    //     $('.group-'+ cls).find('tbody').append('<tr class="champions"></tr>');
                    // }
                    // else {
                    //     $('.group-'+ cls).find('tbody').append('<tr></tr>');
                    // }
                    $('.group-'+ cls).find('tbody').append('<tr></tr>');
                    $('.group-'+ cls).find('tr:last').append('<td class="td">'+ (j) +'</td>');
                    $('.group-'+ cls).find('tr:last').append('<td class="td fio" style="text-align: left; padding-left: 20px;">'+ value[0] +'</td>');
                    $('.group-'+ cls).find('tr:last').append('<td class="td"><button class="btn stat-btn" id="statistic" title="Статистика спортсмена">+</button></td>'); 
                    $('.group-'+ cls).find('tr:last').append('<td class="td years">'+ value[1] +'</td>');
                    $('.group-'+ cls).find('tr:last').append('<td class="td">'+ value[3] +'</td>');
                    $('.group-'+ cls).find('tr:last').append('<td class="td">'+ value[4] +'</td>');
                    $('.group-'+ cls).find('tr:last').append('<td class="td points_vichet">'+ parseFloat(value[6], 10) +'</td>');
                    // $('.group-'+ cls).find('tr:last').append('<td class="td td-img-change-place" title="Изменние позиции в рейтинге">'+ placeChange(value[5]) +'</td>'); // стрелки изменнения в рейтинге, верх вниз
                    if(j == 1){
                        $('.group-'+ cls).find('tr:last').append('<td ><img class="img_place" src="img/cup1.png" height="50px" width="33px"></td>');
                    }
                    else if(j == 2) {
                        $('.group-'+ cls).find('tr:last').append('<td ><img class="img_place" src="img/cup2.png" height="50px" width="33px"></td>');
                    }
                    else if(j == 3) {
                        $('.group-'+ cls).find('tr:last').append('<td ><img class="img_place" src="img/cup3.png" height="50px" width="33px"></td>');   
                    }

                    j++; 
                }
            }
        });
    }

    //показать изменение в рейтинге треугольничками - зеленый вверх, красный вниз
    function placeChange(a) {
        if(a < 0){
            // '<img class="td-img_place" src="img/down_place.png" height="22px" width="44px">'
            return '<i class="placechange-down"></i><span class="span-placechange-down">' + a*(-1) + '</span>';
        }
        else if(a == 0){   
            return '<i class="placechange-up"></i><span class="span-placechange-up">' + a + '</span>';
        }
        else if(a > 0){   
            // '<img class="img_place" src="img/up_place.png" height="22px" width="44px">' + 
            return '<i class="placechange-up"></i><span class="span-placechange-up">' + a + '</span>';
        }

    }

    //показ участников. смена пола в рейтинге при клике
    $('.checkbox-ya input[type=checkbox]').on('click', function(){
        for (let i = 0; i < tab.length; i++) {
            // console.log($('.tab').index($('.whiteborder')));
            if ($('.tab').index($('.whiteborder')) == i) {
                
                let cls = '';
                if (i == 0){cls = 'a_elite';}
                else if (i == 1){cls = 'b_adult';}
                else if (i == 2){cls = 'b_veteran';}
                else if (i == 3){cls = 'b_teenager';}
                else if (i == 4){cls = 'c_kid';}

                showSportsmen(i, cls);
                break;
            }
        }
    });

    // показать статистику по участнику
    $(document).on('click', '.stat-btn', function(){
        var fio = $(this).parent().parent().find('.fio').text();
        var years = $(this).parent().parent().find('.years').text();
        // var sex = $(this).parent().parent().find('.sex').text();

        $('main').addClass("disable-hover"); // убираем для всей формы активность чтобы на нажатия не реагировало когда всплыл ответ от бд
        $('.window-block').addClass('zindex');
        $('.statistics-sportsmen').addClass('visible');
        // $('.statistics-sportsmen__title').html(fio);

        $.ajax({
            type: "POST",
            url: "load_db.php",
            // dataType: "json",
            data: {
               f: fio, 
               y: years,
               group: group
            //    ,sex: sex   
            },
            success: function(response){
                var jsonData = JSON.parse(response);  // раскодируем json данные
                $('.statistics-sportsmen__info div:first').html(fio);
                $('.statistics-sportsmen__info div:last').html(years + " г.р.");
                $('.countstart').html(jsonData.countstart + ' (' + jsonData.countstartfinished + ' успешных)');
                
                if (parseInt(jsonData.timestart[0], 10) / 60 > 1 ){  // если время больше часа. для отображения часов минут секунд
                    let hour = Math.floor(parseInt(jsonData.timestart[0], 10) / 60);
                    let minute = parseInt(jsonData.timestart[0], 10) % 60;
                    if (minute.toString().length == 1){
                        if (jsonData.timestart[1].toString().length == 1){
                            $('.timestart').html(hour + ":0"+ minute + ":0" + jsonData.timestart[1] );
                        }
                        else {
                            $('.timestart').html(hour + ":0"+ minute + ":" + jsonData.timestart[1] );
                        }
                    }
                    else{
                        if (jsonData.timestart[1].toString().length == 1){
                            $('.timestart').html(hour+ ":"+ minute + ":0" + jsonData.timestart[1] );
                        }
                        else {
                            $('.timestart').html(hour+ ":"+ minute + ":" + jsonData.timestart[1] );
                        }
                    }
                   
                }
                else {
                    if (jsonData.timestart[1].toString().length == 1){
                        $('.timestart').html(jsonData.timestart[0] + ":0" + jsonData.timestart[1] );
                    }
                    else {
                        $('.timestart').html(jsonData.timestart[0] + ":" + jsonData.timestart[1] );
                    }
                }
                
                $('.lengthstart').html(jsonData.lengthstart + " м");


                // средняя скорость
                // if (!!!jsonData.place_avg_speedgroup){  // проверка на значение undefined, если у спортсмена нет средней скорости запрос выдает undefined
                //     h = jsonData.countgroup; // смотрим  какое место в групее. последнее если пишем что последнее
                // }
                // else {
                //     h = jsonData.place_avg_speedgroup
                // }
                if (jsonData.avgspeedstart[0] == 0 && jsonData.avgspeedstart[1] == 0){
                    $('.avgspeedstart').html("Увы, еще нет стартов c взятием КП");
                }
                else if (jsonData.avgspeedstart[1].toString().length == 1){
                    $('.avgspeedstart').html(jsonData.avgspeedstart[0] + ":0" + jsonData.avgspeedstart[1] + " м/км (" 
                    + jsonData.place_avg_speedall + " среди всех/ " + jsonData.place_avg_speed_sex[0] + " " + jsonData.place_avg_speed_sex[1] + "/ "+ jsonData.place_avg_speedgroup + " в группе)");
                }
                else {
                $('.avgspeedstart').html(jsonData.avgspeedstart[0] + ":" + jsonData.avgspeedstart[1] + " м/км (" 
                + jsonData.place_avg_speedall + " среди всех/ " + jsonData.place_avg_speed_sex[0] + " " + jsonData.place_avg_speed_sex[1] + "/ "+ jsonData.place_avg_speedgroup + " в группе)");
                }
                // лучшая скорость
                if (jsonData.bestspeed[1] < 0){
                    $('.bestspeed').html("-");
                }
                // else if (jsonData.bestspeed[1].toString().length == 1){
                //     $('.bestspeed').html(jsonData.bestspeed[0] + ":0" + jsonData.bestspeed[1] + " м/км (" 
                //     + jsonData.place_best_speedall + " среди всех/ " + jsonData.place_best_speedgroup + " в группе)");
                // }
                // else {
                // $('.bestspeed').html(jsonData.bestspeed[0] + ":" + jsonData.bestspeed[1] + " м/км (" 
                // + jsonData.place_best_speedall + " среди всех/ " + jsonData.place_best_speedgroup + " в группе)");
                // }
                else if (jsonData.bestspeed[1].toString().length == 1){
                    $('.bestspeed').html(jsonData.bestspeed[0] + ":0" + jsonData.bestspeed[1] + " м/км (" 
                    + jsonData.place_best_speedall + " среди всех/ " + jsonData.place_best_speed_sex[0] + " " + jsonData.place_best_speed_sex[1] + "/ "+ jsonData.place_best_speedgroup + " в группе)");
                }
                else {
                $('.bestspeed').html(jsonData.bestspeed[0] + ":" + jsonData.bestspeed[1] + " м/км (" 
                + jsonData.place_best_speedall + " среди всех/ " + jsonData.place_best_speed_sex[0] + " " + jsonData.place_best_speed_sex[1] + "/ "+ jsonData.place_best_speedgroup + " в группе)");
                }
                // Худшая скорость
                if (jsonData.badspeed[1] < 0){
                    $('.badspeed').html("-");
                }
                else if (jsonData.badspeed[1].toString().length == 1){
                    $('.badspeed').html(jsonData.badspeed[0] + ":0" + jsonData.badspeed[1] + " м/км");
                }
                else {
                $('.badspeed').html(jsonData.badspeed[0] + ":" + jsonData.badspeed[1] + " м/км");
                }

            }
          });

    });

    // закрыть и очистить форму статистику по участнику
    $('#exit').on('click', function(){
        // $('.statistics-sportsmen__title').html('');
        $('.statistics-sportsmen').removeClass('visible');
        $('.window-block').removeClass('zindex');
        $('main').removeClass("disable-hover");

        // чистим статистику спортсмена чтоб логания перезаписывания при открытии следующего не было
        $('.countstart').html('');
        $('.timestart').html('');
        $('.lengthstart').html('');
        $('.avgspeedstart').html('');
        $('.bestspeed').html('');
        $('.badspeed').html('');
    });

    // сортировка участников по очкам с вычетом
    function sort_vichet(sportsmen){
        for(let k = 0; k < sportsmen.length; k++){
            for(let i = 0; i < sportsmen[k].length; i++) {
                for(let j = 0; j < sportsmen[k].length-1; j++) {
                    if(parseFloat(sportsmen[k][j][6],10) < parseFloat(sportsmen[k][j+1][6],10)){
                        var mass = sportsmen[k][j];
                        sportsmen[k][j] = sportsmen[k][j+1];
                        sportsmen[k][j+1] = mass;
                    }
                } 
            }
        }      
        return sportsmen;
    }

});