# -*- coding: utf-8 -*-

from service_call import connect_turing, connect_rest_api


def show_reply():
    response, flag = connect_rest_api()
    reply = show_diff_result(response, flag)
    if reply:
        return
    else:
        return


def show_diff_result(response, flag):
    return response