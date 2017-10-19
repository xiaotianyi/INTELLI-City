# -*- coding: utf-8 -*-
import json

from service_call import connect_rest_api


def show_reply():
    response, flag = connect_rest_api()
    reply = show_diff_result(response, flag)
    if reply:
        return
    else:
        return


def show_diff_result(result, types):
    if types[0] == "查询 全部 工单":
        return get_order_relations(result)

    if types[0] == "查询 全部 设备 类型":
        return get_device_type(result)

    if types[0] == "查询 全部 设备":
        return monitoring_manage_get_devices(result)

    if types[0] == "查询 全部 采集点":
        return get_point_types(result)

    if types[0] == "查询 全部 应急 演练 预案":
        return get_drill_plan(result)

    if types[0] == "查询 局站 名称":
        return get_stations_name(result)

    if types[0] == "查询 全部 操作 日志":
        return get_operation_logs(result)

    if types[0] == "查询 position 报警 数量":
        return get_children_with_warning_count(result)

    if types[0] == "查询 position 员工":
        return get_staff_from_district(result)

    if types[0] == "查询 people 操作 日志 历史" or types[0] == "查询 people time 操作 日志 历史":
        return get_user_operation_log(result)

    if types[0] == "查询 people 历史 工单" or types[0] == "查询 people time 历史 工单":
        return get_work_orders(result)

    if types[0] == "查询 position 报警" or types[0] == "查询 position time 报警":
        return get_warning(result)

    if types[0] == "查询 position 设备":
        return get_devices_by_parents_name(result)

    if types[0] == "查询 people 通知":
        return get_received_messages(result)

    if types[0] == "查询 全部 工具包":
        return get_public_toolkit(result)

    if types[0] == "管理 注册 登录 用户":
        return result


def get_public_toolkit(result):
    format_str = ""
    res = result['response']
    for key in res:
        format_str += key + ":\n"
        count = 1
        for item in res[key]:
            format_str += str(count) + ":" + item["name"] + "\n"
            # format_str += "简介: " + item["description"] + "\n"
            count += 1
        format_str += "\n"
    # print "inn done", r_str
    return format_str


def get_order_relations(result):
    format_str = ""
    for x in result['message']:
        format_str += "设备编号:"
        format_str += x['Device']
        format_str += '\n'
        format_str += "局站名称:"r
        format_str += x['Station']
        format_str += '\n'
        format_str += '工作人员:'
        format_str += '\n'
        for worker in x['Worker_Id']:
            format_str += worker['name']
            format_str += '\n工号:'
            format_str += worker['id']
            format_str += '\n'
        format_str += '\n\n'
    return format_str


def get_device_type(result):
    format_str = ""
    for x in result['response'].values():
        format_str += x
        format_str += '\n'
    return format_str


def monitoring_manage_get_devices(result):
    format_str = ""
    for x in result['response']:
        format_str += "设备ID:"
        format_str += x['ID']
        format_str += '\n'
        format_str += "设备类型:"
        format_str += x['device_type']
        format_str += '\n'
        format_str += "设备名称:"
        format_str += x['name']
        format_str += '\n'
        format_str += "设备位置:"
        for y in x['parents'].values():
            format_str += y
            format_str += " "
        format_str += '\n\n'
    return format_str


def get_point_types(result):
    format_str = ""
    for x in result['response']:
        format_str += "采集点名称:"
        format_str += x['name']
        format_str += '\n'
    return format_str


def get_drill_plan(result):
    format_str = ""
    for x in result['message']:
        for y in x['plans']:
            url = "/preplans/get_plan_by_id?plan_id=" + y
            plan = getResult(url)
            plan = json.loads(plan)
            # print plan['message']
            insidex = plan['message']
            # print insidex
            format_str += "演练名称:"
            format_str += insidex['name']
            format_str += "\n演练时间:"
            format_str += insidex['time']
            format_str += "\n演练地点:"
            format_str += insidex['location']
            format_str += "\n实施人员:"
            format_str += insidex['operator']
            format_str += "\n联系电话:"
            format_str += insidex['phone']
            format_str += "\n参演人员:"
            format_str += insidex['operator']
            format_str += "\n演练步骤:"
            for step in range(len(insidex['description'])):
                format_str += "\n步骤" + str(step + 1) + ':'
                format_str += insidex['description'][step]

    return format_str


def get_stations_name(result):
    format_str = ""
    for x in result['response']:
        format_str += x
        format_str += '\n'
    return format_str


def get_operation_logs(result):
    format_str = ""
    for x in result['response']:
        format_str += "日期:"
        format_str += x['timestamp']
        format_str += '\n'
        format_str += "处理人:"
        format_str += x['operator']
        format_str += '\n'
        format_str += "操作信息:"
        if x['operations'] != []:
            format_str += x['operations'][0]['from'][0]['area'] + '-' + x['operations'][0]['from'][0]['station'] + '-' + \
                    x['operations'][0]['from'][0]['device_name'] + '-' + x['operations'][0]['from'][0]['title']
        format_str += '\n'
        format_str += "操作结果:"
        format_str += x['is_all_success']
        format_str += '\n\n'
    return format_str


def get_devices_by_parents_name(result):
    format_str = "设备名称:\n"
    for x in result['response']:
        format_str += x['name']
        format_str += '\n'
    return format_str


def get_children_with_warning_count(result):
    format_str = ""
    for x in result['response']:
        format_str += '名字:'
        format_str += x['name']
        format_str += '\n一般报警:'
        format_str += str(x['warning_counts'][2])
        format_str += '\n紧急报警:'
        format_str += str(x['warning_counts'][1])
        format_str += '\n严重报警:'
        format_str += str(x['warning_counts'][0])
        format_str += "\n\n"

    return format_str


def get_staff_from_district(result):
    format_str = ""
    for x in result["response"]:
        format_str += "姓名:"
        format_str += x['name']
        format_str += "\n性别:"
        format_str += x['gender']
        format_str += "\n电话:"
        format_str += x['cellphone']
        format_str += "\n电邮:"
        format_str += x['email']
        format_str += "\n公司:"
        format_str += x['company']
        format_str += "\n类型:"
        format_str += x['type']
        format_str += "\n区域:"
        format_str += x['district']['name']
        format_str += "\n资格认证:"
        for y in x['qualification']:
            format_str += y['name']
    return format_str


def get_received_messages(result):
    format_str = ""
    for x in result['response']:
        format_str += "发件人:"
        format_str += x['sender']
        format_str += '\n'
        format_str += "时间:"
        format_str += x['timestamp']
        format_str += '\n'
        format_str += "标题:"
        format_str += x['title']
        format_str += '\n'
        format_str += "内容:"
        format_str += x['content']
        format_str += '\n\n'
    return format_str


def get_user_operation_log(result):
    format_str = ""
    for x in result['response']:
        format_str += "操作人员:"
        for y in x['foreign1']:
            format_str += y['name']
            format_str += " "
        format_str += "\n权限:"
        for y in x['foreign2']:
            format_str += y['name']
            format_str += " "
        format_str += '\n操作内容:'
        format_str += x['operation']
        format_str += '\n操作时间:'
        format_str += x['timestamp']
        format_str += '\n\n'
    return format_str


def get_work_orders(result):
    status = {'0': '已发送', '1': '已确认', '2': '已处理', '3': '已完成'}
    format_str = ""
    for x in result['response']:
        format_str += "工单编号:"
        format_str += str(x['ID'])
        format_str += "\n处理人:"
        format_str += x['worker_name']
        format_str += "\n地点:"
        format_str = format_str + x['event_detail']['Local_Network'] + "-" + x['event_detail']['Area'] + '-' + x['event_detail'][
            'Local_Network'] + x['event_detail']['Station']
        format_str += "\n产生时间:"
        format_str += x['event_detail']['Start_Time']
        format_str += "\n工单内容:"
        format_str = format_str + x['event_detail']['Device'] + '-' + x['event_detail']['Point'] + '-' + x['event_detail'][
            'Warning_Type']
        format_str += "\n当前状态:"
        format_str += status[str(x['status']['current_status'])]
        format_str += '\n\n'
    return format_str


def get_point_info_with_real_time(result):
    format_str = ""
    x = result['response']
    format_str += "区域:"
    format_str += x['point']['area']
    format_str += "\n"
    format_str += "设备:"
    format_str += x['point']['device_name']
    format_str += "\n"
    format_str += "监测点:"
    format_str += x['point']['name']
    format_str += "\n"
    format_str += "时间:"
    format_str += x['point_real_time']['time']
    format_str += "\n"
    format_str += "数值:"
    format_str = format_str + str(x['point_real_time']['value']) + x['point']['units']
    format_str += "\n"
    format_str += "状态:"
    format_str += x['point']['warning_type']
    format_str += "\n"
    format_str += "\n\n"

    return format_str


def get_warning(result):
    format_str = ""
    c = 0
    for x in result['response']:
        c += 1
        format_str += "位置:"
        format_str = format_str + x['Local_Network'] + x['Area'] + '-' + x['Station'] + '-' + x['Device']
        format_str += '\n'
        format_str += "监控点:"
        format_str += x['Point']
        format_str += '\n'
        format_str += "数值:"
        format_str = format_str + str(x['Value']) + x['Units']
        format_str += '\n'
        format_str += "开始时间:"
        format_str += x['Start_Time']
        format_str += '\n'
        format_str += "类型:"
        format_str += x['Warning_Type']
        format_str += '\n'
        format_str += "状态:"
        format_str += x['Status']
        format_str += '\n\n'
        if c >= 8:
            break

    return format_str
