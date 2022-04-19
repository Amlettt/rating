$(document).on('click', 'input[value="2"]', function() {
    
    google.charts.load("current", {packages:["corechart"]});
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {
      var data = google.visualization.arrayToDataTable([
        ['Task', 'Hours per Day'],
        ['Work',     11],
        ['Eat',      2],
        ['Commute',  2],
        ['Watch TV', 2],
        ['Sleep',    7]
      ]);

      var options = {
        title: 'My Daily Activities',
        is3D: true,
      };

      var chart = new google.visualization.PieChart(document.getElementById('piechart_3d'));
      chart.draw(data, options);
    }


    //Better to construct options first and then pass it as a parameter
    var options = {
        title: {
            text: "возраст участников"              
        },
        data: [              
        {
            // Change type to "doughnut", "line", "splineArea", etc.
            type: "column",
            dataPoints: [
                { label: "самый молодой",  y: 5  },
                { label: "самый опытный", y: 74  },
                { label: "средний мужчины", y: 25  },
                { label: "средний женщины",  y: 25  },
                { label: "средний всех участников",  y: 25  }
            ]
        }
        ]
    };
    
    $("#chartContainer").CanvasJSChart(options);
    
    var options2 = {
        exportEnabled: true,
        animationEnabled: true,
        title:{
            text: "количество участников"
        },
        legend:{
            horizontalAlign: "right",
            verticalAlign: "center"
        },
        data: [{
            type: "pie",
            showInLegend: true,
            toolTipContent: "<b>{name}</b>: {y} человек (#percent%)",
            indexLabel: "{name}",
            legendText: "{name} (#percent%)",
            indexLabelPlacement: "inside",
            dataPoints: [
                { y: 140, name: "Мужчины" },
                { y: 76, name: "Женщины" }
            ]
        }]
    };
    $("#chartContainer2").CanvasJSChart(options2);


    var options3 = {
        animationEnabled: true,
        theme: "light2",
        title:{
            text: "График темпа"
        },
        axisX:{
            // valueFormatString: "DD MMM"
        },
        axisY: {
            title: "темп",
            suffix: "м/км",
            minimum: 0
        },
        toolTip:{
            shared:true
        },  
        legend:{
            cursor:"pointer",
            verticalAlign: "bottom",
            horizontalAlign: "left",
            dockInsidePlotArea: true,
            itemclick: toogleDataSeries
        },
        data: [{
            type: "line",
            showInLegend: true,
            name: "Средняя скорость",
            markerType: "square",
            // xValueFormatString: "DD MMM, YYYY",
            color: "#F08080",
            yValueFormatString: "#,##0K",
            dataPoints: [
                { x: "1 старт", y: 4.5 },
                { x: "2 старт", y: 6.9 },
                { x: "3 старт", y: 6.5 },
                // { x: new Date(2017, 10, 4), y: 70 },
                // { x: new Date(2017, 10, 5), y: 71 },
                // { x: new Date(2017, 10, 6), y: 65 },
                // { x: new Date(2017, 10, 7), y: 73 },
                // { x: new Date(2017, 10, 8), y: 96 },
                // { x: new Date(2017, 10, 9), y: 84 },
                // { x: new Date(2017, 10, 10), y: 85 },
                // { x: new Date(2017, 10, 11), y: 86 },
                // { x: new Date(2017, 10, 12), y: 94 },
                // { x: new Date(2017, 10, 13), y: 97 },
                // { x: new Date(2017, 10, 14), y: 86 },
                // { x: new Date(2017, 10, 15), y: 89 }
            ]
        },
        {
            type: "line",
            showInLegend: true,
            name: "Actual Sales",
            lineDashType: "dash",
            yValueFormatString: "#,##0K",
            dataPoints: [
                { x: new Date(2017, 10, 1), y: 6.0 },
                { x: new Date(2017, 10, 2), y: 5.7 },
                { x: new Date(2017, 10, 3), y: 5.1 },
                // { x: new Date(2017, 10, 4), y: 56 },
                // { x: new Date(2017, 10, 5), y: 54 },
                // { x: new Date(2017, 10, 6), y: 55 },
                // { x: new Date(2017, 10, 7), y: 54 },
                // { x: new Date(2017, 10, 8), y: 69 },
                // { x: new Date(2017, 10, 9), y: 65 },
                // { x: new Date(2017, 10, 10), y: 66 },
                // { x: new Date(2017, 10, 11), y: 63 },
                // { x: new Date(2017, 10, 12), y: 67 },
                // { x: new Date(2017, 10, 13), y: 66 },
                // { x: new Date(2017, 10, 14), y: 56 },
                // { x: new Date(2017, 10, 15), y: 64 }
            ]
        }]
    };
    $("#chartContainer3").CanvasJSChart(options3);
    
    function toogleDataSeries(e){
        if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
            e.dataSeries.visible = false;
        } else{
            e.dataSeries.visible = true;
        }
        e.chart.render();
    }


    // загрузка статистики
    bdLoad();

    // показать статистику по стартам
    function bdLoad(){
        $.ajax({
            type: "POST",
            url: "load_db.php",
            // dataType: "json",
            data: {
               stat: 'stat'
            },
            success: function(response){
                var jsonData = JSON.parse(response);  // раскодируем json данные
                
                $('.count-start').html(jsonData.countstart);
                $('.count-people').html(jsonData.countpeople);
                $('.count-people-male').html(jsonData.countpeoplemale);
                $('.count-people-female').html(jsonData.countpeoplefemale);                
                $('.avg-year').html(jsonData.avgyear + " " + okonchanie(jsonData.avgyear)[0]);
                $('.avg-year-male').html(jsonData.avgyearmale + " " + okonchanie(jsonData.avgyearmale)[1]);
                $('.avg-year-female').html(jsonData.avgyearfemale + " " + okonchanie(jsonData.avgyearfemale)[1]);
                $('.young-year').html(jsonData.youngyear + " " + okonchanie(jsonData.youngyear)[1]);
                $('.old-year').html(jsonData.oldyear + " " + okonchanie(jsonData.oldyear)[1]);

                
                $('.count-time').html(jsonData.counttime);
                if (parseInt(jsonData.counttime[0], 10) / 60 > 1 ){  // если время больше часа. для отображения часов минут секунд
                    let hour = Math.floor(parseInt(jsonData.counttime[0], 10) / 60);
                    let minute = parseInt(jsonData.counttime[0], 10) % 60;
                    if (minute.toString().length == 1){
                        if (jsonData.counttime[1].toString().length == 1){
                            $('.count-time').html(hour + "ч:0"+ minute + ":0" + jsonData.counttime[1] );
                        }
                        else {
                            $('.count-time').html(hour + ":0"+ minute + ":" + jsonData.counttime[1] );
                        }
                    }
                    else{
                        if (jsonData.counttime[1].toString().length == 1){
                            $('.count-time').html(hour+ ":"+ minute + ":0" + jsonData.counttime[1] );
                        }
                        else {
                            $('.count-time').html(hour+ ":"+ minute + ":" + jsonData.counttime[1] );
                        }
                    }
                   
                }
                else {
                    if (jsonData.counttime[1].toString().length == 1){
                        $('.count-time').html(jsonData.counttime[0] + ":0" + jsonData.counttime[1] );
                    }
                    else {
                        $('.count-time').html(jsonData.counttime[0] + ":" + jsonData.counttime[1] );
                    }
                }
                
                $('.lengthstart').html(jsonData.lengthstart + " м");
                $('.count-length').html(jsonData.countlength + ' км');
                $('.segment-small').html(jsonData.segmentsmall + ' м');
                $('.segment-large').html(jsonData.segmentlarge + ' м');
                $('.dist-small').html(jsonData.distsmall + ' м');
                $('.dist-large').html(jsonData.distlarge + ' м');

                // Средняя скорость участников
                if (jsonData.avgspeedall[1].toString().length == 1){
                    $('.avg-speed-all').html(jsonData.avgspeedall[0] + ":0" + jsonData.avgspeedall[1] + " м/км");
                }
                else {
                    $('.avg-speed-all').html( jsonData.avgspeedall[0] + ":" + jsonData.avgspeedall[1] + " м/км");
                }

                // лучший средняя скорость у мужчин
                if (jsonData.avgspeedmale[2].toString().length == 1){
                    $('.avg-speed-m').html(jsonData.avgspeedmale[0] + " - " + jsonData.avgspeedmale[1] + ":0" + jsonData.avgspeedmale[2] + " м/км");
                }
                else {
                    $('.avg-speed-m').html(jsonData.avgspeedmale[0] + " - " + jsonData.avgspeedmale[1] + ":" + jsonData.avgspeedmale[2] + " м/км");
                }

                // лучший перегон у мужчин
                if (jsonData.speedfastmale[2].toString().length == 1){
                    $('.speed-fast-m').html(jsonData.speedfastmale[0] + " - " + jsonData.speedfastmale[1] + ":0" + jsonData.speedfastmale[2] + " м/км");
                }
                else {
                    $('.speed-fast-m').html(jsonData.speedfastmale[0] + " - " + jsonData.speedfastmale[1] + ":" + jsonData.speedfastmale[2] + " м/км");
                }

                // лучший первый перегон у мужчин
                if (jsonData.speedfirstfastmale[2].toString().length == 1){
                    $('.speed-first-fast-m').html(jsonData.speedfirstfastmale[0] + " - " + jsonData.speedfirstfastmale[1] + ":0" + jsonData.speedfirstfastmale[2] + " м/км");
                }
                else {
                    $('.speed-first-fast-m').html(jsonData.speedfirstfastmale[0] + " - " + jsonData.speedfirstfastmale[1] + ":" + jsonData.speedfirstfastmale[2] + " м/км");
                }
                // // лучший первый перегон у мужчин
                // if (jsonData.speedfirstfast[2].toString().length == 1){
                //     $('.speed-first-fast-m').html(jsonData.speedfirstfast[0] + " - " + jsonData.speedfirstfast[1] + ":0" + jsonData.speedfirstfast[2] + " м/км");
                // }
                // else {
                //     $('.speed-first-fast-m').html(jsonData.speedfirstfast[0] + " - " + jsonData.speedfirstfast[1] + ":" + jsonData.speedfirstfast[2] + " м/км");
                // }


                // лучший средняя скорость
                if (jsonData.avgspeedfemale[2].toString().length == 1){
                    $('.avg-speed-f').html(jsonData.avgspeedfemale[0] + " - " + jsonData.avgspeedfemale[1] + ":0" + jsonData.avgspeedfemale[2] + " м/км");
                }
                else {
                    $('.avg-speed-f').html(jsonData.avgspeedfemale[0] + " - " + jsonData.avgspeedfemale[1] + ":" + jsonData.avgspeedfemale[2] + " м/км");
                }

                // лучший перегон 
                if (jsonData.speedfastfemale[2].toString().length == 1){
                    $('.speed-fast-f').html(jsonData.speedfastfemale[0] + " - " + jsonData.speedfastfemale[1] + ":0" + jsonData.speedfastfemale[2] + " м/км");
                }
                else {
                    $('.speed-fast-f').html(jsonData.speedfastfemale[0] + " - " + jsonData.speedfastfemale[1] + ":" + jsonData.speedfastfemale[2] + " м/км");
                }

                // лучший первый перегон
                if (jsonData.speedfirstfastfemale[2].toString().length == 1){
                    $('.speed-first-fast-f').html(jsonData.speedfirstfastfemale[0] + " - " + jsonData.speedfirstfastfemale[1] + ":0" + jsonData.speedfirstfastfemale[2] + " м/км");
                }
                else {
                    $('.speed-first-fast-f').html(jsonData.speedfirstfastfemale[0] + " - " + jsonData.speedfirstfastfemale[1] + ":" + jsonData.speedfirstfastfemale[2] + " м/км");
                }

            }
          });

    }

    function okonchanie(chislo){
        var last = parseInt(chislo.toString().slice(-1), 10); // получаем последнюю цифру от числа
        var arr = [12, 13, 14]; // "год"

        if (last == 1 && chislo != 11 ) {
            return ["годик", "год"];
        }
        else if (5 > last && last > 1) {
            if (-1 !== $.inArray(chislo, arr)) { // если содержится в массиве
                 return ["годиков", "лет"];
            }
            return ["годика", "года"];
        }
        else {
            return ["годиков", "лет"];
        }
    }
});