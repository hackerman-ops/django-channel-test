

import subprocess
from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import threading



class tailflog(AsyncWebsocketConsumer):

    async  def connect(self):
        await self.accept()
        # self.p = Bash(["journalctl", "-xef"])
        args_dict = self.scope["url_route"]["kwargs"]

        print(args_dict)
        self.cmd = ["journalctl", "-xef"]
        self.p = subprocess.Popen(self.cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,start_new_session=True,shell=False)
        print(self.p)
        t = threading.Thread(target=self.monitor)
        t.daemon = True
        t.start()


    def monitor(self):
        while self.p.poll() is None:
            output = self.p.stdout.readlines(10)
            for line in output:
                line = line.strip()
                line = line.decode("utf-8")
                async_to_sync(self.send)(line)
        async_to_sync(self.close)()

    async def disconnect(self, code):
        await sync_to_async(self.p.terminate())()

    async  def receive(self, text_data=None, bytes_data=None):
        return
