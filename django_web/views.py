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
import re

# from io import StringIO
# import io
# from xhtml2pdf import pisa
# from django.http import HttpResponse
# from cgi import escape
#
# from django.http import StreamingHttpResponse
# import pdfkit
from django.http import FileResponse
# import os
# import base64
# import img2pdf
#
# from reportlab.pdfgen import canvas
# from PIL import Image

from snapshot_phantomjs import snapshot
from pyecharts.render import make_snapshot

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
export3 = pd.DataFrame()
export4 = pd.DataFrame()
export5 = pd.DataFrame()
export6 = pd.DataFrame()


def home(request):
    return render(request, "display.html")


def draw_line(df1, df2, sensor):
    line = (
        Line(init_opts=opts.InitOpts(animation_opts=opts.AnimationOpts(animation=False)))
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
        # .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.2),)
    )
    return line;


default = {"KLT11_flowRate1": 'Default(LSTM)',
           "KLT12_flowRate1": 'Default(LSTM)',
           "KLT13_flowRate1": 'Default(LSTM)',
           "KLT14_flowRate1": 'Default(LSTM)',
           "KLT11_flowRate2": 'Default(LSTM)',
           "KLT12_flowRate2": 'Default(LSTM)',
           "KLT13_flowRate2": 'Default(LSTM)',
           "KLT14_flowRate2": 'Default(LSTM)',
           "IT Power Consumption (W)": 'Default(LSTM)',
           "Outside Temperature (°C)": 'Default(LSTM)',
           "KLT11_pumpSpeed_p1": 'Default(LSTM)',
           "KLT12_pumpSpeed_p1": 'Default(LSTM)',
           "KLT13_pumpSpeed_p1": 'Default(LSTM)',
           "KLT14_pumpSpeed_p1": 'Default(LSTM)',
           "KLT11_pumpSpeed_p2": 'Default(LSTM)',
           "KLT12_pumpSpeed_p2": 'Default(LSTM)',
           "KLT13_pumpSpeed_p2": 'Default(LSTM)',
           "KLT14_pumpSpeed_p2": 'Default(LSTM)',
           "KLT11_Fan1Speed_HZ": 'Default(LSTM)',
           "KLT12_Fan1Speed_HZ": 'Default(LSTM)',
           "KLT13_Fan1Speed_HZ": 'Default(LSTM)',
           "KLT14_Fan1Speed_HZ": 'Default(LSTM)',
           "KLT11_Fan2Speed_HZ": 'Default(LSTM)',
           "KLT12_Fan2Speed_HZ": 'Default(LSTM)',
           "KLT13_Fan2Speed_HZ": 'Default(LSTM)',
           "KLT14_Fan2Speed_HZ": 'Default(LSTM)',
           "KLT13_inletTempBeforeHydraulicGate": 'Default(LSTM)',
           "KLT11_inletTempBeforeHydraulicGate": 'Default(LSTM)',
           "KLT12_inletTempBeforeHydraulicGate": 'Default(LSTM)',
           "KLT14_inletTempBeforeHydraulicGate": 'Default(LSTM)',
           "wetBulb": 'Default(LSTM)',
           "dryBulb": 'Default(LSTM)',
           "P_WW": 'Default(Hbos)',
           }
default_sensor = ["KLT11_flowRate1",
                  "KLT12_flowRate1",
                  "KLT13_flowRate1",
                  "KLT14_flowRate1",
                  "KLT11_flowRate2",
                  "KLT12_flowRate2",
                  "KLT13_flowRate2",
                  "KLT14_flowRate2",
                  "IT Power Consumption (W)",
                  "Outside Temperature (°C)",
                  "KLT11_pumpSpeed_p1",
                  "KLT12_pumpSpeed_p1",
                  "KLT13_pumpSpeed_p1",
                  "KLT14_pumpSpeed_p1",
                  "KLT11_pumpSpeed_p2",
                  "KLT12_pumpSpeed_p2",
                  "KLT13_pumpSpeed_p2",
                  "KLT14_pumpSpeed_p2",
                  "KLT11_Fan1Speed_HZ",
                  "KLT12_Fan1Speed_HZ",
                  "KLT13_Fan1Speed_HZ",
                  "KLT14_Fan1Speed_HZ",
                  "KLT11_Fan2Speed_HZ",
                  "KLT12_Fan2Speed_HZ",
                  "KLT13_Fan2Speed_HZ",
                  "KLT14_Fan2Speed_HZ",
                  "KLT13_inletTempBeforeHydraulicGate",
                  "KLT11_inletTempBeforeHydraulicGate",
                  "KLT12_inletTempBeforeHydraulicGate",
                  "KLT14_inletTempBeforeHydraulicGate",
                  "wetBulb",
                  "dryBulb",
                  "P_WW"]
default_multi_sensor = ["KLT11_pumpSpeed_p1 KLT11_pumpSpeed_p2",
                        "KLT12_pumpSpeed_p1 KLT12_pumpSpeed_p2",
                        "KLT13_pumpSpeed_p1 KLT13_pumpSpeed_p2",
                        "KLT14_pumpSpeed_p1 KLT14_pumpSpeed_p2",
                        "KLT11_Fan1Speed_HZ KLT11_Fan2Speed_HZ",
                        "KLT12_Fan1Speed_HZ KLT12_Fan2Speed_HZ",
                        "KLT13_Fan1Speed_HZ KLT13_Fan2Speed_HZ",
                        "KLT14_Fan1Speed_HZ KLT14_Fan2Speed_HZ"]
default_multi = {"KLT11_pumpSpeed_p1 KLT11_pumpSpeed_p2": 'Default(Hbos)',
                 "KLT12_pumpSpeed_p1 KLT12_pumpSpeed_p2": 'Default(Hbos)',
                 "KLT13_pumpSpeed_p1 KLT13_pumpSpeed_p2": 'Default(Hbos)',
                 "KLT14_pumpSpeed_p1 KLT14_pumpSpeed_p2": 'Default(Hbos)',
                 "KLT11_Fan1Speed_HZ KLT11_Fan2Speed_HZ": 'Default(Forest)',
                 "KLT12_Fan1Speed_HZ KLT12_Fan2Speed_HZ": 'Default(Forest)',
                 "KLT13_Fan1Speed_HZ KLT13_Fan2Speed_HZ": 'Default(Forest)',
                 "KLT14_Fan1Speed_HZ KLT14_Fan2Speed_HZ": 'Default(Forest)',
                 }


def upload(request):
    global csv
    global export
    if request.method == "POST":
        print("data upload to backe-end")

        file = request.FILES["myFile"]
        form_dict = dict(six.iterlists(request.POST))
        print(form_dict['dim_select'][0])

        csv = pd.read_excel(file)

        if csv is not None:
            enable = True

        col = csv.columns.values.tolist()
        col.remove('timestamp')
        sensor = col[0]
        # csv['timestamp'] = pd.to_datetime(csv['timestamp'])
        print(col)

        print("Data rendering...")

        if len(col) == 1:
            if sensor not in default_sensor:
                default_dict = {'default_algo': "", }
            # return JsonResponse({"error": "input data type not match! Unitvariate: 'KLT12_flowRate1 (l/min)', "
            #                               "'IT Power Consumption (W)', 'Outside Temperature (°C)',"
            #                               "'KLT11_pumpSpeed_p1 (Hz)', 'KLT11_Fan1Speed_HZ (Hz)',"
            #                               "'KLT13_inletTempBeforeHydraulicGate (°C)', 'KLT14_pumpSpeed_p1', "
            #                               "'wetBulb', 'KLT14_Fan1Speed_HZ' "
            #                               "Multivariate:'KLT14_pumpSpeed_p1'+'KLT14_pumpSpeed_p2',"
            #                               "'KLT14_Fan1Speed_HZ'+'KLT14_Fan2Speed_HZ' "},
            #                     status=400)
            else:
                default_dict = {'default_algo': default[sensor], }
        else:
            if sensor + " " + col[1] not in default_multi_sensor:
                default_dict = {'default_algo': "", }
            else:
                default_dict = {'default_algo': default_multi[sensor + " " + col[1]], }

        if form_dict['dim_select'][0] == 'Multi':
            if len(col) == 1:
                return JsonResponse({"error": "Input data is not multivariate"},
                                    status=400)
            if len(col) > 2:
                return JsonResponse({
                    "error": "only accept Two-dimensional Multivariate like:'KLT14_pumpSpeed_p1'+'KLT14_pumpSpeed_p2','KLT14_Fan1Speed_HZ'+'KLT14_Fan2Speed_HZ'"},
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
            if len(col) > 1:
                return JsonResponse({"error": "Input data is not unitvariate"},
                                    status=400)
            line = draw_line(csv['timestamp'], csv[sensor], sensor)
            csv = csv[[sensor, 'timestamp']]

        print("Data rendering finish")

        bar_total_trend = json.loads(line.dump_options())
        export = line  # export pdf

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
            # 'default_algo': default[sensor],
        }
        context.update(default_dict)

        print("Data will show in a while")
        return HttpResponse(json.dumps(context, ensure_ascii=False), content_type="application/json charset=utf-8")


def query(request):
    global pd_data
    global csv

    global export1
    global export2
    global export3

    global export4
    global export5
    global export6
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

    # csv['timestamp'] = pd.to_datetime(csv['timestamp'])

    algo = ['Forest', 'Hbos', 'Cblof']

    print("Request arrives at the backend")

    if 'ALGO_select' in form_dict:
        if len(col) == 1:
            csv = csv[[sensor, 'timestamp']]
            if form_dict['ALGO_select'][0] == 'Lstm':
                if sensor not in default_sensor:
                    return JsonResponse({"error": "no match lstm model"},
                                        status=400)
                pd_data = lstm_detection(csv, contamination=0.01)
            elif form_dict['ALGO_select'][0] in algo:
                pd_data = forest_detection(csv, form_dict['ALGO_select'][0], contamination=0.01)
            else:
                if re.findall(r'[(](.*?)[)]', default[sensor])[0] != "LSTM":
                    str = re.findall(r'[(](.*?)[)]', default[sensor])[0]
                    pd_data = forest_detection(csv, str, contamination=0.01)
                else:
                    if sensor not in default_sensor:
                        return JsonResponse({"error": "no match lstm model"},
                                            status=400)
                    pd_data = lstm_detection(csv, contamination=0.01)
                    print(default[sensor])

            print("Data rendering...")
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
                if sensor + " " + col[1] not in default_multi_sensor:
                    return JsonResponse({"error": "no match lstm model"},
                                        status=400)
                pd_data = multi_lstm_detection(csv, contamination=0.01)
            elif form_dict['ALGO_select'][0] in algo:
                pd_data = forest_detection(csv, form_dict['ALGO_select'][0], contamination=0.01)
            else:
                if re.findall(r'[(](.*?)[)]', default_multi[sensor + " " + col[1]])[0] != "LSTM":
                    str = re.findall(r'[(](.*?)[)]', default_multi[sensor + " " + col[1]])[0]
                    pd_data = forest_detection(csv, str, contamination=0.01)
                else:
                    if sensor + " " + col[1] not in default_multi_sensor:
                        return JsonResponse({"error": "no match lstm model"},
                                            status=400)
                    pd_data = multi_lstm_detection(csv, contamination=0.01)
                    print(default_multi[sensor + " " + col[1]])

            print("Data rendering...")
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
        print("Data rendering finish")

        bar_total_trend = json.loads(line.dump_options())
        bar_total_trend1 = json.loads(line1.dump_options())
        bar_total_trend2 = json.loads(line2.dump_options())
        export1 = line
        export2 = line1
        export3 = line2

        # export = pd_data[['original', 'timestamp']]
        # export1 = pd_data
        # export2 = pd_data[[sensor, 'timestamp']]

        if len(col) == 1:
            csv = pd_data[[sensor, 'timestamp']]
        if len(col) == 2:
            csv = pd_data[[col[0], col[1], 'timestamp']]

        print("Data will show in a while")

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

        print("Data rendering...")

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

        export4 = line
        export5 = line1
        export6 = line2

        print("Data rendering finish")

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
        print("Data will show in a while")

    return HttpResponse(json.dumps(context, ensure_ascii=False), content_type="application/json charset=utf-8")


output_path = ""


def export(request):
    global output_path
    form_dict = dict(six.iterlists(request.GET))
    print(form_dict)
    print(form_dict['format_select'][0])
    print(form_dict['export_select'][0])

    export_collection = {
        "export": export,
        "export1": export1,
        "export2": export2,
        "export3": export3,
        "export4": export4,
        "export5": export5,
        "export6": export6,
    }

    export_select = export_collection[form_dict['export_select'][0]]

    export_select.set_global_opts(
        tooltip_opts=opts.TooltipOpts(is_show=False),
    )
    export_select.render("echart.html")

    output_path = "echart" + "." + form_dict['format_select'][0]

    if form_dict['format_select'][0] != "html":
        make_snapshot(snapshot, "echart.html", output_path)

    # form_dict = dict(six.iterlists(request.POST))
    # print(form_dict)
    # print(form_dict['imgBase64:'][0].split(',')[1])
    #
    # strs = form_dict['imgBase64:'][0].split(',')[1]
    # img = base64.b64decode(strs)
    #
    # file = open('test.jpg', 'wb')
    # file.write(img)
    # file.close()
    #
    # image = Image.open('test.jpg')
    #
    # # converting into chunks using img2pdf
    # pdf_bytes = img2pdf.convert(image.filename, dpi=600)
    #
    # # opening or creating pdf file
    # file = open('test1.pdf', "wb")
    #
    # # writing pdf files with chunks
    # file.write(pdf_bytes)
    #
    # # closing image file
    # image.close()
    #
    # # closing pdf file
    # file.close()

    # response = export_pdf(export)

    # export.set_global_opts(
    #     tooltip_opts=opts.TooltipOpts(is_show=False),
    # )
    #
    # html = export.render("test.html")
    # # result = io.BytesIO()
    #
    # pdfkit.from_file('test.html', 'test.pdf')
    #
    # file_path = "test.pdf"
    # file_name = "test.pdf"
    # file = open(file_path, 'rb')
    # response = FileResponse(file)
    # response['Content-Type'] = 'application/octet-stream'
    # response['Content-Disposition'] = "attachment; filename*=UTF-8''{}".format(file_name)
    return HttpResponse("Here's the Web page.")


def export_pdf(request):
    # export.set_global_opts(
    #     tooltip_opts=opts.TooltipOpts(is_show=False),
    # )

    # html = export.render("echart.html")
    # # result = io.BytesIO()
    #
    # pdfkit.from_file('echart.html', 'echart.pdf')

    file_path = output_path
    file_name = output_path
    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment; filename*=UTF-8''{}".format(file_name)
    return response

    # pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)


# def export1(request):
#     response = export_pdf(export1)
#     return response
#
#
# def export2(request):
#     export2.render("test.html")
#
#     make_snapshot(snapshot, "test.html", "test.pdf")
#     response = export_pdf(export2)
#     return response
#
#
# def export3(request):
#     response = export_pdf(export3)
#     return response
#
#
# def export4(request):
#     response = export_pdf(export4)
#     return response
#
#
# def export5(request):
#     response = export_pdf(export5)
#     return response
#
#
# def export6(request):
#     response = export_pdf(export6)
#     return response
