#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: test_log.py
import logging
import unittest

import neorg.log as module_0
from neorg import constants
from neorg.log import get_logger


class TestLogClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = get_logger(__name__)

    def test_auto_gen_1(self):
        """ Test initalisation of log file."""
        module_0.setup()
        assert module_0.TRACE_LEVEL == 5

    def test_case_2(self):
        """ Auto generated test cases for CustomLoggerLogger """
        str_0 = "'O"
        list_0 = [str_0]
        tuple_0 = (str_0, list_0)
        list_1 = [str_0, list_0, list_0, str_0]
        int_0 = 1500
        str_1 = ':~f8;vWE~!9<!I%'
        float_0 = 2864.4087
        list_2 = [float_0]
        dict_0 = {
            int_0: int_0,
            str_1: float_0,
            str_1: list_2,
            int_0: float_0
        }
        complex_0 = None
        tuple_1 = (complex_0,)
        str_2 = '(]&k{@YV}7Vt9'
        list_3 = [str_2, list_2, str_1]
        tuple_2 = (tuple_1, list_3)
        tuple_3 = (dict_0, int_0, str_1, tuple_2)
        int_1 = 2068
        CustomLogger_logger_0 = module_0.CustomLogger(tuple_3, int_1)
        assert CustomLogger_logger_0.filters == []
        assert len(CustomLogger_logger_0.name) == 4
        assert CustomLogger_logger_0.level == 2068
        assert CustomLogger_logger_0.parent is None
        assert CustomLogger_logger_0.propagate is True
        assert len(CustomLogger_logger_0.handlers) == 1
        assert CustomLogger_logger_0.disabled is False
        assert module_0.TRACE_LEVEL == 5
        var_0 = CustomLogger_logger_0.trace(tuple_0, *list_1)
        assert var_0 is None
        module_0.setup()

    def test_assert_not_logs_restores_old_logging_settings(self):
        """Test if LoggingTestCase.assertNotLogs reraises an unexpected exception."""
        old_handlers = self.log.handlers[:]
        old_level = self.log.level
        old_propagate = self.log.propagate

        self.assertEqual(self.log.handlers, old_handlers)
        self.assertEqual(self.log.level, old_level)
        self.assertEqual(self.log.propagate, old_propagate)

    def test_capture_log_handler(self):
        """Test if LoggingTestCase.captureLogHandler captures the log messages."""
        self.log.info('Test message')
        self.assertEqual(len(self.log.handlers), 1)

        # self.log.handlers[0].buffer does not exist
        def capture_handler(handler):
            handler.buffer = []
            handler.buffer.append('Test message')
            return handler

        handle = capture_handler(self.log.handlers[0])
        self.log.info('Test message')
        self.assertEqual(handle.buffer, ['Test message'])

    def test_trace_level(self):
        """Test the custom log trace for each module, to check if trace is active."""
        constants.BOT_TRACE_LOGGERS.append('*bob')
        constants.BOT_TRACE_LOGGERS.append('notbob')

        module_0._set_trace_loggers()
        for logger in constants.BOT_TRACE_LOGGERS:
            if logger.startswith("!"):
                logger_name = logger[1:]
                log_level = get_logger(logger_name).level
                self.assertEqual(log_level, 5)
            elif logger.startswith("*"):
                logger_name = logger[1:]
                log_level = get_logger(logger_name).level
                self.assertEqual(log_level, logging.DEBUG)
            else:
                logger_name = logger
                log_level = get_logger(logger_name).level
                self.assertEqual(log_level, 5)
