# -*- coding:utf-8 -*-
"""
ipc.py
Inter-process Communication management module.
Dashadower
"""
import os, multiprocessing

MSGTYPE_START = "start"
MSGTYPE_STOP = "stop"
MSGTYPE_KILL = "kill"
MSGTYPE_LOG_DEBUG = "log_debug"
MSGTYPE_LOG_EXCEPTION = "log_exception"
MSGTYPE_INFO_FINISHED = "bot_finished"

class Message:
    def __init__(self, issuer, message_type, message_data, message_params=None):
        """
        Message Object
        :param issuer: Creator PID
        :param message_type: MSGTYPE_X message type
        :param message_data: message data. usage varies with type
        :param message_params: optional additional params if needed
        """
        self.issuer = issuer
        self.message_type = message_type
        self.message_data = message_data
        self.message_params = message_params

class CommunicationHandler:
    """
    This class hosts functions and protocols to help communicate between processes using queues.
    """
    def __init__(self, input_queue=None, output_queue=None):
        """
        Communication relies on two one-way queues to send message objects between processes.
        :param input_queue: multiprocessing.Queue object where the handler will be listening. Will be created if not passed.
        :param output_queue: multiprocessing.Queue object where the handler will be sending message. Will be created if not passed.
        :return :None
        """
        self.input_queue = input_queue if input_queue else multiprocessing.Queue()
        self.output_queue = output_queue if output_queue else multiprocessing.Queue()
        self.pid = os.getpid()

    def reconfigure_queues(self, input_queue=None, output_queue=None):
        """
        Change queue or queues to use
        :param input_queue:
        :param output_queue:
        :return: None
        """
        self.input_queue = input_queue if input_queue else self.input_queue
        self.output_queue = output_queue if output_queue else self.output_queue

    def issue_message(self, msgtype, msgdata=None, msgparams=None):
        """
        Creates a Message object on the fly and adds it to output queue.
        :param msgtype:
        :param msgdata:
        :param msgparams:
        :return:
        """
        msgobj = Message(issuer=self.pid, message_type=msgtype, message_data=msgdata, message_params=msgparams)
        self.output_queue.put(msgobj)

    def fetch_message(self):
        """
        Check if there is something to get.
        :return: list of Message objects if exists, else 0
        """
        if self.input_queue.empty():
            return 0
        else:
            retval = self.input_queue.get()
            return retval

class MasterCommunicationHandler(CommunicationHandler):
    """
    This communication handler is to be used by the main control process.
    """
    def send_start(self, keymap_path, platform_data_path):
        """
        Sends a start command to slave process, starting bot
        :param keymap_path: path to keymap file to be passed to slave process
        :param platform_data_path: platform file path
        :return: None
        """
        payload = {"keymap": keymap_path, "platform": platform_data_path}
        self.issue_message(MSGTYPE_START, payload)

    def send_stop(self):
        """
        Sends stop command to stop bot
        :return: None
        """
        self.issue_message(MSGTYPE_STOP)

    def send_kill(self):
        """
        Sends command to child process to kill itself
        :return: None
        """
        self.issue_message(MSGTYPE_KILL)

class SlaveCommunicationHandler(CommunicationHandler):
    """
    This communication handler is to be used by the slave process
    """
    def __init__(self, input_queue, output_queue):
        """
        :param input_queue: input queue for receiving commands must be passed
        :param output_queue: output queue for sending log data must be passed
        """
        super(SlaveCommunicationHandler, self).__init__(input_queue, output_queue)

    def send_debug(self, data, params=None):
        self.issue_message(MSGTYPE_LOG_DEBUG, data, params)

    def send_exception(self, data, params=None):
        self.issue_message(MSGTYPE_LOG_EXCEPTION, data, params)

    def send_finished(self):
        self.issue_message(MSGTYPE_INFO_FINISHED)

    def log(self, data):
        self.send_debug(data)

    def exception(self, data):
        self.send_exception(data)
