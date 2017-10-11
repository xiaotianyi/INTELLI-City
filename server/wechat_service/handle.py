# -*- coding: utf-8 -*-
# filename: handle.py
import json
import hashlib
import web

from wenpl.divide import showReply

import receive
import reply


class Handle(object):
    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is ", webData  # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = recMsg.Content
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                print replyMsg
                return replyMsg.send()
            elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'voice':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = recMsg.Content
                print "show vioce text", content
                replyMsg = reply.VoiceMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment

    def GET(self):
        try:
            webdata = web.input()
            print webdata
            result = showReply(webdata.query)
            print result
            web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Credentials', 'true')
            # web.header('content-type','text/json')
            return json.dumps({'response': result})
        except:
            return 0
