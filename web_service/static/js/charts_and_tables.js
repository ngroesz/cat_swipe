class Chart
{
    constructor(chartDisplayName, containerName, baseDataUrl, seriesList)
    {
        this.chartDisplayName = chartDisplayName;
        this.containerName = containerName;
        this.baseDataUrl = baseDataUrl;
        this.seriesList = seriesList;
        this.seriesNames = $.unique($.map(seriesList, function (d) { return d['name'] }));
        this.chart = null;
        this.chartOptions = null;
        this.timeOptions = {};
        this.interquartileFilter = {};

        this.seriesIndexBySeriesNameAndKey = {};
        for(var i = 0; i < this.seriesList.length; i++) {
            var series = this.seriesList[i];
            this.seriesIndexBySeriesNameAndKey[series['name']] = this.seriesIndexBySeriesNameAndKey[series['name']] || {};
            this.seriesIndexBySeriesNameAndKey[series['name']][series['key']] = i;
            if (series['options'] && series['options']['show_weekly_as_interquartile'] == 'true') {
                this.interquartileFilter[series['name']] = this.interquartileFilter[series['name']] || [];
                this.interquartileFilter[series['name']].push(series['key']);
            }
        }
        this.setupChart();
    }

    getChartYAxis()
    {
        var yAxis = [];
        for (var i = 0; i < this.seriesList.length; ++i) {
            var series = this.seriesList[i];
            yAxis.push({
                labels: { format: '{value} ' + series.units, },
                title: { text: series.label, },
                opposite: i % 2 == true,
            });
        }
        return yAxis;
    }

    getSeriesOptions()
    {
        var allSeriesOptions = [];
        for (var i = 0; i < this.seriesList.length; ++i) {
            var series = this.seriesList[i];
            var defaultSeriesOptions = {
                name: series.label,
                lineWidth: 0,
                yAxis: series.length,
                type: 'scatter',
                tooltip: {
                    valueSuffix: ' ' + series.units,
                }
            };

            // merge default options with per-series options
            var seriesOptions = Object.assign({}, defaultSeriesOptions, this.seriesList[i].seriesOptions);

            allSeriesOptions.push(seriesOptions);
        }
        return allSeriesOptions;
    }

    getSeriesData(data)
    {
        var seriesData = [];
        var seriesIndexByName = {};

        for (var s = 0; s < this.seriesList.length; s++) {
            seriesData[s] = [];
        }

        for (var dataIndex = 0; dataIndex < data.length; dataIndex++) {
            var datum = data[dataIndex];
            for (var key in datum['attributes']['data']) {
                var index = this.seriesIndexBySeriesNameAndKey[datum['attributes']['name']][key];
                if(index != null) {
                    seriesData[index].push([
                        new Date(datum['attributes']['sensor_time']).getTime(),
                        datum['attributes']['data'][key]
                    ]);
                }
            }
        }

        return seriesData;
    }

    getChartOptions()
    {
        return {
            chart: { type: 'line', },
            title: { text: this.chartDisplayName, },
            xAxis: {
                type: 'datetime',
                dateTimeLabelFormats: {
                    month: '%e. %b',
                    day: '%e. %b',
                },
            },
            yAxis: [],
            legend: { enabled: false, },
            credits: { enabled: false, },
            tooltip: { shared: true, },
            plotOptions: {
                line: {
                    lineWidth: 0,
                }
            },
            series: []
        };
    }

    setupChart()
    {
        this.chartOptions = this.getChartOptions();
        this.chartOptions.yAxis = this.getChartYAxis();
        this.chartOptions.series = this.getSeriesOptions();
        this.chart = Highcharts.chart(this.containerName, this.chartOptions);
    }

    adjustTimeScaleSeconds(element)
    {
        this.timeOptions.relativeSeconds = $(element).attr('value');
        $('.adjustChartTimeScaleSecondsButton').each(function() {
            $(this).attr('disabled', false);
        });
        $(element).attr('disabled', 'disabled');
        this.updateChart();
    }

    adjustTimeScaleDays(element)
    {
        if ($(element).attr('id') == 'time_scale_daily') {
            $('#time_scale_weekly').attr('disabled', false);
            $('#time_scale_daily').attr('disabled', 'disabled');
            this.timeOptions.timeScaleDays = 1;
            this.timeOptions.startLimit = this.timeOptions.endLimit.clone().subtract(1, 'days');
        } else if ($(element).attr('id') == 'time_scale_weekly') {
            $('#time_scale_daily').attr('disabled', false);
            $('#time_scale_weekly').attr('disabled', 'disabled');
            this.timeOptions.timeScaleDays = 7;
            this.timeOptions.startLimit = this.timeOptions.endLimit.clone().subtract(7, 'days');
        } else if ($(element).attr('id') == 'adjust_time_back') {
            this.timeOptions.startLimit.subtract(this.timeOptions.timeScaleDays, 'days');
            this.timeOptions.endLimit.subtract(this.timeOptions.timeScaleDays, 'days');
        } else if($(element).attr('id') == 'adjust_time_forward') {
            this.timeOptions.startLimit.add(this.timeOptions.timeScaleDays, 'days');
            this.timeOptions.endLimit.add(this.timeOptions.timeScaleDays, 'days');
        }

        this.updateChart();
    }

    updateChart()
    {
        var dataUrl = this.baseDataUrl;
        var filter = [{"name": "name", "op": "in_", "val": this.seriesNames}];
        if (this.timeOptions.relativeSeconds && this.timeOptions.relativeSeconds > 0) {
            dataUrl = [dataUrl, '&relative_time_limit=', this.timeOptions.relativeSeconds].join("");
            var startTime = moment.utc().subtract(this.timeOptions.relativeSeconds, 'seconds').format("YYYY-MM-DD HH:MM:ss");
        } else if(this.timeOptions.startLimit && this.timeOptions.endLimit) {
            filter.push({"name": "sensor_time", "op": "ge", "val": this.timeOptions.startLimit.format()});
            filter.push({"name": "sensor_time", "op": "le", "val": this.timeOptions.endLimit.format()});
            var startTime = this.timeOptions.startLimit.format('YYYY-MM-DD HH:MM:ss');
            var endTime = this.timeOptions.endLimit.format('YYYY-MM-DD HH:MM:ss');
            $('#date_range').html(startTime + ' -- ' + endTime);
        }

        // we need to save-off "this" since the $.getJSON function will hide it
        var chart_this = this;

        dataUrl = dataUrl + '&filter=' + JSON.stringify(filter);

        if (Object.keys(this.interquartileFilter).length > 0) {
            dataUrl += '&interquartile_range=' + JSON.stringify([this.interquartileFilter]);
        }

        $.getJSON(dataUrl, function (json) {
            var seriesData = chart_this.getSeriesData(json.data);
            for (var i=0; i<seriesData.length; i++) {
                chart_this.chart.series[i].setData(seriesData[i], true);
            }
        });
    }
}


class Table
{
    constructor(displayName, containerName, baseDataUrl, seriesList)
    {
        this.displayName = displayName;
        this.containerName = containerName;
        this.baseDataUrl = baseDataUrl;
        this.seriesList = seriesList;
        this.seriesNames = $.unique($.map(seriesList, function (d) { return d['name'] }));
        this.seriesNames.unshift('sensor_time');
        this.dataColumns = $.map(seriesList, function(series) {
            return {title: series.label};
        });
        this.dataColumns.unshift({'title': 'Timezone'});
        this.dataColumns.unshift({'title': 'Timestamp', 'type': 'date', 'render': renderDateTime});

        this.seriesIndexBySeriesNameAndKey = {};
        for(var i = 0; i < this.seriesList.length; i++) {
            var series = this.seriesList[i];
            this.seriesIndexBySeriesNameAndKey[series['name']] = this.seriesIndexBySeriesNameAndKey[series['name']] || {};
            // series index begins at one because of the added column
            this.seriesIndexBySeriesNameAndKey[series['name']][series['key']] = i + 1;
        }
        this.table = $('#' + containerName).DataTable(this.getTableOptions());
    }

    getTableOptions()
    {
        return {
            'paging': true,
            'searching': false,
            'info': false,
            'lengthMenu': [
                [ 5, 10, 25, 50, -1, ],
                [ 5, 10, 25, 50, "All", ],
            ],
            'columns': this.dataColumns,
            'order': [[0, 'desc']]
        };

    }

    getDataSet(data)
    {
        var dataSetMap = {};
        for (var i = 0; i < data.length; i++) {
            var datum = data[i];
            var key = datum['attributes']['sensor_time'];
            var values = dataSetMap[key];
            if (values == null) {
                values = Array(this.seriesList.length + 1);
                values[0] = datum['attributes']['timezone'];
                values.fill('', 1)
            }
            for (var datumKey in datum['attributes']['data']) {
                values[this.seriesIndexBySeriesNameAndKey[datum['attributes']['name']][datumKey]] = datum['attributes']['data'][datumKey];
            }
            dataSetMap[key] = values;
        }

        var dataSet = [];
        for(var key in dataSetMap) {
            dataSet.push([key, dataSetMap[key]].flat());
        }

        dataSet.sort(function(a, b) {
            return new Date(a) - new Date(b);
        });
        return dataSet;
    }

    updateTable()
    {
        // we need to save-off "this" since the $.getJSON function will hide it
        var table_this = this;
        var containerId = '#' + this.containerName;
        $.getJSON(this.baseDataUrl, function(json) {
            var data = table_this.getDataSet(json.data);
            table_this.table.clear();
            table_this.table.rows.add(data);
            table_this.table.draw();
        });
    }
}
