// переписать все ошибки в один блок. Менять только текст. а не как сейчас на каждую ошибку свой блок
$(document).ready(function(){
    run ();

    $("#connect_to_bd").on("click", function(){
        //действия
        conn_db();
    });

    $("#send_to_bd").on("click", function(){
        //действия
        parse();
    });
 });

// стартовая функция, чтение файла settings.ini  с настройками подключения
async function run() {
    let arr = new Array();
    arr = await eel.crudConfig()();
    $('.bd_host').val(arr[0]);
    $(".bd_login").val(arr[1]);
    $(".bd_password").val(arr[2]);
    $(".bd_name").val(arr[3]);
}
// подключение к БД
async function conn_db() {
    let connect;
    let host, login, password,name;
    host =  $('.bd_host').val();
    login = $(".bd_login").val();
    password = $(".bd_password").val();
    name = $(".bd_name").val();
    connect = await eel.connect_db(host, login, password, name)();
    if (connect === true) {
        $('.form__bd-accept').toggleClass('visible'); // добавляем класс индикация успеха подключения с дисплей блок
        $('.form_parsing').toggleClass('visible'); // добавляем класс блока выбора файлов с дисплей блок
        $('.line-block').toggleClass('visible'); // добавляем класс просто линия с дисплей блок
        $('#connect_to_bd').toggleClass('no-visible'); // добавляем класс убираем кнопку подключиться с дисплей none
        $('.form__bd').toggleClass('no-visible'); // добавляем класс убираем данные подключения с дисплей none
        if($('.form__bd-no-entry').hasClass("visible")) {
             $('.form__bd-no-entry').removeClass('visible'); // убираем класс индикация не удачного подключение с дисплей none
        }
    }
    else {
        if(!$('.form__bd-no-entry').hasClass("visible")) {
             $('.form__bd-no-entry').addClass('visible'); // добавляем класс индикация не удачного подключение с дисплей none
        }
    }
}
// Отправка файла для парсинга
async function parse() {
    let address, parsing_yes;

    if (!$(".input__file").val() == "") {
        address = $('.input__file').val().split("\\"); // делим по двум чертам
        parsing_yes = await eel.read_doc(address[2])(); // адрес 2 потому что путь разделенн на 3 части. нам нужна 3я
        $(".input__file").val(""); // сбросить выбранный файл
        $('.input__file-button-text').text('Выберите файл');

        if ($('.form__file-no').hasClass("visible")) {
            $('.form__file-no').removeClass('visible'); // удаляем класс индикация когда файл не выбран с дисплей block
        }
        if (parsing_yes === 1) {
            $('.form__parse-yes').addClass('visible')  // добавляем класс индикация удачного чтения файла с дисплей block
            if ($('.form__parse-no').hasClass("visible")) {
                $('.form__parse-no').removeClass('visible'); // удаляем класс индикация не удачного чтения файла с дисплей none
            }
            if ($('.form__parse-was').hasClass("visible")) {
                $('.form__parse-was').removeClass('visible'); // удаляем класс индикация ошибки ранее загруженного файла с дисплей none
                }
        }
        else if (parsing_yes === 3) {
            $('.form__parse-was').addClass('visible')  // добавляем класс индикация ошибки ранее загруженного файла с дисплей block
            if ($('.form__parse-yes').hasClass("visible")) {
                $('.form__parse-yes').removeClass('visible'); // удаляем класс индикация не удачного чтения файла с дисплей none
            }
            if ($('.form__parse-no').hasClass("visible")) {
                $('.form__parse-no').removeClass('visible'); // удаляем класс индикация не удачного чтения файла с дисплей none
                }
        }
        else if (parsing_yes === 2) {
            $('.form__parse-no').addClass('visible'); // добавляем класс индикация не удачного чтения файла с дисплей block
            $('.form__parse-no h4').html("Ошибка названия дистанций");
            if ($('.form__parse-yes').hasClass("visible")) {
                $('.form__parse-yes').removeClass('visible'); // удаляем класс индикация удачного чтения файла с дисплей none
            }
            if ($('.form__parse-was').hasClass("visible")) {
                $('.form__parse-was').removeClass('visible'); // удаляем класс индикация ошибки ранее загруженного файла с дисплей none
            }
        }
        else if (parsing_yes === 4) {
            $('.form__parse-no').addClass('visible'); // добавляем класс индикация не удачного чтения файла с дисплей block
            $('.form__parse-no h4').html("Найдено сокращенное имя");
            if ($('.form__parse-yes').hasClass("visible")) {
                $('.form__parse-yes').removeClass('visible'); // удаляем класс индикация удачного чтения файла с дисплей none
            }
            if ($('.form__parse-was').hasClass("visible")) {
                $('.form__parse-was').removeClass('visible'); // удаляем класс индикация ошибки ранее загруженного файла с дисплей none
            }
        }
        else if (parsing_yes === 5) {
            $('.form__parse-no').addClass('visible'); // добавляем класс индикация не удачного чтения файла с дисплей block
            $('.form__parse-no h4').html("Неправильное название группы");
            if ($('.form__parse-yes').hasClass("visible")) {
                $('.form__parse-yes').removeClass('visible'); // удаляем класс индикация удачного чтения файла с дисплей none
            }
            if ($('.form__parse-was').hasClass("visible")) {
                $('.form__parse-was').removeClass('visible'); // удаляем класс индикация ошибки ранее загруженного файла с дисплей none
            }
        }

        else {
            $('.form__parse-no').addClass('visible'); // добавляем класс индикация не удачного чтения файла с дисплей block
             $('.form__parse-no h4').html("Ошибка чтения файла");
            if ($('.form__parse-yes').hasClass("visible")) {
                $('.form__parse-yes').removeClass('visible'); // удаляем класс индикация удачного чтения файла с дисплей none
            }
            if ($('.form__parse-was').hasClass("visible")) {
                $('.form__parse-was').removeClass('visible'); // удаляем класс индикация ошибки ранее загруженного файла с дисплей none
            }
        }
    }
    else {
        if (!$('.form__file-no').hasClass("visible")) {
            $('.form__file-no').addClass('visible'); // добавляем класс индикация когда файл не выбран с дисплей block
        }
        if ($('.form__parse-no').hasClass("visible")) {
            $('.form__parse-no').removeClass('visible'); // удаляем класс индикация не удачного чтения файла с дисплей none
        }
        if ($('.form__parse-yes').hasClass("visible")) {
            $('.form__parse-yes').removeClass('visible'); // удаляем класс индикация удачного чтения файла с дисплей none
        }
        if ($('.form__parse-was').hasClass("visible")) {
            $('.form__parse-was').removeClass('visible'); // удаляем класс индикация удачного чтения файла с дисплей none
        }
    }

}

// визуализация количества выбранных файлов
let inputs = document.querySelectorAll('.input__file');
Array.prototype.forEach.call(inputs, function (input) {
  let label = input.nextElementSibling;
  let labelVal = label.querySelector('.input__file-button-text').innerText;

  input.addEventListener('change', function (e) {
     $('.form__parse-no').removeClass('visible');
     $('.form__parse-was').removeClass('visible');
     $('.form__parse-yes').removeClass('visible');
     $('.form__file-no').removeClass('visible');
    let countFiles = '';
    if (this.files && this.files.length >= 1)
      countFiles = this.files.length;

    if (countFiles)
      label.querySelector('.input__file-button-text').innerText = 'Выбрано файлов: ' + countFiles;
    else
      label.querySelector('.input__file-button-text').innerText = labelVal;
  });
});




