from multiprocessing import Process,Pipe
from bot.bot import run
from pub_sub.pub_sub import PubSub

"""
Process 1: Discord bot process
Process 2: Pub/Sub Process

To stop any process related to discord bot 
comment out every line related to process1.

To stop any process related to notifications or pub/sub api
comment out every line related to process2.
"""

if __name__=="__main__":
    discord_conn, pubsub_conn = Pipe()
    process1 = Process(target=run,args=(discord_conn,))
    process2 = Process(target=PubSub,args=(pubsub_conn,))
    process1.start()
    process2.start()
    process1.join()
    process2.join()