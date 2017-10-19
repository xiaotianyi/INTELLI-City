# -*- coding: utf-8 -*-
# filename: handle.py

import json
import web
# import hashlib

import receive
import reply
from server.service.reply_show import show_reply


class Handle(object):
    def POST(self):
        try:
            webData = web.data()
            recMsg = receive.parse_xml(webData)

            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = recMsg.Content
                print "Handle Post webData(text) is ", content  # 后台打日志

                replyMsg = reply.LocationMsg(toUser, fromUser, content)
                print "Reply Message", replyMsg

                return replyMsg.send()

            elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'voice':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = recMsg.Content
                print "Handle Post webData(voice) is ", content  # 后台打日志

                replyMsg = reply.VoiceMsg(toUser, fromUser, content)
                print "Reply Message", replyMsg

                return replyMsg.send()

            else:
                print "INPUT TYPE ERROR: 目前只支持处理文字/语音，其它暂不处理"
                return "success"

        except Exception, Argment:
            return Argment


    # TODO 理解一下get方法的目的
    def GET(self):
        try:
            web_data = web.input()
            print "Handle GET webData is ", receive.parse_xml(web_data)  # 后台打日志

            result = show_reply(web_data.query)
            print "Reply Message", result

            web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Credentials', 'true')
            # web.header('content-type','text/json')
            return json.dumps({'response': result})
        except:
            return 0
