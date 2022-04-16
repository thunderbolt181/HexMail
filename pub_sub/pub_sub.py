from google.cloud import pubsub_v1
import os
import json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "pub_sub\pub_sub_token.json"

subscription_id = "Pub-Sub_gmail_API_tesing-sub"
project_id = "gmail-api-testing-331909"

class PubSub:
    """
        This calls Google cloud's PubSub instance as a Subscriber
            to receive push notification.
    """
    def __init__(self,conn) -> None:
        self.conn = conn
        self.subscriber_func()

    def subscriber_func(self):
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(project_id, subscription_id)
        flow_control = pubsub_v1.types.FlowControl(max_messages=10)
        streaming_pull_future = subscriber.subscribe(
            subscription_path, callback=self.callback, flow_control=flow_control
        )
        print(f"Listening for messages on {subscription_path}..\n")
        with subscriber:
            try:
                streaming_pull_future.result()
            except KeyboardInterrupt:
                streaming_pull_future.cancel()  # Trigger the shutdown.
                streaming_pull_future.result()  # Block until the shutdown is complete.
    
    def callback(self,message: pubsub_v1.subscriber.message.Message) -> None:
        message.ack()
        msg = json.loads(message.data.decode("utf-8"))
        self.conn.send(msg)

if __name__=="__main__":
    obj=PubSub(True)