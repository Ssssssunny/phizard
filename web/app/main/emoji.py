# -*- coding: utf-8 -*-

"""


created: 2017-05-31

by: Yr
"""


from datetime import *
import datetime
import time
from . import main
from app import db
from ..api_1_0.authentication import auth
from flask import render_template, make_response, redirect, url_for, request, current_app, flash, jsonify
from flask_login import current_user, login_required
from ..models import User, Result
from phizard.utils.daily_statistics import statistics


@main.route('/pattern', methods=['POST'])
@auth.login_required
def get_emoji():
    """
    存储传过来的表情信息进mysql

    :return:
    """
    params = request.get_json()

    user_id = params['employe_id']

    emotion = str(params['emotion_score'])
    time = params['time']
    status = params['status']  # 0失败   1成功

    if status == 0:  # 失败的任务就不需要存
        return 0

    result = Result(user_id=user_id, emoji=emotion, taketime=time)
    try:
        db.session.add(result)
        db.session.commit()
    except Exception:
        return jsonify({'code': 201, 'message': 'save failed', 'data': []})

    return jsonify({'code': 200, 'message': 'save successful', 'data': []})


@main.route('/personal_pattern', methods=['POST'])
@auth.login_required
def personal_pattern():
    """
    传入employ_id 和一个时间范围(start ~ end);如果没有时间范围，则视为时间范围是当天00:00开始的一整天
    返回该员工在时间范围内的情绪值 (table : result)
    {
        "employ_id": 1,
        "timeline": {
            "start": "2017-06-22 10:12:00",
            "end": "2017-06-23 10:12:00"
        }

    }
    -----------------------------
    {  "2017-06-22": [{ ......},{ ......}]
    }
    :return:
    """

    params = request.get_json()
    print params
    employee_dict = {}
    employee_timeline_lists = {}  # 雇员和时间组成的新的list

    user_id = params['employ_id']
    result = Result.query.filter_by(user_id=user_id).all()  # 获取某雇员所有记录信息

    # 将传进来的时间字符串转格式
    if 'timeline' in params.keys():
        timeline = params['timeline']
        start_limit = timeline['start'][:10] + ' ' + timeline['start'][11:]
        end_limit = timeline['end'][:10] + ' ' + timeline['end'][11:]
        b1 = time.strptime(start_limit, "%Y-%m-%d %H:%M:%S")
        y1, m1, d1 = b1[0:3]
        b2 = time.strptime(end_limit, "%Y-%m-%d %H:%M:%S")
        y2, m2, d2 = b2[0:3]
        new_start_timeline = datetime.datetime(y1, m1, d1)
        new_end_timeline = datetime.datetime(y2, m2, d2)

    # 没有起止时间规定的就以当天为准

    else:
        end_limit = date.today()  # 当前时间的下限
        start_limit = end_limit - datetime.timedelta(days=90)  # 三个月以前的上限
        # datetime.date 格式转字符串拼接时间
        start_limit = str(start_limit) + ' 00:00:00'

        end_limit = str(end_limit) + ' 00:00:00'

        b1 = time.strptime(start_limit, "%Y-%m-%d %H:%M:%S")
        y1, m1, d1 = b1[0:3]
        b2 = time.strptime(end_limit, "%Y-%m-%d %H:%M:%S")
        y2, m2, d2 = b2[0:3]
        new_start_timeline = datetime.datetime(y1, m1, d1)
        new_end_timeline = datetime.datetime(y2, m2, d2+1)

    # 去除符合时间的选项
    for item in result:
        taketime =item.taketime[:10] + ' ' + item.taketime[11:]
        b = time.strptime(taketime, "%Y-%m-%d %H:%M:%S")
        y, m, d = b[0:3]

        if datetime.datetime(y, m, d) > new_start_timeline and datetime.datetime(y, m, d) < new_end_timeline:
            employee_dict[item.id] = item.taketime[:10]
            # employee_timeline_lists.append({'emotion_score': eval(item.emoji), 'time': item.taketime})

    # 将结果组装成最后需要的格式
    if employee_dict != {}:
        for k in employee_dict:
            res = Result.query.filter_by(id=k).first()
            if employee_dict[k] in employee_timeline_lists.keys():
                employee_timeline_lists[employee_dict[k]].append(eval(res.emoji))
            else:
                employee_timeline_lists[employee_dict[k]] = [eval(res.emoji)]
    print employee_timeline_lists
    return jsonify({'code': 200, 'message': 'opearate successful', 'data': employee_timeline_lists})


@main.route('/pattern/<int:id>', methods=['GET', 'POST'])
@login_required
def pattern(id):
    """
    按周为单位，统计x轴坐标点为天的折线图
    :param id:
    :return:
    """
    legend_values = {'sadness': [], 'happiness': [], 'disgust': [], 'anger': [], 'surprise': [], 'fear': [],
                     'neutral': [], 'contempt': []}
    x_data = []
    data = statistics(id)
    print "*" * 30

    print data['date']
    for item in data['date']:
        x_data.append(item[5:10].replace('-', '.'))

    legend_graphs = data['graph']
    legend_lstm = data['lstm-graph']
    legend_arima = data['arima-graph']



    # day_lists = {}
    # today = datetime.datetime.now()
    #
    # all_results = Result.query.filter_by(user_id=id).all()
    # for result in all_results:
    #     date_list = [int(item) for item in result.taketime[:10].split('-')]
    #     day_lists[result.id] = (datetime.datetime(date_list[0], date_list[1], date_list[2]))
    #
    # legend_values = {'sadness':[], 'happiness':[], 'disgust':[], 'anger':[], 'surprise':[], 'fear':[], 'neutral':[], 'contempt':[]}
    # x_data = []
    # compare_list = [i for i in range(1,100)]
    # # 获取当前日期前100天的图像信息
    # for timeline in day_lists:
    #     if (today-day_lists[timeline]).days in compare_list:
    #         this_result = Result.query.filter_by(id=timeline).first()
    #         x_data.append(this_result.taketime[5:10].replace('-', '.'))
    #         for key in legend_values.keys():
    #             legend_values[key].append(eval(this_result.emoji)[key])
    print "=" * 30
    print x_data
    xtest={'x': [float(d) for d in x_data]}
    return render_template('emoji.html', legend=legend_values, xaxis=x_data, xtest=xtest, graphs=legend_graphs, arima=legend_arima, lstm=legend_lstm)
