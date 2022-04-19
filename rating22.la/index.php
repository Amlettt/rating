<!DOCTYPE html>
<html lang="ru">
    <head>
        <meta charset="UTF-8">
        <!-- Отключение кэширования страницы -->
        <meta http-equiv="Cache-Control" content="no-cache"> 
        <!-- <meta name="viewport" content="width=device-width, initial-scale=1.0"> -->
        <!-- <meta name="viewport" content="user-scalable=no"> -->
        <title>Рейтинг кубка "O-party" по спортивному ориентированию</title>
        <!-- <link rel="stylesheet" href="css/style.css?t=<?php echo(microtime(true).rand()); ?>" type="text/css"> -->
        <link rel="stylesheet" href="css/style.css" type="text/css">
        <link rel="icon" href="img/icon.png" type="image/png">
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script src = "code-highcharts/highcharts.js"></script>
        <script src="code-highcharts/modules/series-label.js"></script>
        <script src="code-highcharts/modules/exporting.js"></script>
        <script src="code-highcharts/modules/export-data.js"></script>
        <script src="code-highcharts/modules/accessibility.js"></script>
        <script src="code-highcharts/modules/wordcloud.js"></script>
        <script src="code-highcharts/themes/dark-unica.js"></script>
        <script src="https://kit.fontawesome.com/3cd7afbb17.js" crossorigin="anonymous"></script>
        <!-- <script type="text/javascript" src="https://canvasjs.com/assets/script/jquery-1.11.1.min.js"></script> -->
        <!-- <script type="text/javascript" src="js/jquery.canvasjs.min.js"></script> -->
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript" src="js/main.js"></script>
        <script type="text/javascript" src="js/rating.js"></script>
        <script type="text/javascript" src="js/statistics.js"></script>
    </head>
<body>
    <div class="container">
        <header class="header">
        <div class="header__container">
                <div class="header__menu-burger">
                    <span></span>
                </div>

                <nav class="widget">
                    <h3 class="widget-title">Протоколы стартов</h3>
                    <ul class="widget-list">
                    <li><a class="menu-link" href="http://yarfst.ru/rating_SO/sourse/20210411_report.html?scores=1&sportorg=1" target="_blank">Старт 1</a></li>
                        <li><a class="menu-link" href="http://yarfst.ru/rating_SO/sourse/20210506_report.html?scores=1&sportorg=1" target="_blank">Старт 2</a></li>
                        <li><a class="menu-link" href="http://yarfst.ru/rating_SO/sourse/20210522_report.html?scores=1&sportorg=1" target="_blank">Старт 3</a></li>
                        <li><a class="menu-link" href="http://yarfst.ru/rating_SO/sourse/20210725_report.html?scores=1&sportorg=1" target="_blank">Старт 4</a></li>
                        <li><a class="menu-link" href="http://yarfst.ru/rating_SO/sourse/20210807_report.html?scores=1&sportorg=1" target="_blank">Старт 5</a></li>
                        <li><a class="menu-link" href="http://yarfst.ru/rating_SO/sourse/20210829_report.html?scores=1&sportorg=1" target="_blank">Старт 6</a></li>
                        <li><a class="menu-link" href="http://yarfst.ru/rating_SO/sourse/20210911_report.html?scores=1&sportorg=1" target="_blank">Старт 7</a></li>
                        <li><a class="menu-link" href="http://yarfst.ru/rating_SO/sourse/20211102_report.html?scores=1&sportorg=1" target="_blank">Старт 8</a></li>
                        <li><a class="menu-link" href="http://yarfst.ru/rating_SO/sourse/20211114_report.html?scores=1&sportorg=1" target="_blank">Старт 9</a></li>
                        <li><a class="menu-link" href="http://yarfst.ru/rating_SO/sourse/20211128_report.html?scores=1&penalty_time=1&sportorg=1" target="_blank">Старт 10</a></li>
                    </ul>
                </nav>
                <div class="title" id="title-1">
                    <h1>Рейтинг участников 2021</h1>
                </div>
                <div class="title" id="title-2">
                    <h1 class="title-color">Статистика стартов 2021</h1>
                </div>

                <div class="switch">
                    <label for="tab_1" title="Рейтинг спортсменов">
                        <input type="radio" name="tab_btn" id="tab_1" value="1" checked class="radio">
                        <span class="radio-left"></span>
                    </label>

                    <label for="tab_2" title="Статистика стартов">
                        <input type="radio" name="tab_btn" id="tab_2" value="2" class="radio">
                        <span class="radio-right"></span>
                    </label>
                </div>

            </div>   
        </header>
            <?php
                require "rating.php";
            ?>
            <?php
                require "statistics.php";
            ?>

        <footer>
			<div class="main-footer">
				<p>Вопросы, замечания и предложения просьба присылать на почту <a href="mailto:o.party76@gmail.com ">o.party76@gmail.com</a></p>
			</div>	
		</footer>
    </div>
</body>
</html>