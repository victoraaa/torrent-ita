import sys
# import thread

from client import listen


def main():

    tracker_host = sys.argv[1]
    tracker_host = tracker_host.split(':')
    tracker_ip = tracker_host[0]
    tracker_port = int(tracker_host[1])

    print 'Tracker: ' + tracker_ip + ':' + str(tracker_port)

    # client_upload.TRACKER_HOST = tracker_ip
    # client_upload.TRACKER_PORT = tracker_port

    # thread.start_new_thread(client_upload.run)


def run_uploader():
    while True:
        listen(50011)


if __name__ == "__main__":
    run_uploader()
