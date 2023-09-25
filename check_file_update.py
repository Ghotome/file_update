import os
import sys
from datetime import datetime
import pymsteams
from watchdog.observers import Observer
import watchdog.events

os.environ["PATH_TO_FILE"] = sys.argv[1]
os.environ["WEBHOOK_URL"] = sys.argv[2]


def send_notification(body: dict):
    webhook_url = os.environ.get('WEBHOOK_URL')
    send_message = pymsteams.connectorcard(webhook_url)
    send_message.text(f'>[*Event path:* {body["event_path"]}]   \n'
                      f'>[*Event type:* {body["event_type"]}]   \n'
                      f'>[*Event time:* {body["timestamp"]}]   \n')
    send_message.send()


class CheckFileChanges(watchdog.events.PatternMatchingEventHandler):

    def on_modified(self, event):
        print(f'>[-- Event time: {datetime.now()}]\n'
              f' >[-- Event type: {event.event_type}]\n'
              f' >[-- Event path: {event.src_path}]\n')
        result = {'event_type': event.event_type, 'event_path': event.src_path,
                  'timestamp': datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")}
        send_notification(result)
        return None


if __name__ == '__main__':
    event_handler = CheckFileChanges()
    observer = Observer()
    observer.schedule(event_handler, path=os.environ.get('PATH_TO_FILE'), recursive=False)
    observer.start()
    observer.join()
