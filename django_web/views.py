from django.shortcuts import render, HttpResponse
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
    global csv
    if request.method == "POST":
        file = request.FILES["myFile"]
        csv = pd.read_excel(file)
        print(csv.head())

        table = csv.to_html(
            classes='ui selectable celled table',
            table_id='data'
        )
        context = {

        }
        # col = csv.columns.values.tolist()
        # col.remove('timestamp')
        # sensor = col[0]
        #
        # csv['timestamp'] = pd.to_datetime(csv['timestamp'])
        #
        # line = (
        #     Line()
        #         .add_xaxis(xaxis_data=csv['timestamp'].tolist())
        #         .add_yaxis(
        #         series_name=sensor,
        #         y_axis=csv[sensor].tolist(),
        #         is_connect_nones=False,
        #     )
        #         .set_global_opts(
        #
        #         tooltip_opts=opts.TooltipOpts(is_show=False),
        #         yaxis_opts=opts.AxisOpts(
        #             splitline_opts=opts.SplitLineOpts(is_show=True),
        #         )
        #     )
        #
        # )
        #
        # bar_total_trend = json.loads(line.dump_options())
        #
        # context = {
        #     'data': table,
        #     'bar_total_trend': bar_total_trend
        # }
        return render(request, "display.html", context)
        # return HttpResponse(csv.to_html())
    else:
        return render(request, "display.html")


def upload(request):
    return render(request, "fileupload.html")


def query(request):
    global pd_data
    global csv

    global export
    global export1
    global export2
    pd_data = csv

    context = {}
    table = pd_data.to_html(
        classes='ui selectable celled table',
        table_id='data'
    )

    form_dict = dict(six.iterlists(request.GET))

    col = csv.columns.values.tolist()
    col.remove('timestamp')
    sensor = col[0]

    csv['timestamp'] = pd.to_datetime(csv['timestamp'])

    algo = ['Forest', 'Hbos', 'Cblof', 'Pca']

    default = {"Outside Temperature (°C)": 'Forest',
               "KLT11_pumpSpeed_p1 (Hz)": 'Hbos',
               "KLT12_flowRate1 (l/min)": 'Cblof',
               }

    if 'ALGO_select' in form_dict:
        csv = csv[[sensor, 'timestamp']]
        if form_dict['ALGO_select'][0] in algo:
            pd_data = forest_detection(csv, form_dict['ALGO_select'][0], contamination=0.05)
        else:
            pd_data = forest_detection(csv, default[sensor], contamination=0.05)
            print(default[sensor])
        table = pd_data.to_html(
            classes='ui selectable celled table',
            table_id='data'
        )

        line = (
            Line()
                .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                .add_yaxis(
                series_name=sensor,
                y_axis=pd_data['original'].tolist(),
                is_connect_nones=False,
            )
                .set_global_opts(
                toolbox_opts=opts.ToolboxOpts(is_show=True, orient='vertical', pos_left='right',
                                              feature=opts.ToolBoxFeatureOpts(
                                                  save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                                                      background_color='#eee'),
                                                  restore=opts.ToolBoxFeatureRestoreOpts(),
                                                  data_view=opts.ToolBoxFeatureDataViewOpts(),
                                                  data_zoom=opts.ToolBoxFeatureDataZoomOpts(),
                                                  magic_type=opts.ToolBoxFeatureDataViewOpts(),
                                                  brush=opts.ToolBoxFeatureDataZoomOpts(),
                                              )),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                datazoom_opts=opts.DataZoomOpts(),
                yaxis_opts=opts.AxisOpts(
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                )
            )

        )

        outlier_data = pd_data.loc[pd_data['anomaly'] == 1]
        pd_data['cleananomaly'] = np.nan
        for index in outlier_data.index.tolist():
            pd_data.loc[index, 'cleananomaly'] = pd_data.loc[index, 'original']

        line1 = (
            Line()
                .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                .add_yaxis(
                series_name=sensor,
                y_axis=pd_data['original'].tolist(),
                is_connect_nones=False,
            )
                .set_global_opts(
                toolbox_opts=opts.ToolboxOpts(is_show=True, orient='vertical', pos_left='right',
                                              feature=opts.ToolBoxFeatureOpts(
                                                  save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                                                      background_color='#eee'),
                                                  restore=opts.ToolBoxFeatureRestoreOpts(),
                                                  data_view=opts.ToolBoxFeatureDataViewOpts(),
                                                  data_zoom=opts.ToolBoxFeatureDataZoomOpts(),
                                                  magic_type=opts.ToolBoxFeatureDataViewOpts(),
                                                  brush=opts.ToolBoxFeatureDataZoomOpts(),
                                              )),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                datazoom_opts=opts.DataZoomOpts(),
                yaxis_opts=opts.AxisOpts(
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                )
            )

        )

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

        line2 = (
            Line()
                .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                .add_yaxis(
                series_name=sensor,
                y_axis=pd_data[sensor].tolist(),
                is_connect_nones=False,
            )
                .set_global_opts(
                toolbox_opts=opts.ToolboxOpts(is_show=True, orient='vertical', pos_left='right',
                                              feature=opts.ToolBoxFeatureOpts(
                                                  save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                                                      background_color='#eee'),
                                                  restore=opts.ToolBoxFeatureRestoreOpts(),
                                                  data_view=opts.ToolBoxFeatureDataViewOpts(),
                                                  data_zoom=opts.ToolBoxFeatureDataZoomOpts(),
                                                  magic_type=opts.ToolBoxFeatureDataViewOpts(),
                                                  brush=opts.ToolBoxFeatureDataZoomOpts(),
                                              )),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                datazoom_opts=opts.DataZoomOpts(),
                yaxis_opts=opts.AxisOpts(
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                )
            )

        )

        bar_total_trend = json.loads(line.dump_options())
        bar_total_trend1 = json.loads(line1.dump_options())
        bar_total_trend2 = json.loads(line2.dump_options())

        export = pd_data[['original', 'timestamp']]
        export1 = pd_data
        export2 = pd_data[[sensor, 'timestamp']]

        csv = pd_data

        context = {
            'data': table,
            'bar_total_trend': bar_total_trend,
            'bar_total_trend1': bar_total_trend1,
            'bar_total_trend2': bar_total_trend2
        }

    if 'Gap_filling' in form_dict:
        line = (
            Line()
                .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                .add_yaxis(
                series_name=sensor,
                y_axis=pd_data[sensor].tolist(),
                is_connect_nones=False,
            )
                .set_global_opts(
                toolbox_opts=opts.ToolboxOpts(is_show=True, orient='vertical', pos_left='right',
                                              feature=opts.ToolBoxFeatureOpts(
                                                  save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(background_color='#eee'),
                                                  restore=opts.ToolBoxFeatureRestoreOpts(),
                                                  data_view=opts.ToolBoxFeatureDataViewOpts(),
                                                  data_zoom=opts.ToolBoxFeatureDataZoomOpts(),
                                                  magic_type=opts.ToolBoxFeatureDataViewOpts(),
                                                  brush=opts.ToolBoxFeatureDataZoomOpts(),
                                              )),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                datazoom_opts=opts.DataZoomOpts(),
                yaxis_opts=opts.AxisOpts(
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                )
            )

        )
        export = pd_data

        pd_data = gap_filling(csv, form_dict['Gap_filling'][0])
        table = pd_data.to_html(
            classes='ui selectable celled table',
            table_id='data'
        )

        line1 = (
            Line()
                .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                .add_yaxis(
                series_name=sensor,
                y_axis=pd_data[sensor].tolist(),
                is_connect_nones=False,
            )
                .set_global_opts(
                toolbox_opts=opts.ToolboxOpts(is_show=True, orient='vertical', pos_left='right',
                                              feature=opts.ToolBoxFeatureOpts(
                                                  save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(background_color='#eee'),
                                                  restore=opts.ToolBoxFeatureRestoreOpts(),
                                                  data_view=opts.ToolBoxFeatureDataViewOpts(),
                                                  data_zoom=opts.ToolBoxFeatureDataZoomOpts(),
                                                  magic_type=opts.ToolBoxFeatureDataViewOpts(),
                                                  brush=opts.ToolBoxFeatureDataZoomOpts(),
                                              )),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                datazoom_opts=opts.DataZoomOpts(),
                yaxis_opts=opts.AxisOpts(
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                )
            )

        )

        scatter = (
            Line()
                .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                .add_yaxis(
                series_name="filling",
                y_axis=pd_data['filling'].tolist(),
                # symbol_size=5,
                is_connect_nones=False,

            )
                .set_global_opts(
                toolbox_opts=opts.ToolboxOpts(is_show=True, orient='vertical', pos_left='right',
                                              feature=opts.ToolBoxFeatureOpts(
                                                  save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(background_color='#eee'),
                                                  restore=opts.ToolBoxFeatureRestoreOpts(),
                                                  data_view=opts.ToolBoxFeatureDataViewOpts(),
                                                  data_zoom=opts.ToolBoxFeatureDataZoomOpts(),
                                                  magic_type=opts.ToolBoxFeatureDataViewOpts(),
                                                  brush=opts.ToolBoxFeatureDataZoomOpts(),
                                              )),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                datazoom_opts=opts.DataZoomOpts(),
                yaxis_opts=opts.AxisOpts(
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                )
            )

        )
        line1.overlap(scatter)

        line2 = (
            Line()
                .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
                .add_yaxis(
                series_name=sensor,
                y_axis=pd_data[sensor].tolist(),
                is_connect_nones=False,
            )
                .set_global_opts(
                toolbox_opts=opts.ToolboxOpts(is_show=True, orient='vertical', pos_left='right',
                                              feature=opts.ToolBoxFeatureOpts(
                                                  save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(),
                                                  restore=opts.ToolBoxFeatureRestoreOpts(),
                                                  data_view=opts.ToolBoxFeatureDataViewOpts(),
                                                  data_zoom=opts.ToolBoxFeatureDataZoomOpts(),
                                                  magic_type=opts.ToolBoxFeatureDataViewOpts(),
                                                  brush=opts.ToolBoxFeatureDataZoomOpts(),
                                              )),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                datazoom_opts=opts.DataZoomOpts(),
                yaxis_opts=opts.AxisOpts(
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                )
            )

        )
        bar_total_trend = json.loads(line.dump_options())
        bar_total_trend1 = json.loads(line1.dump_options())
        bar_total_trend2 = json.loads(line2.dump_options())

        export1 = pd_data
        export2 = pd_data

        csv = pd_data

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
