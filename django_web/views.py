from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
import pandas as pd
import json
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar, Line, Scatter
import pyecharts.options as opts
from .detection import *

try:
    import six  # for modern Django
except ImportError:
    from django.utils import six  # for legacy Django

try:
    from io import BytesIO as IO  # for modern python
except ImportError:
    from io import StringIO as IO  # for legacy python
import datetime

csv = pd.DataFrame()
pd_data = pd.DataFrame()

export = pd.DataFrame()
export1 = pd.DataFrame()
export2 = pd.DataFrame()


def home(request):
    return render(request, "display.html")


def draw_line(df1, df2, sensor):
    line = (
        Line()
            .add_xaxis(xaxis_data=df1.tolist())
            .add_yaxis(
            series_name=sensor,
            y_axis=df2.tolist(),
            is_connect_nones=False,
        )
            .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(is_show=True, orient='vertical', pos_left='right',
                                          feature=opts.ToolBoxFeatureOpts(
                                              save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(title="Save as Image"
                                                                                               ,
                                                                                               background_color='#eee'),
                                              restore=opts.ToolBoxFeatureRestoreOpts(),
                                              data_view=opts.ToolBoxFeatureDataViewOpts(is_show=False),
                                              data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                                              magic_type=opts.ToolBoxFeatureDataViewOpts(is_show=False),
                                              brush=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                                          )),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            datazoom_opts=opts.DataZoomOpts(),
            xaxis_opts=opts.AxisOpts(
                name='Timestamp',
            ),
            yaxis_opts=opts.AxisOpts(
                name=sensor,
                splitline_opts=opts.SplitLineOpts(is_show=True),
            )
        )
    )
    return line;


def upload(request):
    global csv
    if request.method == "POST":

        default = {"KLT12_flowRate1 (l/min)": 'Default(LSTM)',
                   "IT Power Consumption (W)": 'Default(LSTM)',
                   "Outside Temperature (°C)": 'Default(LSTM)',
                   "KLT11_pumpSpeed_p1 (Hz)": 'Default(LSTM)',
                   "KLT11_Fan1Speed_HZ (Hz)": 'Default(LSTM)',
                   "KLT13_inletTempBeforeHydraulicGate (°C)": 'Default(LSTM)',
                   "KLT14_pumpSpeed_p1": 'Default(HBOS)',
                   "wetBulb": 'Default(LSTM)',
                   "KLT14_Fan1Speed_HZ": 'Default(IForest)',
                   "P_WW": 'Default(HBOS)',
                   }

        default_sensor = ["KLT12_flowRate1 (l/min)", 'IT Power Consumption (W)', 'Outside Temperature (°C)',
                          'KLT11_pumpSpeed_p1 (Hz)', 'KLT11_Fan1Speed_HZ (Hz)',
                          'KLT13_inletTempBeforeHydraulicGate (°C)', 'KLT14_pumpSpeed_p1', 'wetBulb',
                          'KLT14_Fan1Speed_HZ', 'P_WW']

        file = request.FILES["myFile"]
        form_dict = dict(six.iterlists(request.POST))
        print(form_dict['dim_select'][0])

        csv = pd.read_excel(file)
        print(csv.head())
        if csv is not None:
            enable = True

        col = csv.columns.values.tolist()
        col.remove('timestamp')
        sensor = col[0]
        csv['timestamp'] = pd.to_datetime(csv['timestamp'])
        print(col)

        if sensor not in default_sensor:
            return JsonResponse({"error": "input data type not match! Unitvariate: 'KLT12_flowRate1 (l/min)', "
                                          "'IT Power Consumption (W)', 'Outside Temperature (°C)',"
                                          "'KLT11_pumpSpeed_p1 (Hz)', 'KLT11_Fan1Speed_HZ (Hz)',"
                                          "'KLT13_inletTempBeforeHydraulicGate (°C)', 'KLT14_pumpSpeed_p1', "
                                          "'wetBulb', 'KLT14_Fan1Speed_HZ' "
                                          "Multivariate:'KLT14_pumpSpeed_p1'+'KLT14_pumpSpeed_p2',"
                                          "'KLT14_Fan1Speed_HZ'+'KLT14_Fan2Speed_HZ' "},
                                status=400)

        if form_dict['dim_select'][0] == 'Multi':
            if len(col) == 1:
                return JsonResponse({"error": "Input data is not multivariate"},
                                    status=400)
            if len(col) > 2:
                return JsonResponse({"error": "only accept Multivariate:'KLT14_pumpSpeed_p1'+'KLT14_pumpSpeed_p2','KLT14_Fan1Speed_HZ'+'KLT14_Fan2Speed_HZ'"},
                                    status=400)

            line = draw_line(csv['timestamp'], csv[col[0]], col[0])

            line1 = (
                Line()
                    .add_xaxis(xaxis_data=csv['timestamp'].tolist())
                    .add_yaxis(
                    series_name=col[1],
                    # yaxis_index=1,
                    y_axis=csv[col[1]].tolist(),
                    is_connect_nones=False,
                )
            )
            csv = csv[[sensor, col[1], 'timestamp']]
            if len(col) == 2:
                line.overlap(line1)
                line.extend_axis(
                    yaxis=opts.AxisOpts(
                        name=col[1],
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    )
                )

            if len(col) == 3:
                line2 = (
                    Line()
                        .add_xaxis(xaxis_data=csv['timestamp'].tolist())
                        .add_yaxis(
                        series_name=col[2],
                        y_axis=csv[col[2]].tolist(),
                        is_connect_nones=False,
                    )
                )
                line.overlap(line1)
                line.overlap(line2)
                line.extend_axis(
                    yaxis=opts.AxisOpts(
                        name=col[2],
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    )
                )
                csv = csv[[sensor, col[1], col[2], 'timestamp']]

        else:
            # if len(col) > 1:
            #     return JsonResponse({"error": "Input data is not unitvariate"},
            #                         status=400)
            line = draw_line(csv['timestamp'], csv[sensor], sensor)
            csv = csv[[sensor, 'timestamp']]

        bar_total_trend = json.loads(line.dump_options())

        table = csv.to_html(
            classes='ui selectable celled table',
            table_id='data'
        )

        table1 = csv.to_html(
            classes='ui selectable celled table',
            table_id='data1'
        )
        context = {
            'enable': enable,
            'data': table,
            'data1': table1,
            'bar_total_trend': bar_total_trend,
            'default_algo': default[sensor],
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False), content_type="application/json charset=utf-8")


def query(request):
    global pd_data
    global csv

    global export
    global export1
    global export2
    pd_data = csv

    table = pd_data.to_html(
        classes='ui selectable celled table',
        table_id='data'
    )
    context = {
        'data': table,
    }

    form_dict = dict(six.iterlists(request.GET))

    col = csv.columns.values.tolist()
    col.remove('timestamp')
    sensor = col[0]

    csv['timestamp'] = pd.to_datetime(csv['timestamp'])

    algo = ['Forest', 'Hbos', 'Cblof']

    default = {"KLT12_flowRate1 (l/min)": 'Default(LSTM)',
               "IT Power Consumption (W)": 'Default(LSTM)',
               "Outside Temperature (°C)": 'Default(LSTM)',
               "KLT11_pumpSpeed_p1 (Hz)": 'Default(LSTM)',
               "KLT11_Fan1Speed_HZ (Hz)": 'Default(LSTM)',
               "KLT13_inletTempBeforeHydraulicGate (°C)": 'Default(LSTM)',
               "KLT14_pumpSpeed_p1": 'Default(HBOS)',
               "wetBulb": 'Default(LSTM)',
               "KLT14_Fan1Speed_HZ": 'Default(IForest)',
               }
    default_sensor = ["KLT12_flowRate1 (l/min)", 'IT Power Consumption (W)', 'Outside Temperature (°C)',
                      'KLT11_pumpSpeed_p1 (Hz)', 'KLT11_Fan1Speed_HZ (Hz)',
                      'KLT13_inletTempBeforeHydraulicGate (°C)', 'KLT14_pumpSpeed_p1', 'wetBulb',
                      'KLT14_Fan1Speed_HZ']

    if 'ALGO_select' in form_dict:
        if len(col) == 1:
            csv = csv[[sensor, 'timestamp']]
            if form_dict['ALGO_select'][0] == 'Lstm':
                if sensor not in default_sensor:
                    return JsonResponse({"error": "no match lstm model"},
                                        status=400)
                pd_data = lstm_detection(csv, contamination=0.05)
            elif form_dict['ALGO_select'][0] in algo:
                pd_data = forest_detection(csv, form_dict['ALGO_select'][0], contamination=0.05)
            else:
                if sensor == "P_WW":
                    pd_data = forest_detection(csv, 'Hbos', contamination=0.05)
                else:
                    if sensor not in default_sensor:
                        return JsonResponse({"error": "no match lstm model"},
                                            status=400)
                    pd_data = lstm_detection(csv, contamination=0.05)
                    print(default[sensor])
            table = pd_data.to_html(
                classes='ui selectable celled table',
                table_id='data1'
            )

            line = draw_line(pd_data['timestamp'], pd_data['original'], sensor)

            outlier_data = pd_data.loc[pd_data['anomaly'] == 1]
            pd_data['cleananomaly'] = np.nan
            for index in outlier_data.index.tolist():
                pd_data.loc[index, 'cleananomaly'] = pd_data.loc[index, 'original']

            line1 = draw_line(pd_data['timestamp'], pd_data['original'], sensor)

            scatter = (
                Line()
                    .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                    .add_yaxis(
                    series_name="outlier",
                    y_axis=pd_data['cleananomaly'].tolist(),
                    # symbol_size=5,
                    is_connect_nones=False,

                )
                    .set_global_opts(

                    tooltip_opts=opts.TooltipOpts(is_show=False),
                    yaxis_opts=opts.AxisOpts(
                        splitline_opts=opts.SplitLineOpts(is_show=True),

                    )
                )

            )
            line1.overlap(scatter)

            line2 = draw_line(pd_data['timestamp'], pd_data[sensor], sensor)

        if len(col) == 2:
            csv = csv[[col[0], col[1], 'timestamp']]
            if form_dict['ALGO_select'][0] == 'Lstm':
                if sensor not in default_sensor:
                    return JsonResponse({"error": "no match lstm model"},
                                        status=400)
                pd_data = multi_lstm_detection(csv, contamination=0.05)
            elif form_dict['ALGO_select'][0] in algo:
                pd_data = forest_detection(csv, form_dict['ALGO_select'][0], contamination=0.05)
            else:
                if default[sensor] == 'Default(LSTM)':
                    if sensor not in default_sensor:
                        return JsonResponse({"error": "no match lstm model"},
                                            status=400)
                    pd_data = multi_lstm_detection(csv, contamination=0.05)
                else:
                    if sensor == "KLT14_pumpSpeed_p1" or "P_WW":
                        pd_data = forest_detection(csv, 'Hbos', contamination=0.05)
                    if sensor == "KLT14_Fan1Speed_HZ":
                        pd_data = forest_detection(csv, 'Forest', contamination=0.05)
                print(default[sensor])
            table = pd_data.to_html(
                classes='ui selectable celled table',
                table_id='data1'
            )

            line = draw_line(pd_data['timestamp'], pd_data['original' + " " + col[0]], col[0])
            line_1 = (
                Line()
                    .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                    .add_yaxis(
                    series_name=col[1],
                    y_axis=pd_data['original' + " " + col[1]].tolist(),
                    is_connect_nones=False,
                )
            )
            line.overlap(line_1)
            line.extend_axis(
                yaxis=opts.AxisOpts(
                    name=col[1],
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                )
            )

            outlier_data = pd_data.loc[pd_data['anomaly'] == 1]
            pd_data['cleananomaly' + " " + col[0]] = np.nan
            pd_data['cleananomaly' + " " + col[1]] = np.nan
            for index in outlier_data.index.tolist():
                pd_data.loc[index, 'cleananomaly' + " " + col[0]] = pd_data.loc[index, 'original' + " " + col[0]]
                pd_data.loc[index, 'cleananomaly' + " " + col[1]] = pd_data.loc[index, 'original' + " " + col[1]]

            line1 = draw_line(pd_data['timestamp'], pd_data['original' + " " + col[0]], col[0])
            line1_1 = (
                Line()
                    .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                    .add_yaxis(
                    series_name=col[1],
                    y_axis=pd_data['original' + " " + col[1]].tolist(),
                    is_connect_nones=False,
                )
            )

            scatter_1 = (
                Line()
                    .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                    .add_yaxis(
                    series_name="outlier" + " " + col[0],
                    y_axis=pd_data['cleananomaly' + " " + col[0]].tolist(),
                    is_connect_nones=False,

                )
                    .set_global_opts(

                    tooltip_opts=opts.TooltipOpts(is_show=False),
                    yaxis_opts=opts.AxisOpts(
                        splitline_opts=opts.SplitLineOpts(is_show=True),

                    )
                )

            )
            scatter_2 = (
                Line()
                    .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                    .add_yaxis(
                    series_name="outlier" + " " + col[1],
                    y_axis=pd_data['cleananomaly' + " " + col[1]].tolist(),
                    is_connect_nones=False,

                )
                    .set_global_opts(

                    tooltip_opts=opts.TooltipOpts(is_show=False),
                    yaxis_opts=opts.AxisOpts(
                        splitline_opts=opts.SplitLineOpts(is_show=True),

                    )
                )

            )
            line1.overlap(scatter_1)
            line1_1.overlap(scatter_2)
            line1.overlap(line1_1)
            line1.extend_axis(
                yaxis=opts.AxisOpts(
                    name=col[1],
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                )
            )

            line2 = draw_line(pd_data['timestamp'], pd_data[col[0]], col[0])
            line2_1 = (
                Line()
                    .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                    .add_yaxis(
                    series_name=col[1],
                    y_axis=pd_data[col[1]].tolist(),
                    is_connect_nones=False,
                )
            )
            line2.overlap(line2_1)
            line2.extend_axis(
                yaxis=opts.AxisOpts(
                    name=col[1],
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                )
            )

        bar_total_trend = json.loads(line.dump_options())
        bar_total_trend1 = json.loads(line1.dump_options())
        bar_total_trend2 = json.loads(line2.dump_options())

        # export = pd_data[['original', 'timestamp']]
        # export1 = pd_data
        # export2 = pd_data[[sensor, 'timestamp']]

        if len(col) == 1:
            csv = pd_data[[sensor, 'timestamp']]
        if len(col) == 2:
            csv = pd_data[[col[0], col[1], 'timestamp']]

        context = {
            'data': table,
            'bar_total_trend': bar_total_trend,
            'bar_total_trend1': bar_total_trend1,
            'bar_total_trend2': bar_total_trend2
        }

    if 'Gap_filling' in form_dict:
        print(len(col))

        line = draw_line(pd_data['timestamp'], pd_data[sensor], sensor)
        if len(col) == 2:
            line_1 = (
                Line()
                    .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                    .add_yaxis(
                    series_name=col[1],
                    y_axis=pd_data[col[1]].tolist(),
                    is_connect_nones=False,
                )
            )
            line.overlap(line_1)
            line.extend_axis(
                yaxis=opts.AxisOpts(
                    name=col[1],
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                )
            )

        # export = pd_data

        pd_data = gap_filling(csv, form_dict['Gap_filling'][0])
        table = pd_data.to_html(
            classes='ui selectable celled table',
            table_id='data2'
        )

        line1 = draw_line(pd_data['timestamp'], pd_data[sensor], sensor)

        scatter = (
            Line()
                .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                .add_yaxis(
                series_name="filling" + " " + col[0],
                y_axis=pd_data['filling' + " " + col[0]].tolist(),
                is_connect_nones=False,

            )
                .set_global_opts(
                tooltip_opts=opts.TooltipOpts(is_show=False),
                yaxis_opts=opts.AxisOpts(
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                )
            )

        )
        line1.overlap(scatter)
        if len(col) == 2:
            line1_1 = (
                Line()
                    .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                    .add_yaxis(
                    series_name=col[1],
                    y_axis=pd_data[col[1]].tolist(),
                    is_connect_nones=False,
                )
            )
            scatter1 = (
                Line()
                    .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                    .add_yaxis(
                    series_name="filling" + " " + col[1],
                    y_axis=pd_data['filling' + " " + col[1]].tolist(),
                    is_connect_nones=False,

                )
                    .set_global_opts(
                    tooltip_opts=opts.TooltipOpts(is_show=False),
                    yaxis_opts=opts.AxisOpts(
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    )
                )

            )
            line1_1.overlap(scatter1)
            line1.overlap(line1_1)
            line1.extend_axis(
                yaxis=opts.AxisOpts(
                    name=col[1],
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                )
            )

        line2 = draw_line(pd_data['timestamp'], pd_data[sensor], sensor)
        if len(col) == 2:
            line2_1 = draw_line(pd_data['timestamp'], pd_data[col[1]], col[1])
            line2.overlap(line2_1)
            line2.extend_axis(
                yaxis=opts.AxisOpts(
                    name=col[1],
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                )
            )

        bar_total_trend = json.loads(line.dump_options())
        bar_total_trend1 = json.loads(line1.dump_options())
        bar_total_trend2 = json.loads(line2.dump_options())

        # export1 = pd_data
        # export2 = pd_data

        if len(col) == 1:
            csv = pd_data[[sensor, 'timestamp']]
        if len(col) == 2:
            csv = pd_data[[col[0], col[1], 'timestamp']]

        context = {
            'data': table,
            'bar_total_trend': bar_total_trend,
            'bar_total_trend1': bar_total_trend1,
            'bar_total_trend2': bar_total_trend2
        }

    return HttpResponse(json.dumps(context, ensure_ascii=False), content_type="application/json charset=utf-8")


def export(request):
    form_dict = dict(six.iterlists(request.GET))
    print(type)

    df = export

    excel_file = IO()

    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    df.to_excel(xlwriter, 'data', index=True)

    xlwriter.save()
    xlwriter.close()

    excel_file.seek(0)

    response = HttpResponse(excel_file.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    response['Content-Disposition'] = 'attachment; filename=' + now + '.xlsx'
    return response


def export1(request):
    form_dict = dict(six.iterlists(request.GET))
    print(type)

    df = export1

    excel_file = IO()

    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    df.to_excel(xlwriter, 'data', index=True)

    xlwriter.save()
    xlwriter.close()

    excel_file.seek(0)

    response = HttpResponse(excel_file.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    response['Content-Disposition'] = 'attachment; filename=' + now + '.xlsx'
    return response


def export2(request):
    form_dict = dict(six.iterlists(request.GET))
    print(type)

    df = export2

    excel_file = IO()

    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    df.to_excel(xlwriter, 'data', index=True)

    xlwriter.save()
    xlwriter.close()

    excel_file.seek(0)

    response = HttpResponse(excel_file.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    response['Content-Disposition'] = 'attachment; filename=' + now + '.xlsx'
    return response
