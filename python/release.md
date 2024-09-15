# <div align="center">Gamu Logger - Python Version</div>


## <div align="center">📚 Table of Contents</div>
<div align="center">
    <h3><a href="#-installation">🔨 Installation</a></h3>
    <h3><a href="#-usage">💡 Usage</a></h3>
    <h3><a href="#️-configuration">⚙️ Configuration</a></h3>
    <h3><a href="#-examples">📁 Examples</a></h3>
    <h3><a href="#-license">📜 License</a></h3>
</div>


## <div align="center">🔨 Installation</div>
The package is available in the assets of the latest release on [github](https://github.com/GamuNetwork/logger/releases/latest).

You can manually download the package and install it with pip:
```bash
pip install path/to/gamu_logger-2.0.0-py3-none-any.whl
```
Or install it directly from github (**recommended**):
```bash
pip install https://github.com/GamuNetwork/logger/releases/download/2.0.0/gamu_logger-2.0.0-py3-none-any.whl
```
> note: replace `2.0.0` with the version number you want to install.



## <div align="center">💡 Usage</div>

- First you need to import the package:
    ```python
    from gamuLogger import deepDebug, debug, info, warning, error, critical, Logger, LEVELS, SENSITIVE_LEVELS
    ```
> note: you can also only import the members you need instead of importing all of them.

- Then you can use the functions like this:
    ```python
    info('This is an info message')
    warning('This is a warning message')
    error('This is an error message')
    ```

> You may note that the logging function are also available as static methods in the `Logger` class. This allow you to have them encapsulated in a class and use them in a more object > oriented way:
> ```python
> from gamuLogger import Logger
> 
> Logger.info('This is an info message')
> Logger.warning('This is a warning message')
> Logger.error('This is an error message')
> ```


## <div align="center">⚙️ Configuration</div>

### 1. Basic Configuration
You can configure the logger using methods of the `Logger` class. Here is an example of how you can do it:
```python
from gamuLogger import Logger, LEVELS, SENSITIVE_LEVELS

# default target is the standard output, name is 'stdout'

Logger.setLevel("stdout", LEVELS.INFO); # this mean yhat all logs with level less than INFO will be ignored

Logger.setSensitiveLevel("stdout", SENSITIVE_LEVELS.HIDE); # If a log message contains sensitive data, it will be hidden

Logger.addSensitiveData('myPasswordSecret'); # add 'myPasswordSecret' to the list of sensitive data (if a log message contains any of them, it will be hidden according to the sensitive level)

Logger.setModule('my-module'); # set the module name for this file to 'my-module' (this will be displayed in the log message) (by default, no module name is set)

Logger.addTarget("data.log", LEVELS.DEBUG, SENSITIVE_LEVELS.HIDE) # add a new target to the logger (this will log all messages with level less than DEBUG to the file 'data.log' and hide sensitive data if any)
```

> Please note that the logger can be used without any manual configuration. The default configuration is:
> - target: terminal
>   - level: `INFO`
>   - sensitive mode: `HIDE`
> - sensitive data: `[]`
> - module name: `None`

> Note that the module name is set only for the current file. If you want to set the module name for all files, you need to set it in each file.


### 2. Configuration with `argparse`
This module is compatible with `argparse`, and contains confugurations methods for the argument parser:
```python
from gamuLogger import Logger
import argparse

parser = argparse.ArgumentParser()
Logger.configArgParse(parser) # this will add options to the parser, encapsulated in a group named 'Logger configuration'
args = parser.parse_args()
Logger.parseArgs(args) # this will apply the configuration from the arguments to the logger
```

### 3. Configuration from a file
#### 3.1. JSON Configuration

#### 3.2. XML Configuration


## <div align="center">📁 Examples</div>
you can find examples in the [example](./example) directory.
- [example 1](./example/example1) - 
- [example 2](./example/example2) - 



## <div align="center">📜 License</div>

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
