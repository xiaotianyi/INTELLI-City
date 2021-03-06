# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import reply
import receive
import web
import json
from wenpl.divide import showReply


class Handle(object):
    def POST(self):
        '''
        给微信提供服务
        '''
        try:
            webData = web.data()
            print "\n\n\nHandle Post webdata is ", webData   #后台打日志
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
                replyMsg = reply.VoiceMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment

    def GET(self):
        '''
        给网页端的服务
        '''

        try:
            webdata=web.input()
            print webdata
            result=showReply(webdata.query)
            print result
            web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
            web.header('Access-Control-Allow-Origin','*')
            web.header('Access-Control-Allow-Credentials','true')
            # web.header('content-type','text/json')
            return json.dumps({'response':result})
        except:
            return 0