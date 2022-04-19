$(document).on('click', 'input[value="2"]', function() {

    var options1 = {
        navigation: {
            buttonOptions: {
                enabled: false
            }
        },
        title: {
            text: 'Информация об участниках'
        },
        xAxis: {
            categories: ['Средний возраст', 'Средний возраст мужчин', 'Средний возраст женщин', 'Самый молодой участник', 'Самый опытный участник']
        },
        yAxis: {
            title: {
                text: 'возраст'
            }
        },
        labels: {
            items: [{
                html: [],
                style: {
                    left: '110px',
                    top: '18px',
                    color: ( // theme
                        Highcharts.defaultOptions.title.style &&
                        Highcharts.defaultOptions.title.style.color
                    ) || 'black'
                }
            }]
        },
        plotOptions: {
            column: {
                /* настройка ширины колонки */
                maxPointWidth: 40
            }
        },
        series: [{
            type: 'column',
            name: 'участники',
            data: [],
            color: Highcharts.getOptions().colors[1],
            tooltip: {
                pointFormatter: function () {
                    return this.y + ' ' + this.okonchanie;
                }
            },
            dataLabels: {
                enabled: true,
                color: '#FFFFFF',
                align: 'center',
                x: 0,
                y: 0,
                rotation: 0
            }
        }, {
            type: 'pie',
            name: 'Всего',
            data: [{
                name: 'Мужчины',
                y: [],
                color: Highcharts.getOptions().colors[0] 
            }, {
                name: 'Женщины',
                y: [],
                color: Highcharts.getOptions().colors[2] // Joe's color
            }],
            center: [150, 80],
            size: 100,
            showInLegend: false,
            dataLabels: {
                enabled: true,
                color: '#FFFFFF',
                align: 'center',
                x: 0,
                y: 0,
                rotation: 0
            }
        }]
    };

    var options2 = {
        navigation: {
            buttonOptions: {
                enabled: false
            }
        },
        title: {
            text: 'График участия спортсменов'
        },
        xAxis: {
            categories: []
        },
        yAxis: {
            title: {
                text: 'количество'
            }
        },
        series: [{
            type: 'column',
            name: 'Мужчины',
            data: [],
            color: '#2b908f',
            dataLabels: {
                enabled: true,
                color: '#FFFFFF',
                align: 'center',
                x: 0,
                y: 0,
                rotation: 0
            }
        }, {
            type: 'column',
            name: 'Женщины',
            data: [],
            color: '#f45b5b',
            dataLabels: {
                enabled: true,
                color: '#FFFFFF',
                align: 'center',
                x: 0,
                y: 0,
                rotation: 0
            }
        }, {
            type: 'column',
            name: 'Снятые',
            data: [],
            color: '#90ee7e',
            dataLabels: {
                enabled: true,
                color: '#FFFFFF',
                align: 'center',
                x: 0,
                y: 0,
                rotation: 0
            }
        }, {
            type: 'spline',
            name: 'Всего',
            data: [],
            marker: {
                lineWidth: 2,
                lineColor: Highcharts.getOptions().colors[3],
                fillColor: 'white'
            },
            dataLabels: {
                enabled: true,
                color: '#FFFFFF',
                align: 'center',
                x: 0,
                y: 0,
                rotation: 0
            }
        }
        ]
    };


    var options4 = {  
        navigation: {
            buttonOptions: {
                enabled: false
            }
        },
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Скорости участников'
        },
        // subtitle: {
        //     text: 'Source: <a href="http://populationpyramid.net/germany/2018/">Population Pyramids of the World from 1950 to 2100</a>'
        // },
        accessibility: {
            point: {
                valueDescriptionFormat: '{index}. Age {xDescription}, {value}%.'
            }
        },
        xAxis: [{
            categories: ['Средняя скорость', 'Лучшая средняя скорость', 'Самый быстрый перегон', 'Самый быстрый первый перегон'],
            reversed: false,
            labels: {
                step: 1
            },
            accessibility: {
                description: 'Категория (мужчины)'
            }
        }, { // mirror axis on right side
            opposite: true,
            reversed: false,
            categories: ['Средняя скорость', 'Лучшая средняя скорость', 'Самый быстрый перегон', 'Самый быстрый первый перегон'],
            linkedTo: 0,
            labels: {
                step: 1
            },
            accessibility: {
                description: 'Категория (женщины)'
            }
        }],
        yAxis: {
            title: {
                text: null
            },
            labels: {
                formatter: function () {
                    return Math.abs(this.value) + ' м/км';
                }
            },
            accessibility: {
                description: 'Скорость',
                // rangeDescription: 'Range: 0 to 5%'
            }
        },
        plotOptions: {
            series: {
                stacking: 'normal'
            }
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.series.name + ', ' + this.point.name + '</b><br/>' +
                this.point.category + ': ' + this.point.temp + ' м/км';
            }
        },
        series: [{
            name: 'Мужчины',
            data: [],
            color: '#2b908f'
        }, {
            name: 'Женщины',
            data: [],
            color: '#f45b5b'
        }]
    };

    var options5 = {
        // chart: {
        //     style: {
        //         fontFamily: 'Helvetica'
        //     }
        // },
        navigation: {
            buttonOptions: {
                enabled: false
            }
        },
        accessibility: {
            screenReaderSection: {
                beforeChartFormat: '<h5>{chartTitle}</h5>' +
                    '<div>{chartSubtitle}</div>' +
                    '<div>{chartLongdesc}</div>' +
                    '<div>{viewTableButton}</div>'
            }
        },
        series: [{
            type: 'wordcloud',
            data: [],
            name: 'Встречаемость'
        }],
        title: {
            text: 'Имена участников'
        }
    };
    
    // загрузка статистики
    bdLoad();
    

    // переключение вкладок меню статистики стартов
    $(function() {
        $('.ca-menu').delegate('li:not(.chosen)', 'click', function() {
          $(this).addClass('chosen').siblings().removeClass('chosen')
           .parents('.block-in').find('.tab-content').hide().eq( $(this).index() ).fadeIn(170);
        });
      });


    // показать статистику по стартам
    function bdLoad(){
        $.ajax({
            type: "POST",
            url: "load_db.php",
            data: {
               stat: 'stat'
            },
            success: function(response){
                var jsonData = JSON.parse(response);  // раскодируем json данные

                // Инфа об участниках
                options1.series[0].data.push({
                    y: parseFloat(jsonData.avgyear),
                    okonchanie: okonchanie(jsonData.avgyear)[1]
                });
                options1.series[0].data.push({
                    y: parseFloat(jsonData.avgyearmale),
                    okonchanie: okonchanie(jsonData.avgyearmale)[1]
                });
                options1.series[0].data.push({
                    y: parseFloat(jsonData.avgyearfemale),
                    okonchanie: okonchanie(jsonData.avgyearfemale)[1]
                });
                options1.series[0].data.push({
                    y: parseFloat(jsonData.youngyear),
                    okonchanie: okonchanie(jsonData.youngyear)[1]
                });
                options1.series[0].data.push({
                    y: parseFloat(jsonData.oldyear),
                    okonchanie: okonchanie(jsonData.oldyear)[0]
                });
                options1.labels.items[0].html.push('Всего участников: ' + parseFloat(jsonData.countpeople));
                options1.series[1].data.push({
                    name: 'Мужчины',
                    y: parseFloat(jsonData.countpeoplemale),
                    color: Highcharts.getOptions().colors[0] 
                });
                options1.series[1].data.push({
                    name: 'Женщины',
                    y: parseFloat(jsonData.countpeoplefemale),
                    color: Highcharts.getOptions().colors[2] 
                });
                Highcharts.chart('chart-sportsmen', options1);

                // График участия спорстменов
                for(let i = 0; i < jsonData.statstarts.length; i++) {
                    options2.xAxis.categories.push(jsonData.statstarts[i][0]);
                    options2.series[0].data.push(parseFloat(jsonData.statstarts[i][2]));
                    options2.series[1].data.push(parseFloat(jsonData.statstarts[i][3]));
                    options2.series[2].data.push(parseFloat(jsonData.statstarts[i][4]));
                    options2.series[3].data.push(parseFloat(jsonData.statstarts[i][1]));
                }
                Highcharts.chart('chart-start', options2);
                
                // Скорости участников
                // мужчины
                options4.series[0].data.push({
                    name: 'среди всех',
                    y: -parseFloat(jsonData.avgspeedmale[0]),
                    temp: jsonData.avgspeedmale[1] 
                });
                options4.series[0].data.push({
                    name: jsonData.avgspeedmalebest[0],
                    y: -parseFloat(jsonData.avgspeedmalebest[1]),
                    temp: jsonData.avgspeedmalebest[2] 
                });
                options4.series[0].data.push({
                    name: jsonData.speedfastmale[0],
                    y: -parseFloat(jsonData.speedfastmale[1]),
                    temp: jsonData.speedfastmale[2] 
                });
                options4.series[0].data.push({
                    name: jsonData.speedfirstfastmale[0],
                    y: -parseFloat(jsonData.speedfirstfastmale[1]),
                    temp: jsonData.speedfirstfastmale[2] 
                });

                //женщины
                options4.series[1].data.push({
                    name: 'среди всех',
                    y: parseFloat(jsonData.avgspeedfemale[0]),
                    temp: jsonData.avgspeedfemale[1] 
                });
                options4.series[1].data.push({
                    name: jsonData.avgspeedfemalebest[0],
                    y: parseFloat(jsonData.avgspeedfemalebest[1]),
                    temp: jsonData.avgspeedfemalebest[2] 
                });
                options4.series[1].data.push({
                    name: jsonData.speedfastfemale[0],
                    y: parseFloat(jsonData.speedfastfemale[1]),
                    temp: jsonData.speedfastfemale[2] 
                });
                options4.series[1].data.push({
                    name: jsonData.speedfirstfastfemale[0],
                    y: parseFloat(jsonData.speedfirstfastfemale[1]),
                    temp: jsonData.speedfirstfastfemale[2] 
                });
                Highcharts.chart('chart-speed', options4);
                
                // График Имен участников
                for(let i = 0; i < jsonData.namesportsmen.length; i++) {
                    options5.series[0].data.push({
                        name: jsonData.namesportsmen[i][0],
                        weight: jsonData.namesportsmen[i][1]
                    });
                }
                // Include this snippet after loading Highcharts and before Highcharts.chart is executed.
                Highcharts.seriesTypes.wordcloud.prototype.deriveFontSize = function (relativeWeight) {
                    var maxFontSize = 23;
                // Will return a fontSize between 0px and 25px.
                if (relativeWeight < 0.08) { // взависимости от того сколько слово раз встречается ему присваивается вес от 0 до 1 (считается в wordcloud.js)
                    return Math.floor(2); // принудительно чуть увеличиваем размер шрифта для самых редких слов
                }
                else {
                    return Math.floor(maxFontSize * relativeWeight);  
                } 
                };
                Highcharts.chart('chart-name', options5);
                
                $('.count-start').html(jsonData.countstart + " / 10");
                $('.count-people').html(jsonData.countpeople);
                // $('.count-people-male').html(jsonData.countpeoplemale);
                // $('.count-people-female').html(jsonData.countpeoplefemale);                
                // $('.avg-year').html(jsonData.avgyear + " " + okonchanie(jsonData.avgyear)[0]);
                // $('.avg-year-male').html(jsonData.avgyearmale + " " + okonchanie(jsonData.avgyearmale)[1]);
                // $('.avg-year-female').html(jsonData.avgyearfemale + " " + okonchanie(jsonData.avgyearfemale)[1]);
                // $('.young-year').html(jsonData.youngyear + " " + okonchanie(jsonData.youngyear)[1]);
                // $('.old-year').html(jsonData.oldyear + " " + okonchanie(jsonData.oldyear)[1]);

                
                if (parseInt(jsonData.counttime[0], 10) / 60 > 1 ){  // если время больше часа. для отображения часов минут секунд
                    let hour = Math.floor(parseInt(jsonData.counttime[0], 10) / 60);
                    let minute = parseInt(jsonData.counttime[0], 10) % 60;
                    if (minute.toString().length == 1){
                        if (jsonData.counttime[1].toString().length == 1){
                            $('.count-time').html(hour + ":0"+ minute + ":0" + jsonData.counttime[1] );
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
                
                // $('.lengthstart').html(jsonData.lengthstart + " м");
                $('.count-length').html(jsonData.countlength + ' км');
                $('.segment-small').html(jsonData.segmentsmall + ' м');
                $('.segment-large').html(jsonData.segmentlarge + ' м');
                $('.dist-small').html(jsonData.distsmall + ' м');
                $('.dist-large').html(jsonData.distlarge + ' м');

                // // Средняя скорость участников
                // if (jsonData.avgspeedall[1].toString().length == 1){
                //     $('.avg-speed-all').html(jsonData.avgspeedall[0] + ":0" + jsonData.avgspeedall[1] + " м/км");
                // }
                // else {
                //     $('.avg-speed-all').html( jsonData.avgspeedall[0] + ":" + jsonData.avgspeedall[1] + " м/км");
                // }

                // // лучший средняя скорость у мужчин
                // if (jsonData.avgspeedmale[2].toString().length == 1){
                //     $('.avg-speed-m').html(jsonData.avgspeedmale[0] + " - " + jsonData.avgspeedmale[1] + ":0" + jsonData.avgspeedmale[2] + " м/км");
                // }
                // else {
                //     $('.avg-speed-m').html(jsonData.avgspeedmale[0] + " - " + jsonData.avgspeedmale[1] + ":" + jsonData.avgspeedmale[2] + " м/км");
                // }

                // // лучший перегон у мужчин
                // if (jsonData.speedfastmale[2].toString().length == 1){
                //     $('.speed-fast-m').html(jsonData.speedfastmale[0] + " - " + jsonData.speedfastmale[1] + ":0" + jsonData.speedfastmale[2] + " м/км");
                // }
                // else {
                //     $('.speed-fast-m').html(jsonData.speedfastmale[0] + " - " + jsonData.speedfastmale[1] + ":" + jsonData.speedfastmale[2] + " м/км");
                // }

                // // лучший первый перегон у мужчин
                // if (jsonData.speedfirstfastmale[2].toString().length == 1){
                //     $('.speed-first-fast-m').html(jsonData.speedfirstfastmale[0] + " - " + jsonData.speedfirstfastmale[1] + ":0" + jsonData.speedfirstfastmale[2] + " м/км");
                // }
                // else {
                //     $('.speed-first-fast-m').html(jsonData.speedfirstfastmale[0] + " - " + jsonData.speedfirstfastmale[1] + ":" + jsonData.speedfirstfastmale[2] + " м/км");
                // }
                // // // лучший первый перегон у мужчин
                // // if (jsonData.speedfirstfast[2].toString().length == 1){
                // //     $('.speed-first-fast-m').html(jsonData.speedfirstfast[0] + " - " + jsonData.speedfirstfast[1] + ":0" + jsonData.speedfirstfast[2] + " м/км");
                // // }
                // // else {
                // //     $('.speed-first-fast-m').html(jsonData.speedfirstfast[0] + " - " + jsonData.speedfirstfast[1] + ":" + jsonData.speedfirstfast[2] + " м/км");
                // // }


                // // лучший средняя скорость
                // if (jsonData.avgspeedfemale[2].toString().length == 1){
                //     $('.avg-speed-f').html(jsonData.avgspeedfemale[0] + " - " + jsonData.avgspeedfemale[1] + ":0" + jsonData.avgspeedfemale[2] + " м/км");
                // }
                // else {
                //     $('.avg-speed-f').html(jsonData.avgspeedfemale[0] + " - " + jsonData.avgspeedfemale[1] + ":" + jsonData.avgspeedfemale[2] + " м/км");
                // }

                // // лучший перегон 
                // if (jsonData.speedfastfemale[2].toString().length == 1){
                //     $('.speed-fast-f').html(jsonData.speedfastfemale[0] + " - " + jsonData.speedfastfemale[1] + ":0" + jsonData.speedfastfemale[2] + " м/км");
                // }
                // else {
                //     $('.speed-fast-f').html(jsonData.speedfastfemale[0] + " - " + jsonData.speedfastfemale[1] + ":" + jsonData.speedfastfemale[2] + " м/км");
                // }

                // // лучший первый перегон
                // if (jsonData.speedfirstfastfemale[2].toString().length == 1){
                //     $('.speed-first-fast-f').html(jsonData.speedfirstfastfemale[0] + " - " + jsonData.speedfirstfastfemale[1] + ":0" + jsonData.speedfirstfastfemale[2] + " м/км");
                // }
                // else {
                //     $('.speed-first-fast-f').html(jsonData.speedfirstfastfemale[0] + " - " + jsonData.speedfirstfastfemale[1] + ":" + jsonData.speedfirstfastfemale[2] + " м/км");
                // }

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