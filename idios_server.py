# coding:utf-8
import json
import urllib.parse

import tornado
from tornado.web import url
import jionlp as jio
import asyncio
# from flask import jsonify

# import to

# app = Flask(__name__)
# 创建出字典对象
chinese_idioms = jio.chinese_idiom_loader()


def get_idiom(idiom):
    print(f"查询成语: {idiom}")
    try:
        return chinese_idioms[idiom]
    except KeyError as e:
        print(f"查询成语失败 ： {idiom} error: {e}")
        return None


class App(object):

    def __init__(self, port=9000):
        handlers = [
            url(
                '/api/getIdiom',
                GetIdiomHandler
            )
        ]
        self.app = tornado.web.Application(handlers=handlers)
        self.port = port

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        server = tornado.httpserver.HTTPServer(self.app)
        server.listen(self.port)
        print(f"sever running at: http://localhost:{self.port}")
        tornado.ioloop.IOLoop.current().start()


class GetIdiomHandler(tornado.web.RequestHandler):

    async def get(self):
        query = self.request.arguments.get("idiom", "")[0]  # 没有默认为 0
        if isinstance(query, bytes):
            query = query.decode(encoding="utf-8")

        # query = urllib.parse.unquote(query)
        # print("")

        result = get_idiom(query)
        if result is None:
            result = {
                "hasData":False
            }
        else:
            result['hasData'] = True
        self.write(json.dumps(result))
# @app.route('/api/getIdiom', methods=['GET'])
# def get_data():
#     print(request.args)
#     text_param = request.args.get('idiom',default='', type=str)
#     # if isinstance(text_param,bytes):
#
#     # text_param = text_param.encode(encoding="utf-8").decode(encoding="utf-8")
#     # text_param = urllib.parse.unquote(text_param,encoding="utf-8")
#     result = get_idiom(text_param)
#     if result  is None:
#         result = {
#             "hasData":False
#         }
#     return jsonify(result)
#
#
if __name__ == '__main__':
    App().run()
