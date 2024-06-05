import pytest

import sys
import os
import re
import tempfile
from time import sleep

from gamuLogger import Logger, deepDebug, debug, info, warning, error, critical, message, deepDebugFunc, debugFunc, chrono, LEVELS, TERMINAL_TARGETS, SENSITIVE_LEVELS

# from ..src.gamuLogger import Logger, deepDebug, debug, info, warning, error, critical, message, deepDebugFunc, debugFunc, chrono, LEVELS, TERMINAL_TARGETS

class Test_Logger:
    def test_deepDebug(self, capsys):
        Logger.reset()
        Logger.setLevel("terminal", LEVELS.DEEP_DEBUG)
        deepDebug("This is a deep debug message")
        captured = capsys.readouterr()
        result = captured.out
        print(result)
        assert re.match(r"\[.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\] \[.*  DEBUG   .*\] This is a deep debug message", result)
        
    def test_debug(self, capsys):
        Logger.reset()
        Logger.setLevel("terminal", LEVELS.DEBUG)
        debug("This is a debug message")
        captured = capsys.readouterr()
        result = captured.out
        print(result)
        assert re.match(r"\[.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\] \[.*  DEBUG   .*\] This is a debug message", result)
        
    def test_info(self, capsys):
        Logger.reset()
        Logger.setLevel("terminal", LEVELS.INFO)
        info("This is an info message")
        captured = capsys.readouterr()
        result = captured.out
        print(result)
        assert re.match(r"\[.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\] \[.*   INFO   .*\] This is an info message", result)
        
    def test_warning(self, capsys):
        Logger.reset()
        Logger.setLevel("terminal", LEVELS.WARNING)
        warning("This is a warning message")
        captured = capsys.readouterr()
        result = captured.out
        print(result)
        assert re.match(r"\[.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\] \[.* WARNING  .*\] This is a warning message", result)
        
    def test_error(self, capsys):
        Logger.reset()
        Logger.setLevel("terminal", LEVELS.ERROR)
        error("This is an error message")
        captured = capsys.readouterr()
        result = captured.out
        print(result)
        assert re.match(r"\[.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\] \[.*  ERROR   .*\] This is an error message", result)
        
    def test_critical(self, capsys):
        Logger.reset()
        Logger.setLevel("terminal", LEVELS.CRITICAL)
        critical("This is a critical message")
        captured = capsys.readouterr()
        result = captured.out
        print(result)
        assert re.match(r"\[.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\] \[.* CRITICAL .*\] This is a critical message", result)
        
    def test_message(self, capsys):
        Logger.reset()
        Logger.setLevel("terminal", LEVELS.INFO)
        message("This is a message")
        captured = capsys.readouterr()
        result = captured.out
        print(result)
        assert re.match(r"This is a message", result)
        
    def test_multiline(self, capsys):
        Logger.reset()
        Logger.setLevel("terminal", LEVELS.INFO)
        info("This is a message\nThis is a message")
        captured = capsys.readouterr()
        result = captured.out
        print(result)
        assert re.match(r"\[.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\] \[.*   INFO   .*\] This is a message\n                                 \| This is a message", result)
        
    def test_module(self, capsys):
        Logger.reset()
        Logger.setLevel("terminal", LEVELS.INFO)
        Logger.setModule("test")
        info("This is a message")
        captured = capsys.readouterr()
        result = captured.out
        print(result)
        assert re.match(r"\[.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\] \[.*   INFO   .*\] \[ .*   test   .* \] This is a message", result)
        
    def test_multiline_module(self, capsys):
        Logger.reset()
        Logger.setLevel("terminal", LEVELS.INFO)
        Logger.setModule("test")
        info("This is a message\nThis is a message")
        captured = capsys.readouterr()
        result = captured.out
        print(result)
        assert re.match(r"\[.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\] \[.*   INFO   .*\] \[ .*   test   .* \] This is a message\n                                                \| This is a message", result)
        
    def test_too_long_module_name(self):
        Logger.reset()
        with pytest.raises(ValueError):
            Logger.setModule("This module name is too long")
            
    def test_chrono(self, capsys):
        Logger.reset()
        Logger.setLevel("terminal", LEVELS.DEBUG)
        
        @chrono
        def test():
            sleep(1)
        
        test()
        captured = capsys.readouterr()
        result = captured.out
        print(result)
        assert re.match(r"\[.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\] \[.*  DEBUG   .*\] Function test took 0:00:01.\d{6} to execute", result)
        
    def test_deepDebugFunc(self, capsys):
        Logger.reset()
        Logger.setLevel("terminal", LEVELS.DEEP_DEBUG)
        
        @deepDebugFunc(True)
        def test():
            return "This is a deep debug function"
        
        test()
        captured = capsys.readouterr()
        result = captured.out
        print(result)
        assert re.match(r"\[.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\] \[.*  DEBUG   .*\] Calling test with\n                                 \| args: \(\)\n                                 \| kwargs: {}\n\[.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\] \[.*  DEBUG   .*\] Function test took 0:00:00.\d{6} to execute and returned \"This is a deep debug function\"", result)
        
    def test_debugFunc(self, capsys):
        Logger.reset()
        Logger.setLevel("terminal", LEVELS.DEBUG)
        
        @debugFunc(False)
        def test():
            return "This is a debug function"
        
        test()
        captured = capsys.readouterr()
        result = captured.out
        print(result)
        assert re.match(r'\[.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\] \[.*  DEBUG   .*\] Calling test with\n                                 \| args: \(\)\n                                 \| kwargs: {}\n\[.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\] \[.*  DEBUG   .*\] Function test returned "This is a debug function"', result)
        
    def test_setLevel(self, capsys):
        Logger.reset()
        Logger.setLevel("terminal", LEVELS.INFO)
        
        debug("This is a debug message that should not be displayed")
        
        Logger.setLevel("terminal", LEVELS.DEBUG)
        
        debug("This is a debug message that should be displayed")
        
        captured = capsys.readouterr()
        result = captured.out
        print(result)
        assert re.match(r"\[.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\] \[.*  DEBUG   .*\] This is a debug message that should be displayed", result)
        
    def test_setSensitiveMode(self, capsys):
        Logger.reset()
        
        data = "abcdefg"
        
        Logger.setSensitiveMode("terminal", SENSITIVE_LEVELS.HIDE)
        Logger.addSensitiveData(data)
        info("This is a message with a password: " + data)
        
        captured = capsys.readouterr()
        result = captured.out
        print(result)
        
        assert data not in result
        
        Logger.setSensitiveMode("terminal", SENSITIVE_LEVELS.SHOW)
        Logger.addSensitiveData(data)
        
        info("This is a message with a password: " + data)
        
        captured = capsys.readouterr()
        result = captured.out
        print(result)
        
        assert data in result
        
        