<?php 
    $dist = array(); // массив всех рейтинга со всех дистанций
    
    // определяем начальные данные
    $servername = "localhost";
    $username = "x91598g9_rating";
    $password = "eFo&nzP5";
    $dbname = "x91598g9_rating";
    $db_elite ="a_elite";
    $db_adult ="b_adult";
    $db_veteran ="b_veteran";
    $db_teanager ="b_teenager";
    $db_kid ="c_kid";
    $db_sportsmen ="sportsmen";
    $db_statisticssportsmen ="statisticssportsmen";


    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);
    // Check connection
    if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
    }

    if(isset($_POST['a'])){
        // запрос показать все уникальные рейтинг по дистанциям в порядке убывания очков убывания
        $sqlRating_elite = "SELECT $db_elite.SportsmenId AS id, CONCAT_WS(' ',$db_sportsmen.Surname, $db_sportsmen.Name) AS fio, $db_sportsmen.Year AS years, $db_sportsmen.Sex AS sex, $db_elite.CountStarts AS starts, $db_elite.Points AS points, $db_elite.PlaceChange AS place_change, $db_elite.PointsBad1 AS pointsBad1, $db_elite.PointsBad2 AS pointsBad2, $db_elite.PointsBad3 AS pointsBad3, $db_elite.PointsBad4 AS pointsBad4, $db_elite.PointsBad5 AS pointsBad5
            FROM $db_elite
            LEFT JOIN $db_sportsmen ON $db_elite.SportsmenId = $db_sportsmen.SportsmenId
            ORDER BY $db_sportsmen.Sex ASC, $db_elite.Points DESC, $db_sportsmen.Surname ASC";
        
        $sqlRating_adult = "SELECT $db_adult.SportsmenId AS id, CONCAT_WS(' ',$db_sportsmen.Surname, $db_sportsmen.Name) AS fio, $db_sportsmen.Year AS years, $db_sportsmen.Sex AS sex, $db_adult.CountStarts AS starts, $db_adult.Points AS points, $db_adult.PlaceChange AS place_change, $db_adult.PointsBad1 AS pointsBad1, $db_adult.PointsBad2 AS pointsBad2, $db_adult.PointsBad3 AS pointsBad3, $db_adult.PointsBad4 AS pointsBad4, $db_adult.PointsBad5 AS pointsBad5
            FROM $db_adult
            LEFT JOIN $db_sportsmen ON $db_adult.SportsmenId = $db_sportsmen.SportsmenId
            ORDER BY $db_sportsmen.Sex, $db_adult.Points DESC, $db_sportsmen.Surname ASC";

        $sqlRating_veteran = "SELECT $db_veteran.SportsmenId AS id, CONCAT_WS(' ',$db_sportsmen.Surname, $db_sportsmen.Name) AS fio, $db_sportsmen.Year AS years, $db_sportsmen.Sex AS sex, $db_veteran.CountStarts AS starts, $db_veteran.Points AS points, $db_veteran.PlaceChange AS place_change, $db_veteran.PointsBad1 AS pointsBad1, $db_veteran.PointsBad2 AS pointsBad2, $db_veteran.PointsBad3 AS pointsBad3, $db_veteran.PointsBad4 AS pointsBad4, $db_veteran.PointsBad5 AS pointsBad5
            FROM $db_veteran
            LEFT JOIN $db_sportsmen ON $db_veteran.SportsmenId = $db_sportsmen.SportsmenId
            ORDER BY $db_sportsmen.Sex, $db_veteran.Points DESC, $db_sportsmen.Surname ASC";

        $sqlRating_teenager = "SELECT $db_teanager.SportsmenId AS id, CONCAT_WS(' ',$db_sportsmen.Surname, $db_sportsmen.Name) AS fio, $db_sportsmen.Year AS years, $db_sportsmen.Sex AS sex, $db_teanager.CountStarts AS starts, $db_teanager.Points AS points, $db_teanager.PlaceChange AS place_change, $db_teanager.PointsBad1 AS pointsBad1, $db_teanager.PointsBad2 AS pointsBad2, $db_teanager.PointsBad3 AS pointsBad3, $db_teanager.PointsBad4 AS pointsBad4, $db_teanager.PointsBad5 AS pointsBad5
            FROM $db_teanager
            LEFT JOIN $db_sportsmen ON $db_teanager.SportsmenId = $db_sportsmen.SportsmenId
            ORDER BY $db_sportsmen.Sex, $db_teanager.Points DESC, $db_sportsmen.Surname ASC";

        $sqlRating_kid = "SELECT $db_kid.SportsmenId AS id, CONCAT_WS(' ',$db_sportsmen.Surname, $db_sportsmen.Name) AS fio, $db_sportsmen.Year AS years, $db_sportsmen.Sex AS sex, $db_kid.CountStarts AS starts, $db_kid.Points AS points, $db_kid.PlaceChange AS place_change, $db_kid.PointsBad1 AS pointsBad1, $db_kid.PointsBad2 AS pointsBad2, $db_kid.PointsBad3 AS pointsBad3, $db_kid.PointsBad4 AS pointsBad4, $db_kid.PointsBad5 AS pointsBad5
            FROM $db_kid
            LEFT JOIN $db_sportsmen ON $db_kid.SportsmenId = $db_sportsmen.SportsmenId
            ORDER BY $db_sportsmen.Sex, $db_kid.Points DESC, $db_sportsmen.Surname ASC";

        $group_elite = $conn->query($sqlRating_elite);  // берем результат отправки запроса
        $group_adult = $conn->query($sqlRating_adult);  // берем результат отправки запроса
        $group_veteran = $conn->query($sqlRating_veteran);  // берем результат отправки запроса
        $group_teenager = $conn->query($sqlRating_teenager);  // берем результат отправки запроса
        $group_kid = $conn->query($sqlRating_kid);  // берем результат отправки запроса

        if ($group_elite->num_rows > 0) { //если будет хоть одна заявка выводим ее
            $j = 0;
            while($row = $group_elite->fetch_assoc()){
                $vichet = $row['starts'] - 5;
                $points_vichet = 0;
                if ($vichet > 0) {
                    for ($i = 1; $i <= $vichet; $i++) {
                        $points_vichet += $row['pointsBad'. $i];
                    }
                }
                $dist[0][$j] = [$row['fio'], $row['years'], $row['sex'], $row['starts'], $row['points'], $row['place_change'], number_format($row['points'] - $points_vichet, 2, '.', '')];
                $j++;
            }
        }
        else {
            echo 'Все пропало куда-то';
        }

        if ($group_adult->num_rows > 0) { //если будет хоть одна заявка выводим ее
            $j = 0;
            while($row = $group_adult->fetch_assoc()){
                $vichet = $row['starts'] - 5;
                $points_vichet = 0;
                if ($vichet > 0) {
                    for ($i = 1; $i <= $vichet; $i++) {
                        $points_vichet += $row['pointsBad'. $i];
                    }
                }
                $dist[1][$j] = [$row['fio'], $row['years'], $row['sex'], $row['starts'], $row['points'], $row['place_change'], number_format($row['points'] - $points_vichet, 2, '.', '')];
                $j++;
            }
        }
            
        else {
            echo 'Все пропало куда-то';
        }

        if ($group_veteran->num_rows > 0) {
            $j = 0;
            while($row = $group_veteran->fetch_assoc()){
                $vichet = $row['starts'] - 5;
                $points_vichet = 0;
                if ($vichet > 0) {
                    for ($i = 1; $i <= $vichet; $i++) {
                        $points_vichet += $row['pointsBad'. $i];
                    }
                }
                $dist[2][$j] = [$row['fio'], $row['years'], $row['sex'], $row['starts'], $row['points'], $row['place_change'], number_format($row['points'] - $points_vichet, 2, '.', '')];
                $j++;
            }
        }
        else {
            echo 'Все пропало куда-то';
        }

        if ($group_teenager->num_rows > 0) {
            $j = 0;
            while($row = $group_teenager->fetch_assoc()){
                $vichet = $row['starts'] - 5;
                $points_vichet = 0;
                if ($vichet > 0) {
                    for ($i = 1; $i <= $vichet; $i++) {
                        $points_vichet += $row['pointsBad'. $i];
                    }
                }
                $dist[3][$j] = [$row['fio'], $row['years'], $row['sex'], $row['starts'], $row['points'], $row['place_change'], number_format($row['points'] - $points_vichet, 2, '.', '')];
                $j++;
            }
        }
        else {
            echo 'Все пропало куда-то';
        }
        
        if ($group_kid->num_rows > 0) {
            $j = 0;
            while($row = $group_kid->fetch_assoc()){
                $vichet = $row['starts'] - 5;
                $points_vichet = 0;
                if ($vichet > 0) {
                    for ($i = 1; $i <= $vichet; $i++) {
                        $points_vichet += $row['pointsBad'. $i];
                    }
                }
                $dist[4][$j] = [$row['fio'], $row['years'], $row['sex'], $row['starts'], $row['points'], $row['place_change'], number_format($row['points'] - $points_vichet, 2, '.', '')];
                $j++;
            }
        }
        else {
            echo 'Все пропало куда-то';
        }
    
        echo json_encode($dist);
        
    }

    if(isset($_POST['f'])) {
        $res = array(); //массив для возврата данных о спортсмене
        $speed = array(); // массив для поиска порядкового места участника по определенному параметру в отсортированных запросах
        list($surname, $name) = explode(" ", $_POST['f']);  // разделить значение на две переменные
        $years = $_POST['y'];
        $group =  $_POST['group'];
        // $sex = $_POST['sex'];
        
        // $sqlSportsmen0 = "SELECT gr.PlaceOld FROM $group AS gr";
        // $e = $conn->query($sqlSportsmen0);  // берем результат отправки запроса
        // if ($e->num_rows > 0) {
        //     $result0 = $e->fetch_row();
        //     $res['countgroup'] = $result0[0];
        // }

        $sqlSportsmen1 = "SELECT ss.SportsmenId, ss.AllCountStarts, ss.AllCountStartsF, ss.AllTime, ss.LengthAll, ss.AvgSpeed,ss.BestSpeed, ss.BadSpeed
        FROM statisticssportsmen AS ss 
        LEFT JOIN sportsmen AS s ON ss.SportsmenId = s.SportsmenId WHERE s.Surname = '$surname' AND s.Name = '$name' AND s.Year = '$years'";
        $x = $conn->query($sqlSportsmen1);  // берем результат отправки запроса
        if ($x->num_rows > 0) {
            $result1 = $x->fetch_row();

            $res['countstart'] = $result1[1];
            $res['countstartfinished'] =$result1[2];
            $res['timestart'][0] = (int)(intval($result1[3])/60000);
            $res['timestart'][1] = (intval($result1[3])/1000)%60;
            $res['lengthstart'] = $result1[4];
            $res['avgspeedstart'][0] = (int)(intval($result1[5])/60);
            $res['avgspeedstart'][1] = intval($result1[5])%60;
            $res['bestspeed'][0] = (int)(intval($result1[6])/60);
            $res['bestspeed'][1] = intval($result1[6])%60;
            $res['badspeed'][0] = (int)(intval($result1[7])/60);
            $res['badspeed'][1] = intval($result1[7])%60;
        }

        $SportsmenId = intval($result1[0]); // id спортсмена для получения запросов конкретного челика

        // ищем место средней скорости среди всех. плохо работает в mysql 5.7 ; CASE два раза потому что этот оператор выполняет только одно условие, а нам надо два
        // $sqlSportsmen2 = "SELECT * FROM ( SELECT @place:=CASE WHEN @avg_speed != ss.AvgSpeed THEN @place:= @place+1+@i ELSE @place END AS num, 
        //                         CASE WHEN @avg_speed != ss.AvgSpeed THEN @i:= 0 ELSE @i:=@i+1 END AS num2,
        //                          @avg_speed:= ss.AvgSpeed AS avg_speed, ss.SportsmenId AS id FROM statisticssportsmen AS ss, 
        //                          (SELECT @place:=0, @avg_speed:=0, @i:=0) AS z WHERE ss.AvgSpeed>0 ORDER BY ss.AvgSpeed ASC) AS m WHERE id ='$SportsmenId'";
        // $y = $conn->query($sqlSportsmen2);  // берем результат отправки запроса
        
        // if ($y->num_rows > 0) {
        //     $result2 = $y->fetch_row();
        //     $res['place_avg_speedall'] = $result2[0];
        //     // echo "<script>console.log($result2);</script>";
        // }
        $sqlSportsmen2 = "SELECT ss.SportsmenId AS id, ss.AvgSpeed AS avg_speed FROM statisticssportsmen AS ss 
                                WHERE ss.AvgSpeed>0 ORDER BY ss.AvgSpeed ASC";
        $y = $conn->query($sqlSportsmen2);  // берем результат отправки запроса
        if ($y->num_rows > 0) {
            $j = -1; // отсчет повторяющихся параметров
            $i = 1; // место среди участников по текущей строке
            $k = 0; // счетчик 
            $speed = [];
            while($row = $y->fetch_assoc()){
                if ($k >= 1 && $speed[$k-1] != $row['avg_speed']){
                    $i = $i + 1 + $j;
                    $j = 0;
                }
                elseif($k ==0 ){$j=0;}
                else {$j++;}
                if ($SportsmenId == $row['id']){
                    $res['place_avg_speedall'] = $i ;
                    break;
                }
                $speed[$k] = $row['avg_speed'];
                $k++;
            }
        }

            

        // ищем место средней скорости внутри группы
        // $sqlSportsmen3 = "SELECT * FROM (
        //                         SELECT @place:=CASE WHEN @avg_speed != ss.AvgSpeed THEN @place:= @place+1+@i ELSE @place END AS num, 
        //                         CASE WHEN @avg_speed != ss.AvgSpeed THEN @i:= 0 ELSE @i:=@i+1 END AS num2,
        //                         @avg_speed:= ss.AvgSpeed AS avg_speed, ss.SportsmenId AS id 
        //                         FROM $group AS ss
        //                         LEFT JOIN sportsmen AS s ON ss.SportsmenId = s.SportsmenId, (SELECT @place:=0, @avg_speed:=0, @i:=0) AS z 
        //                         WHERE ss.AvgSpeed>0 AND s.Sex = (SELECT sportsmen.Sex FROM sportsmen WHERE sportsmen.SportsmenId = '$SportsmenId') 
        //                         ORDER BY ss.AvgSpeed ASC ) AS m WHERE id ='$SportsmenId'";
        // $z = $conn->query($sqlSportsmen3);  // берем результат отправки запроса
        // if ($z->num_rows > 0) {
        //     $result3 = $z->fetch_row();
        //     $res['place_avg_speedgroup'] = $result3[0];
        // }
        // скорость средняя должна браться из самой группы, но из-за того что кто-то в нескольких групп бегает получается визуально неправильный вывод места в группе
        //типа средняя скорость у одного быстрее общая, но в группе меньше чем у другого, а показываем мы общую, а на деле в итоге в группе он ниже чем другой
        // в итоге этот вариант с еще одним LEFT всех прогоняет через общую среднюю скорость
        $sqlSportsmen3 = "SELECT ss.SportsmenId AS id, st.AvgSpeed AS avg_speed FROM $group AS ss LEFT JOIN sportsmen AS s ON ss.SportsmenId = s.SportsmenId
                                LEFT JOIN statisticssportsmen AS st ON ss.SportsmenId = st.SportsmenId 
                                WHERE st.AvgSpeed>0 AND s.Sex = (SELECT sportsmen.Sex FROM sportsmen WHERE sportsmen.SportsmenId = '$SportsmenId') ORDER BY st.AvgSpeed ASC";
        $z = $conn->query($sqlSportsmen3);  // берем результат отправки запроса
        if ($z->num_rows > 0) {
            $j = -1; // отсчет повторяющихся параметров
            $i = 1; // место среди участников по текущей строке
            $k = 0; // счетчик 
            $speed = [];
            while($row = $z->fetch_assoc()){
                if ($k >= 1 && $speed[$k-1] != $row['avg_speed']){
                    $i = $i + 1 + $j;
                    $j = 0;
                }
                elseif($k ==0 ){$j=0;}
                else {$j++;}
                if ($SportsmenId == $row['id']){
                    $res['place_avg_speedgroup'] = $i ;
                    break;
                }
                $speed[$k] = $row['avg_speed'];
                $k++;
            }
        }

        // ищем место средней скорости среди всех по половому признаку
        $sqlSportsmen4 = "SELECT ss.SportsmenId AS id, ss.AvgSpeed AS avg_speed, s.Sex AS sex FROM statisticssportsmen AS ss LEFT JOIN sportsmen AS s ON ss.SportsmenId = s.SportsmenId
                                WHERE ss.AvgSpeed>0 AND s.Sex = (SELECT sportsmen.Sex FROM sportsmen WHERE sportsmen.SportsmenId = '$SportsmenId') ORDER BY ss.AvgSpeed ASC";
        $t = $conn->query($sqlSportsmen4);  // берем результат отправки запроса
        if ($t->num_rows > 0) {
            $j = -1; // отсчет повторяющихся параметров
            $i = 1; // место среди участников по текущей строке
            $k = 0; // счетчик 
            $speed = [];
            while($row = $t->fetch_assoc()){
                if ($k >= 1 && $speed[$k-1] != $row['avg_speed']){
                    $i = $i + 1 + $j;
                    $j = 0;
                }
                elseif($k ==0 ){$j=0;}
                else {$j++;}
                if ($SportsmenId == $row['id']){
                    $res['place_avg_speed_sex'][0] = $i ;
                    if($row['sex'] == 'Ж'){
                        $res['place_avg_speed_sex'][1] = "среди женщин";
                    }
                    else {
                        $res['place_avg_speed_sex'][1] = "среди мужчин";
                    }
                    break;
                }
                $speed[$k] = $row['avg_speed'];
                $k++;
            }
        }


        // ищем место лучшей скорости среди всех 
        // $sqlSportsmen5 = "SELECT * FROM ( 
        //     SELECT @place:=CASE WHEN @best_speed != ss.BestSpeed THEN @place:= @place+1+@i ELSE @place END AS num, 
        //                 CASE WHEN @best_speed != ss.BestSpeed THEN @i:= 0 ELSE @i:=@i+1 END AS num2,
        //                 @best_speed:= ss.BestSpeed AS best_speed, ss.SportsmenId AS id FROM statisticssportsmen AS ss, 
        //                 (SELECT @place:=0, @best_speed:=0, @i:=0) AS z WHERE ss.BestSpeed>0 
        //                 ORDER BY ss.BestSpeed ASC) AS m WHERE id ='$SportsmenId'";
        // $v = $conn->query($sqlSportsmen5);  // берем результат отправки запроса
        
        // if ($v->num_rows > 0) {
        //     $result5 = $v->fetch_row();
        //     $res['place_best_speedall'] = $result5[0];
        //     // echo "<script>console.log($result2);</script>";
        // }
        $sqlSportsmen5 = "SELECT ss.SportsmenId AS id, ss.BestSpeed AS best_speed FROM statisticssportsmen AS ss 
                                WHERE ss.BestSpeed>0 ORDER BY ss.BestSpeed ASC";
        $v = $conn->query($sqlSportsmen5);  // берем результат отправки запроса
        if ($v->num_rows > 0) {
            $j = -1; // отсчет повторяющихся параметров
            $i = 1; // место среди участников по текущей строке
            $k = 0; // счетчик 
            $speed = [];
            while($row = $v->fetch_assoc()){
                if ($k >= 1 && $speed[$k-1] != $row['best_speed']){
                    $i = $i + 1 + $j;
                    $j = 0;
                }
                elseif($k ==0 ){$j=0;}
                else {$j++;}
                if ($SportsmenId == $row['id']){
                    $res['place_best_speedall'] = $i ;
                    break;
                }
                $speed[$k] = $row['best_speed'];
                $k++;
            }
        }


        // ищем место лучшей скорости среди всех по половому признаку
        // $sqlSportsmen6 = "SELECT * FROM (
        //     SELECT @place:=CASE WHEN @best_speed != ss.BestSpeed THEN @place:= @place+1+@i ELSE @place END AS num, 
        //                     CASE WHEN @best_speed != ss.BestSpeed THEN @i:= 0 ELSE @i:=@i+1 END AS num2, 
        //                     @best_speed:= ss.BestSpeed AS best_speed, ss.SportsmenId AS id, s.Sex AS sex 
        //                     FROM statisticssportsmen AS ss LEFT JOIN sportsmen AS s ON ss.SportsmenId = s.SportsmenId, 
        //                     (SELECT @place:=0, @best_speed:=0, @i:=0) AS z WHERE ss.Bestspeed>0 AND s.Sex=(SELECT sportsmen.Sex FROM sportsmen WHERE sportsmen.SportsmenId = '$SportsmenId')
        //                     ORDER BY ss.BestSpeed ASC) AS m WHERE id='$SportsmenId'";
        // $p = $conn->query($sqlSportsmen6);  // берем результат отправки запроса
        // if ($p->num_rows > 0) {
        //     $result6 = $p->fetch_row();
        //     $res['place_best_speed_sex'][0] = $result6[0];
        //     if($result6[2] == 'Ж'){
        //         $res['place_best_speed_sex'][1] = "среди женщин";
        //     }
        //     else {
        //         $res['place_best_speed_sex'][1] = "среди мужчин";
        //     }
        // }
        // echo "<script>console.log($sex);</script>";
        $sqlSportsmen6 = "SELECT ss.SportsmenId AS id, ss.BestSpeed AS best_speed, s.Sex AS sex FROM statisticssportsmen AS ss LEFT JOIN sportsmen AS s ON ss.SportsmenId = s.SportsmenId
                                WHERE ss.BestSpeed>0 AND s.Sex = (SELECT sportsmen.Sex FROM sportsmen WHERE sportsmen.SportsmenId = '$SportsmenId') ORDER BY ss.BestSpeed ASC";
        $p = $conn->query($sqlSportsmen6);  // берем результат отправки запроса
        if ($p->num_rows > 0) {
            $j = -1; // отсчет повторяющихся параметров
            $i = 1; // место среди участников по текущей строке
            $k = 0; // счетчик 
            $speed = [];
            while($row = $p->fetch_assoc()){
                if ($k >= 1 && $speed[$k-1] != $row['best_speed']){
                    $i = $i + 1 + $j;
                    $j = 0;
                }
                elseif($k ==0 ){$j=0;}
                else {$j++;}
                if ($SportsmenId == $row['id']){
                    $res['place_best_speed_sex'][0] = $i ;
                    if($row['sex'] == 'Ж'){
                        $res['place_best_speed_sex'][1] = "среди женщин";
                    }
                    else {
                        $res['place_best_speed_sex'][1] = "среди мужчин";
                    }
                    break;
                }
                $speed[$k] = $row['best_speed'];
                $k++;
            }
        }

        // ищем место лучшей скорости внутри группы
        //Это вообще не работало ни на какой бд
        // $sqlSportsmen7 = "SELECT * FROM ( 
        //                         SELECT @i:= @i+1 AS row_number, ss.SportsmenId AS id, st.BestSpeed AS best 
        //                         FROM $group AS ss 
        //                         LEFT JOIN sportsmen AS s ON ss.SportsmenId = s.SportsmenId 
        //                         LEFT JOIN statisticssportsmen AS st ON ss.SportsmenId = st.SportsmenId, (select @i:=0) AS z
        //                         WHERE st.BestSpeed>0 AND s.Sex = (SELECT sportsmen.Sex FROM sportsmen WHERE sportsmen.SportsmenId = '$SportsmenId') 
        //                         ORDER BY st.BestSpeed ASC) AS m 
        //                         WHERE id = '$SportsmenId'";
        // $q = $conn->query($sqlSportsmen7);  // берем результат отправки запроса
        // if ($q->num_rows > 0) {
        //     $result7 = $q->fetch_row();
        //     $res['place_best_speedgroup'] = $result7[0];
        // }
        $sqlSportsmen7 = "SELECT ss.SportsmenId AS id, st.BestSpeed AS best_speed FROM $group AS ss LEFT JOIN sportsmen AS s ON ss.SportsmenId = s.SportsmenId
                                LEFT JOIN statisticssportsmen AS st ON ss.SportsmenId = st.SportsmenId
                                WHERE st.BestSpeed>0 AND s.Sex = (SELECT sportsmen.Sex FROM sportsmen WHERE sportsmen.SportsmenId = '$SportsmenId') ORDER BY st.BestSpeed ASC";
        $q = $conn->query($sqlSportsmen7);  // берем результат отправки запроса
        if ($q->num_rows > 0) {
            $j = -1; // отсчет повторяющихся параметров
            $i = 1; // место среди участников по текущей строке
            $k = 0; // счетчик 
            $speed = [];
            while($row = $q->fetch_assoc()){
                if ($k >= 1 && $speed[$k-1] != $row['best_speed']){
                    $i = $i + 1 + $j;
                    $j = 0;
                }
                elseif($k ==0 ){$j=0;}
                else {$j++;}
                if ($SportsmenId == $row['id']){
                    $res['place_best_speedgroup'] = $i ;
                    break;
                }
                $speed[$k] = $row['best_speed'];
                $k++;
            }
        }

        echo json_encode($res);
    }


    if(isset($_POST['stat'])) {
        //массив для возврата данных о спортсмене
        $stat = array();

        $sqlStatistics00 = "SELECT Title, CountSportsmen, CountMen, CountWomen, CountDSQ, OutOfComp FROM statisticsstarts";
        $dd = $conn->query($sqlStatistics00);  

        if ($dd->num_rows > 0) { //если будет хоть одна строка выводим ее
            $j = 0;
            while($row = $dd->fetch_assoc()){
                $stat['statstarts'][$j] = [$row['Title'], $row['CountSportsmen'], $row['CountMen'], $row['CountWomen'], $row['CountDSQ'], $row['OutOfComp']];
                $j++;
            }
        }
    

        $sqlStatistics0 = "SELECT COUNT(StartId), MIN(small_length_segment), MAX(large_length_segment), 
        -- SUBSTRING(split_first_best,1,INSTR(split_first_best,' ')-1) AS id, 
        MIN(SUBSTRING(split_first_best,INSTR(split_first_best,' '))) AS speed,
        MAX(GREATEST(LengthA, LengthB, LengthC, LengthD)), MIN(LEAST(LengthA, LengthB, LengthC, LengthD)) 
        FROM statisticsstarts";
        $aa = $conn->query($sqlStatistics0);  // берем результат отправки запроса
        if ($aa->num_rows > 0) {
            $result = $aa->fetch_row();
            $stat['countstart'] = $result[0];
            $stat['segmentsmall'] = $result[1];
            $stat['segmentlarge'] = $result[2];
            $stat['distlarge'] = $result[4];
            $stat['distsmall'] = $result[5];
        }
        
        $sqlStatistics1 = "SELECT COUNT(s.SportsmenId), AVG(s.Year),MIN(s.year), MAX(s.Year), t1.male, t2.female, t1.yearmale, t2.yearfemale
            FROM sportsmen AS s,
            (SELECT COUNT(s1.SEX) AS male, AVG(s1.Year) AS yearmale FROM sportsmen AS s1 WHERE s1.SEX = 'М') AS t1,
            (SELECT COUNT(s2.SEX) AS female, AVG(s2.Year) AS yearfemale FROM sportsmen AS s2 WHERE s2.SEX = 'Ж') AS t2";
        $bb = $conn->query($sqlStatistics1);  // берем результат отправки запроса
        if ($bb->num_rows > 0) {
            $result = $bb->fetch_row();
            $stat['countpeople'] = $result[0];
            $stat['avgyear'] = date ( 'Y' ) - intval($result[1]);
            $stat['youngyear'] = date ( 'Y' ) - intval($result[3]);
            $stat['oldyear'] = date ( 'Y' ) - intval($result[2]);
            $stat['countpeoplemale'] = $result[4];
            $stat['countpeoplefemale'] = $result[5];
            $stat['avgyearmale'] = date ( 'Y' ) - intval($result[6]);
            $stat['avgyearfemale'] = date ( 'Y' ) - intval($result[7]);
        }

        $sqlStatistics01 = "SELECT ss1.avgmale, s1.avgfemale FROM
        (SELECT AVG(ss.AvgSpeed) AS avgmale FROM statisticssportsmen AS ss LEFT JOIN sportsmen AS s ON ss.SportsmenId = s.SportsmenId WHERE s.Sex = 'М') AS ss1,
        (SELECT AVG(ss.AvgSpeed) as avgfemale FROM statisticssportsmen AS ss LEFT JOIN sportsmen AS s ON ss.SportsmenId = s.SportsmenId WHERE s.Sex = 'Ж') AS s1";
        $bbb = $conn->query($sqlStatistics01);  // берем результат отправки запроса
        if ($bbb->num_rows > 0) {
            $result = $bbb->fetch_row();
            $stat['avgspeedmale'][0] = round((int)(intval($result[0])/60) + (intval($result[0])%60)/60, 2);
            $stat['avgspeedfemale'][0] = round((int)(intval($result[1])/60) + (intval($result[1])%60)/60, 2);
            if (strlen((string)intval($result[0])%60) == 1) {
                $stat['avgspeedmale'][1] = strval((int)(intval($result[0])/60)) . ':0' . strval(intval($result[0])%60);
            }
            else {
                $stat['avgspeedmale'][1] = strval((int)(intval($result[0])/60)) . ':' . strval(intval($result[0])%60);
            }
            if (strlen((string)intval($result[1])%60) == 1) {
                $stat['avgspeedfemale'][1] = strval((int)(intval($result[1])/60)) . ':0' . strval(intval($result[1])%60);
            }
            else {
                $stat['avgspeedfemale'][1] = strval((int)(intval($result[1])/60)) . ':' . strval(intval($result[1])%60);
            }
        }

        $sqlStatistics2 = "SELECT SUM(AllTime), SUM(LengthAll), MIN(AvgSpeed), MIN(BestSpeed), AVG(AvgSpeed) 
        FROM statisticssportsmen WHERE AvgSpeed > 0";
        $cc = $conn->query($sqlStatistics2);  // берем результат отправки запроса
        if ($cc->num_rows > 0) {
            $result = $cc->fetch_row();
            $stat['counttime'][0] = (int)(intval($result[0])/60000);
            $stat['counttime'][1] = (intval($result[0])/1000)%60;
            $stat['countlength'] = $result[1]/1000;
            $stat['avgspeedall'][0] = (int)(intval($result[4])/60);
            $stat['avgspeedall'][1] = intval($result[4])%60;
        }

        //Мужчины ищем имя по айди из предыдущего запроса среднюю скорость у кого лучшая
        $sqlStatistics02 = "SELECT CONCAT(s.Surname, ' ', s.Name), ss.AvgSpeed 
        FROM sportsmen AS s LEFT JOIN statisticssportsmen AS ss ON s.SportsmenId = ss.SportsmenId 
        WHERE s.Sex = 'М' AND ss.AvgSpeed > 0 ORDER BY ss.AvgSpeed ASC LIMIT 1";
        $result02 = ($conn->query($sqlStatistics02))->fetch_row();
        $stat['avgspeedmalebest'][0] = $result02[0]; // имя чемпиона по скорости
        $stat['avgspeedmalebest'][1] = round((int)(intval($result02[1])/60) + (intval($result02[1])%60)/60, 2); 
        if (strlen((string)intval($result02[1])%60) == 1) {
            $stat['avgspeedmalebest'][2] = strval((int)(intval($result02[1])/60)) . ':0' . strval(intval($result02[1])%60);
        }
        else {
            $stat['avgspeedmalebest'][2] = strval((int)(intval($result02[1])/60)) . ':' . strval(intval($result02[1])%60);
        }
        // $stat['avgspeedmale'][1] = (int)(intval($result02[1])/60);
        // $stat['avgspeedmale'][2] = intval($result02[1])%60;

        //Мужчины ищем имя по айди из предыдущего запроса обладателя самого быстрого перегона
        $sqlStatistics03 = "SELECT CONCAT(s.Surname, ' ', s.Name), ss.BestSpeed 
        FROM sportsmen AS s LEFT JOIN statisticssportsmen AS ss ON s.SportsmenId = ss.SportsmenId 
        WHERE s.Sex = 'М' AND ss.AvgSpeed > 0 ORDER BY ss.BestSpeed ASC LIMIT 1";
        $result03 = ($conn->query($sqlStatistics03))->fetch_row();
        $stat['speedfastmale'][0] = $result03[0]; // имя чемпиона по скорости
        $stat['speedfastmale'][1] = round((int)(intval($result03[1])/60) + (intval($result03[1])%60)/60, 2); 
        if (strlen((string)intval($result03[1])%60) == 1) {
            $stat['speedfastmale'][2] = strval((int)(intval($result03[1])/60)) . ':0' . strval(intval($result03[1])%60);
        }
        else {
            $stat['speedfastmale'][2] = strval((int)(intval($result03[1])/60)) . ':' . strval(intval($result03[1])%60);
        }
        // $stat['speedfastmale'][1] = (int)(intval($result03[1])/60);
        // $stat['speedfastmale'][2] = intval($result03[1])%60;

        //Мужчины ищем имя по айди из предыдущего запроса обладателя лучшего первого перегона
        $sqlStatistics04 = "SELECT CONCAT(s.Surname, ' ', s.Name), ss.BestSpeedFirst 
        FROM sportsmen AS s LEFT JOIN statisticssportsmen AS ss ON s.SportsmenId = ss.SportsmenId 
        WHERE s.Sex = 'М' AND ss.AvgSpeed > 0 ORDER BY ss.BestSpeedFirst ASC LIMIT 1";
        $result04 = ($conn->query($sqlStatistics04))->fetch_row();
        $stat['speedfirstfastmale'][0] = $result04[0]; // имя чемпиона по скорости
        $stat['speedfirstfastmale'][1] = round((int)(intval($result04[1])/60) + (intval($result04[1])%60)/60, 2); 
        if (strlen((string)intval($result04[1])%60) == 1) {
            $stat['speedfirstfastmale'][2] = strval((int)(intval($result04[1])/60)) . ':0' . strval(intval($result04[1])%60);
        }
        else {
            $stat['speedfirstfastmale'][2] = strval((int)(intval($result04[1])/60)) . ':' . strval(intval($result04[1])%60);
        }
        // $stat['speedfirstfastmale'][1] = (int)(intval($result04[1])/60);
        // $stat['speedfirstfastmale'][2] = intval($result04[1])%60;

        //Женщины ищем имя по айди из предыдущего запроса среднюю скорость у кого лучшая
        $sqlStatistics3 = "SELECT CONCAT(s.Surname, ' ', s.Name), ss.AvgSpeed 
        FROM sportsmen AS s LEFT JOIN statisticssportsmen AS ss ON s.SportsmenId = ss.SportsmenId 
        WHERE s.Sex = 'Ж' AND ss.AvgSpeed > 0 ORDER BY ss.AvgSpeed ASC LIMIT 1";
        $result3 = ($conn->query($sqlStatistics3))->fetch_row();
        $stat['avgspeedfemalebest'][0] = $result3[0]; // имя чемпиона по скорости
        $stat['avgspeedfemalebest'][1] = round((int)(intval($result3[1])/60) + (intval($result3[1])%60)/60, 2); 
        if (strlen((string)intval($result3[1])%60) == 1) {
            $stat['avgspeedfemalebest'][2] = strval((int)(intval($result3[1])/60)) . ':0' . strval(intval($result3[1])%60);
        }
        else {
            $stat['avgspeedfemalebest'][2] = strval((int)(intval($result3[1])/60)) . ':' . strval(intval($result3[1])%60);
        }
        // $stat['avgspeedfemale'][1] = (int)(intval($result3[1])/60);
        // $stat['avgspeedfemale'][2] = intval($result3[1])%60;

        //Женщины ищем имя по айди из предыдущего запроса обладателя самого быстрого перегона
        $sqlStatistics4 = "SELECT CONCAT(s.Surname, ' ', s.Name), ss.BestSpeed 
        FROM sportsmen AS s LEFT JOIN statisticssportsmen AS ss ON s.SportsmenId = ss.SportsmenId 
        WHERE s.Sex = 'Ж' AND ss.AvgSpeed > 0 ORDER BY ss.BestSpeed ASC LIMIT 1";
        $result4 = ($conn->query($sqlStatistics4))->fetch_row();
        $stat['speedfastfemale'][0] = $result4[0]; // имя чемпиона по скорости
        $stat['speedfastfemale'][1] = round((int)(intval($result4[1])/60) + (intval($result4[1])%60)/60, 2); 
        if (strlen((string)intval($result4[1])%60) == 1) {
            $stat['speedfastfemale'][2] = strval((int)(intval($result4[1])/60)) . ':0' . strval(intval($result4[1])%60);
        }
        else {
            $stat['speedfastfemale'][2] = strval((int)(intval($result4[1])/60)) . ':' . strval(intval($result4[1])%60);
        }
        // $stat['speedfastfemale'][1] = (int)(intval($result4[1])/60);
        // $stat['speedfastfemale'][2] = intval($result4[1])%60;

        //Женщины ищем имя по айди из предыдущего запроса обладателя лучшего первого перегона
        $sqlStatistics5 = "SELECT CONCAT(s.Surname, ' ', s.Name), ss.BestSpeedFirst 
        FROM sportsmen AS s LEFT JOIN statisticssportsmen AS ss ON s.SportsmenId = ss.SportsmenId 
        WHERE s.Sex = 'Ж' AND ss.AvgSpeed > 0 ORDER BY ss.BestSpeedFirst ASC LIMIT 1";
        $result5 = ($conn->query($sqlStatistics5))->fetch_row();
        $stat['speedfirstfastfemale'][0] = $result5[0]; // имя чемпиона по скорости
        $stat['speedfirstfastfemale'][1] = round((int)(intval($result5[1])/60) + (intval($result5[1])%60)/60, 2); 
        if (strlen((string)intval($result5[1])%60) == 1) {
            $stat['speedfirstfastfemale'][2] = strval((int)(intval($result5[1])/60)) . ':0' . strval(intval($result5[1])%60);
        }
        else {
            $stat['speedfirstfastfemale'][2] = strval((int)(intval($result5[1])/60)) . ':' . strval(intval($result5[1])%60);
        }
        // $stat['speedfirstfastfemale'][1] = (int)(intval($result5[1])/60);
        // $stat['speedfirstfastfemale'][2] = intval($result5[1])%60;

        $sqlStatistics6 = "SELECT Name AS name, COUNT(*) AS count FROM sportsmen GROUP BY Name HAVING count> 0";
        $result6 = ($conn->query($sqlStatistics6));
        if ($result6->num_rows > 0) { //если будет хоть одна заявка выводим ее
            $j = 0;
            while($row = $result6->fetch_assoc()){
                $stat['namesportsmen'][$j] = [$row['name'], $row['count']];
                $j++;
            }
        }

        echo json_encode($stat);
    }

    // закрываем соединение с сервером  базы данных
    $conn->close();
?>