from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
import pandas as pd
import json
from pyecharts.charts import Line
import pyecharts.options as opts
from .detection import *

try:
    import six  # for modern Django
except ImportError:
    from django.utils import six  # for legacy Django


try:
    from io import BytesIO as IO # for modern python
except ImportError:
    from io import StringIO as IO # for legacy python
import datetime


csv = pd.DataFrame()
pd_data = pd.DataFrame()


def home(request):
    global csv
    if request.method == "POST":
        file = request.FILES["myFile"]
        csv = pd.read_excel(file)
        print(csv.head())
        # arr = csv['Outside Temperature (°C)'].median()
        # sumation = sum(arr)
        # print(arr)

        table = csv.to_html(
            classes='ui selectable celled table',
            table_id='data'
        )
        context = {

        }
        return render(request, "display.html", context)
        # return HttpResponse(csv.to_html())
    else:
        return render(request, "index.html")


def upload(request):
    return render(request, "fileupload.html")


def query(request):
    global pd_data
    pd_data = csv
    table = pd_data.to_html(
        classes='ui selectable celled table',
        table_id='data'
    )

    form_dict = dict(six.iterlists(request.GET))

    col = csv.columns.values.tolist()
    col.remove('timestamp')
    sensor = col[0]

    csv['timestamp'] = pd.to_datetime(csv['timestamp'])

    if 'ALGO_select' in form_dict:
        if form_dict['ALGO_select'][0] == 'Forest':
            pd_data = forest_detection(csv, contamination=0.05)
            table = pd_data.to_html(
                classes='ui selectable celled table',
                table_id='data'
            )

    if 'Gap_filling' in form_dict:
        pd_data = gap_filling(csv)
        table = pd_data.to_html(
            classes='ui selectable celled table',
            table_id='data'
        )

    line = (
        Line()
            .add_xaxis(xaxis_data=pd_data['timestamp'].tolist())
            .add_yaxis(
            series_name=sensor,
            y_axis=pd_data[sensor].tolist(),
            is_connect_nones=False,
        )
            .set_global_opts(

            tooltip_opts=opts.TooltipOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                splitline_opts=opts.SplitLineOpts(is_show=True),
            )
        )

    )
    print(form_dict)

    bar_total_trend = json.loads(line.dump_options())

    context = {
        'data': table,
        'bar_total_trend': bar_total_trend
    }
    return HttpResponse(json.dumps(context, ensure_ascii=False), content_type="application/json charset=utf-8")


def export(request):
    form_dict = dict(six.iterlists(request.GET))
    print(type)

    df = pd_data

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
