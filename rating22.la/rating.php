<section class="page" id="page-1">
    <div id="tabs">
        <div class="tab__menu">
            <div class="tab__menu-left">
                <div class="tab whiteborder">Элита</div>
                <div class="tab">Взрослые</div>
                <div class="tab">Ветераны</div>
                <div class="tab">Подростки</div>
                <div class="tab">Дети</div>
                
            </div>
            <div class="tab__menu-right">
                <label class="checkbox-ya">
                    <input type="checkbox">
                    <span class="checkbox-ya-switch">
                        <span class="checkbox-ya-feature" data-label-on="Жен" data-label-off="Муж"></span>
                    </span>
                </label>
            </div>
        </div>

        <table class="table table-content group-a_elite" cellspacing="10" cellpadding="0">
            <thead>
                <tr>
                    <th class="th">№</th>
                    <th class="th">Фамилия Имя</th>
                    <th class="th">Статистика</th>
                    <th class="th">Год рождения</th>
                    <th class="th">Кол-во стартов</th>
                    <th class="th">Очки</th>
                    <th class="th">Очки с вычетом: <span style="font-size: 12px;text-transform: none;">5 стартов</span></th>
                    <!-- <th class="th th-img-change-place">
                        <img src="img/change_place.png" height="25px" width="37px" title="Изменние позиции в рейтинге">
                    </th> -->
                </tr>
            </thead>
            <tbody>
                <tr>
                </tr>
            </tbody>
        </table>

        <table class="table table-content group-b_adult" cellspacing="10" cellpadding="0">
            <thead>
                <tr>
                    <th class="th">№</th>
                    <th class="th">Фамилия Имя</th>
                    <th class="th">Статистика</th>
                    <th class="th">Год рождения</th>
                    <th class="th">Кол-во стартов</th>
                    <th class="th">Очки</th>
                    <th class="th">Очки с вычетом: <span style="font-size: 12px;text-transform: none;">5 стартов</span></th>
                    <!-- <th class="th th-img-change-place">
                        <img src="img/change_place.png" height="25px" width="37px" title="Изменние позиции в рейтинге">
                    </th> -->
                </tr>
            </thead>
            <tbody>
                <tr>
                </tr>
            </tbody>
        </table>

        <table class="table table-content group-b_veteran" cellspacing="10" cellpadding="0">
            <thead>
                <tr>
                    <th class="th">№</th>
                    <th class="th">Фамилия Имя</th>
                    <th class="th">Статистика</th>
                    <th class="th">Год рождения</th>
                    <th class="th">Кол-во стартов</th>
                    <th class="th">Очки</th>
                    <th class="th">Очки с вычетом: <span style="font-size: 12px;text-transform: none;">5 стартов</span></th>
                    <!-- <th class="th th-img-change-place">
                        <img src="img/change_place.png" height="25px" width="37px" title="Изменние позиции в рейтинге">
                    </th> -->
                </tr>
            </thead>
            <tbody>
                <tr>
                </tr>
            </tbody>
        </table>

        <table class="table table-content group-b_teenager" cellspacing="10" cellpadding="0">
            <thead>
                <tr>
                    <th class="th">№</th>
                    <th class="th">Фамилия Имя</th> 
                    <th class="th">Статистика</th>
                    <th class="th">Год рождения</th>
                    <th class="th">Кол-во стартов</th>
                    <th class="th">Очки</th>
                    <th class="th">Очки с вычетом: <span style="font-size: 12px;text-transform: none;">5 стартов</span></th>
                    <!-- <th class="th th-img-change-place">
                        <img src="img/change_place.png" height="25px" width="37px" title="Изменние позиции в рейтинге">
                    </th> -->
                </tr>
            </thead>
            <tbody>
                <tr>                   
                </tr>
            </tbody>
        </table>

        <table class="table table-content group-c_kid" cellspacing="10" cellpadding="0">
            <thead>
                <tr>
                    <th class="th">№</th>
                    <th class="th">Фамилия Имя</th>
                    <th class="th">Статистика</th>
                    <th class="th">Год рождения</th>
                    <th class="th">Кол-во стартов</th>
                    <th class="th">Очки</th>
                    <th class="th">Очки с вычетом: <span style="font-size: 12px;text-transform: none;">5 стартов</span></th>
                    <!-- <th class="th th-img-change-place">
                        <img src="img/change_place.png" height="25px" width="37px" title="Изменние позиции в рейтинге">
                    </th> -->
                </tr>
            </thead>
            <tbody>
                <tr>                   
                </tr>
            </tbody>
        </table>

    </div>

    <div class="window-block">
        <div class="statistics-sportsmen">
            <div class="cl-btn-7" id="exit"></div>
            <div class="statistics-sportsmen__title">Статистика спортсмена</div>

            <div class="statistics-sportsmen__info">
                <div></div>
                <div></div>
            </div>
            <div class="statistics-sportsmen__table">

                <table cellspacing="10" cellpadding="0">
                <tr>
                    <th></th><th></th>
                </tr>
                <tr>
                    <td class="stat-item">Количество стартов: </td>
                    <td><p class="stat-content countstart"></p></td>
                </tr>
                <tr>
                    <td class="stat-item">Общее время в лесу: </td>
                    <td><p class="stat-content timestart"></p></td>
                </tr>
                <tr>
                    <td class="stat-item">Общая длина дистанций*: </td>
                    <td><p class="stat-content lengthstart"></p></td>
                </tr>
                <tr>
                    <td class="stat-item">Средняя скорость**: </td>
                    <td><p class="stat-content avgspeedstart"></p></td>
                </tr>
                <tr>
                    <td class="stat-item">Самый быстрый перегон: </td>
                    <td><p class="stat-content bestspeed"></p></td>
                </tr>
                <tr>
                    <td class="stat-item">Самый медленный перегон: </td>
                    <td><p class="stat-content badspeed"></p></td>
                </tr>
                </table> 
            </div>
            <div class="statistics-ps">
                <span></span>
                <p>* - сумма дистанциий на которые спортсмен выходил (не зависимо добежал он или нет)</p>
                <p>** - средняя скорость считается только по успешным сплитам программы SportOrg (есть зависимость скорости от кол-ва стартов и местности)</p>
            </div>
        </div>
    </div>
</section>