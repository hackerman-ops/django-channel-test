

import subprocess
from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import threading
import json

from django_redis import get_redis_connection
cache = get_redis_connection("default")

key = "subprocess"

cache.set(key,2)
if not cache.get(key):
    cache.set(key,1)
else:
    print(cache.get(key))



class tailflog(AsyncWebsocketConsumer):

    async  def connect(self):
        await self.accept()

        self.p = None
        processnum = cache.get(key)
        if int(processnum) == 0:
            await self.send("fuck you")
            await self.close()


    def monitor(self):
        while self.p.poll() is None:
            output = self.p.stdout.readlines(10)
            for line in output:
                line = line.strip()
                line = line.decode("utf-8")
                async_to_sync(self.send)(line)


    async def disconnect(self, code):
        if self.p:
            await sync_to_async(self.p.terminate)()
        await self.close()

    async  def receive(self, text_data=None, bytes_data=None):

        text = json.loads(text_data)

        terminal = text.get("terminal")
        print(terminal)
        if terminal:

            if self.p:
                self.p.terminate()
                self.p.wait(0.3)
                self.p = None
                with cache.lock(key + "oh"):
                    cache.incr(key)
            await self.send("日志查询结束")
            print("结束了吗")



        else:
            print(terminal)
            namespace = text["namespace"]
            clusteruuid= text["clusteruuid"]
            pod = text["pod"]
            container = text["container"]

            with cache.lock(key + "oh"):
                self.p = subprocess.Popen(["journalctl", "-xef"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True,
                                          shell=False)
                cache.decr(key)
            t = threading.Thread(target=self.monitor)
            t.daemon = True
            t.start()
            print(cache.get(key))