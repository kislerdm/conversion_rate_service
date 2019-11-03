# Dmitry Kisler © 2019
# admin@dkisler.com

import os
import sys
import logging
import requests
import inspect
import time


class getLogger:
    """Logger class to log and interrupt the process on the error"""

    def __init__(self,
                 logger="logs",
                 webhook_url=None,
                 kill=False):
        """Instantiate logger

            Args: 
                logger: logger name
                webhook_url: url to push webhook
                kill: flag to terminate the process on the error
        """
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s.%(msecs)03d [%(levelname)-5s] [%(name)-12s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        
        self.logger_name = logger
        self.logs = logging.getLogger(self.logger_name)
        self.kill = kill
        self.webhook_url = webhook_url

    @classmethod
    def get_line(cls):
        """Returns the current line number"""
        return inspect.currentframe().f_back.f_lineno

    def _send_webhook(self,
                      msg: str,
                      is_error=True):
        """Function to push a webhook to slack channel

            Args:
                msg: log message
                is_error: flag to signal if message is the error message
        """
        if self.webhook_url is None:
            return

        color = "#ff003a"
        level = "ERROR"
        if not is_error:
            color = "#36a64f"
            level = "INFO"

        body = {
            "attachments": [
                {
                    "color": color,
                    "author_name": self.logger_name,
                    "title": level,
                    "text": msg,
                    "ts": int(time.time())
                }
            ]
        }

        try:
            res = requests.post(url=self.webhook_url,
                                headers={"Content-type": "application/json"},
                                json=body)
            if res.status_code > 200:
                self.logs.error("Cannot push webhook using provided URL")
                self.webhook_url = None
        except Exception as ex:
            self.logs.error("Cannot push webhook using provided URL")
            self.webhook_url = None

    def send(self,
             msg: str,
             lineno=None,
             kill=None,
             is_error=True,
             webhook=False):
        """Send a message into the logging output

            Args:
                msg: log message
                lineno: line number in the code where log send was triggered
                kill: flag to terminate the process on the error
                is_error: flag to signal if message is the error message
                webhook: flag to post message as the webhook post request
        """
        if lineno:
            msg = f"[line: {lineno}] {msg}"
        if is_error:
            self.logs.error(msg)
            self._send_webhook(msg,
                               is_error=is_error)
            if (kill if kill is not None else self.kill):
                sys.exit(1)
        else:
            self.logs.info(msg)
            if webhook:
                self._send_webhook(msg,
                                   is_error=is_error)
            if kill:
                sys.exit(0)
