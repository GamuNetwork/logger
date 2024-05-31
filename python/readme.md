# <div align="center">Gamu Logger - Python Version</div>

## 🔨 Installation
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

## 💡Usage

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

### List of available members:
<details><summary>Logging functions</summary>
    <table>
        <thead>
            <th>Function name</th>
            <th>arguments</th>
            <th>return type</th>
            <th>Description</th>
        </thead>
        <tbody>
            <tr>
                <td><code>deepDebug</code></td>
                <td><code>message: string</code></td>
                <td><code>None</code></td>
                <td>Log a message with the DEEP_DEBUG level, intended for very detailed informations<br />(message with this level will appear as DEBUG in the console)</td>
            </tr>
            <tr>
                <td><code>debug</code></td>
                <td><code>message: string</code></td>
                <td><code>None</code></td>
                <td>Log a message with the DEBUG level, intended for detailed informations</td>
            </tr>
            <tr>
                <td><code>info</code></td>
                <td><code>message: string</code></td>
                <td><code>None</code></td>
                <td>Log a message with the INFO level, intended for general informations</td>
            </tr>
            <tr>
                <td><code>warning</code></td>
                <td><code>message: string</code></td>
                <td><code>None</code></td>
                <td>Log a message with the WARNING level, intended for warnings (non-blocking errors)</td>
            </tr>
            <tr>
                <td><code>error</code></td>
                <td><code>message: string</code></td>
                <td><code>None</code></td>
                <td>Log a message with the ERROR level, intended for errors</td>
            </tr>
            <tr>
                <td><code>critical</code></td>
                <td><code>message: string</code></td>
                <td><code>None</code></td>
                <td>Log a message with the CRITICAL level, should be used to tell the reason of a crash (aka. the message from the highest level of the stack trace)</td>
            </tr>
            <tr>
                <td><code>message</code></td>
                <td>- <code>message: Any</code><br />- <code>color: COLORS</code></td>
                <td><code>None</code></td>
                <td>Display a message with a specific color</td>
            </tr>
            <tr>
            </tr>
        </tbody>
    </table>
</details>

<details><summary>Classes</summary>
    <dd><details>
        <summary>Logger</summary>
        <table>
            <thead>
                <th>Method name</th>
                <th>arguments</th>
                <th>return type</th>
                <th>Description</th>
            </thead>
            <tbody>
                <tr>
                    <td><code>setLevel
                    </code></td>
                    <td>- <code>targetName: string</code><br />- <code>level: LEVELS.LEVELS</code></td>
                    <td><code>None</code></td>
                    <td>Set the log level for a target</td>
                </tr>
                <tr>
                    <td><code>setSensitiveMode</code></td>
                    <td>- <code>targetName: string</code><br />- <code>mode: SENSITIVE_LEVELS</code></td>
                    <td><code>None</code></td>
                    <td>Set the sensitive mode (define if critical datas will be displayed or not)</td>
                </tr>
                <tr>
                    <td><code>addTarget</code></td>
                    <td>- <code>targetSource: Callable[[str], None] | str | Target</code><br />- <code>level: LEVELS.LEVELS</code><br />- <code>sensitiveMode: SENSITIVE_LEVELS</code></td>
                    <td><code>None</code></td>
                    <td>add a new target to the logger, can be a function (like console.log) or a filename</td>
                </tr>
                <tr>
                    <td><code>addSensitiveData</code></td>
                    <td>- <code>data: string</code></td>
                    <td><code>None</code></td>
                    <td>Add a string to the list of sensitive data</td>
                </tr>
                <tr>
                    <td><code>setModule</code></td>
                    <td>- <code>name: string</code></td>
                    <td><code>None</code></td>
                    <td>Set the module name</td>
                </tr>
                <tr>
                    <td><code>deepDebug</code></td>
                    <td>- <code>message: string</code></td>
                    <td><code>None</code></td>
                    <td>Log a message with the DEEP_DEBUG level</td>
                </tr>
                <tr>
                    <td><code>debug</code></td>
                    <td>- <code>message: string</code></td>
                    <td><code>None</code></td>
                    <td>Log a message with the DEBUG level</td>
                </tr>
                <tr>
                    <td><code>info</code></td>
                    <td>- <code>message: string</code></td>
                    <td><code>None</code></td>
                    <td>Log a message with the INFO level</td>
                </tr>
                <tr>
                    <td><code>warning</code></td>
                    <td>- <code>message: string</code></td>
                    <td><code>None</code></td>
                    <td>Log a message with the WARNING level</td>
                </tr>
                <tr>
                    <td><code>error</code></td>
                    <td>- <code>message: string</code></td>
                    <td><code>None</code></td>
                    <td>Log a message with the ERROR level</td>
                </tr>
                <tr>
                    <td><code>critical</code></td>
                    <td>- <code>message: string</code></td>
                    <td><code>None</code></td>
                    <td>Log a message with the CRITICAL level</td>
                </tr>
                <tr>
                    <td><code>message</code></td>
                    <td>- <code>message: string</code><br />- <code>color: COLORS</code></td>
                    <td><code>None</code></td>
                    <td>Log a message with the DEEP_DEBUG level</td>
                </tr>
                <tr>
                    <td><code>configArgparse</code></td>
                    <td>- <code>parser : argparse.ArgumentParser</code></td>
                    <td><code>None</code></td>
                    <td>Configure an argparse parser to add the logger arguments</td>
                </tr>
                <tr>
                    <td><code>parseArgs</code></td>
                    <td>- <code>args : argparse.Namespace</code></td>
                    <td><code>None</code></td>
                    <td>Parse the arguments from an argparse parser and apply them to the logger</td>
                </tr>
            </tbody>
        </table>
    </details>
    <dd><details>
        <summary>Target</summary>
        <p>Class used internally to store a target</p>
        <table>
            <thead>
                <th>Method name</th>
                <th>arguments</th>
                <th>return type</th>
                <th>Description</th>
            </thead>
            <tbody>
                <tr>
                    <td><code>constructor</code></td>
                    <td>- <code>target: Callable[[str], None]</code><br />- <code>name: string|None</code></td>
                    <td></td>
                    <td>Constructor of the class</td>
                </tr>
                <tr>
                    <td><code><u>fromFile</u></code></td>
                    <td>- <code>file: string</code></td>
                    <td><code>Target</code></td>
                    <td>Create a new target from a file path</td>
                </tr>
                <tr>
                    <td><code><u>get</u></code></td>
                    <td>- <code>name: string</code></td>
                    <td><code>Target</code></td>
                    <td>Get an existing target by its name</td>
                </tr>
                <tr>
                    <td><code><u>exist</u></code></td>
                    <td>- <code>name: string</code></td>
                    <td><code>bool</code></td>
                    <td>Check if a target with the given name exists</td>
                </tr>
                <tr>
                    <td><code>__call__</code></td>
                    <td>- <code>string: string</code></td>
                    <td><code>None</code></td>
                    <td>Call the target function with the message as argument</td>
                </tr>
                <tr>
                    <td><code>__str__</code></td>
                    <td></td>
                    <td><code>string</code></td>
                    <td>get the target name</td>
                </tr>
                <tr>
                    <td><code>__getitem__</code></td>
                    <td>- <code>key: string</code></td>
                    <td><code>any</code></td>
                    <td>get a property of the target</td>
                </tr>
                <tr>
                    <td><code>__delitem__</code></td>
                    <td>- <code>key: string</code></td>
                    <td><code>any</code></td>
                    <td>delete a property of the target</td>
                </tr>
                <tr>
                    <td><code>__contains__</code></td>
                    <td>- <code>key: string</code></td>
                    <td><code>any</code></td>
                    <td>check if a property exists in the target</td>
                </tr>
                <tr>
                    <td><code>__setitem__</code></td>
                    <td>- <code>key: string</code><br />- <code>value: any</code></td>
                    <td><code>None</code></td>
                    <td>set a property of the target</td>
                </tr>
                <tr>
                    <td><code>__repr__</code></td>
                    <td></td>
                    <td><code>string</code></td>
                    <td>get a string representation of the target</td>
                </tr>
                <tr>
                    <td><code>name</code></td>
                    <td><code>string</code></td>
                    <td><code>string</code></td>
                    <td>the name of the target (read/write)</td>
                </tr>
                <tr>
                    <td><code>type</code></td>
                    <td></td>
                    <td><code>string</code></td>
                    <td>the type of the target (read only)</td>
                </tr>
            </tbody>
        </table>
    </details>
</details>

<details><summary>Enums</summary>
    <dd><details><summary>LEVELS</summary>
        <table>
            <thead>
                <th>Member name</th>
                <th>Parameter</th>
                <th>Return / value</th>
                <th>Description</th>
            </thead>
            <tbody>
                <tr>
                    <td><code>DEEP_DEBUG</code></td>
                    <td></td>
                    <td><code>0</code></td>
                    <td>Shortcut for <code>LEVELS.LEVELS.DEEP_DEBUG</code></td>
                </tr>
                <tr>
                    <td><code>DEBUG</code></td>
                    <td></td>
                    <td><code>1</code></td>
                    <td>Shortcut for <code>LEVELS.LEVELS.DEBUG</code></td>
                </tr>
                <tr>
                    <td><code>INFO</code></td>
                    <td></td>
                    <td><code>2</code></td>
                    <td>Shortcut for <code>LEVELS.LEVELS.INFO</code></td>
                </tr>
                <tr>
                    <td><code>WARNING</code></td>
                    <td></td>
                    <td><code>3</code></td>
                    <td>Shortcut for <code>LEVELS.LEVELS.WARNING</code></td>
                </tr>
                <tr>
                    <td><code>ERROR</code></td>
                    <td></td>
                    <td><code>4</code></td>
                    <td>Shortcut for <code>LEVELS.LEVELS.ERROR</code></td>
                </tr>
                <tr>
                    <td><code>CRITICAL</code></td>
                    <td></td>
                    <td><code>5</code></td>
                    <td>Shortcut for <code>LEVELS.LEVELS.CRITICAL</code></td>
                </tr>
                <tr>
                    <td><code><u>from_string</u></code></td>
                    <td><code>level: str</code></td>
                    <td><code>LEVELS</code></td>
                    <td>Get the level corresponding to a string</td>
                </tr>
                <tr>
                    <td><code>__str__</code></td>
                    <td></td>
                    <td><code>string</code></td>
                    <td>Get string representation of a log level</td>
                </tr>
                <tr>
                    <td><code>__int__</code></td>
                    <td></td>
                    <td><code>int</code></td>
                    <td>Get integer representation of a log level</td>
                </tr>
                <tr>
                    <td><code>__le__</code></td>
                    <td><code>other: LEVELS</code></td>
                    <td><code>bool</code></td>
                    <td>Check if a level is less or equal to another</td>
                </tr>
                <tr>
                    <td><code>color</code></td>
                    <td></td>
                    <td><code>COLORS</code></td>
                    <td>Get the color corresponding to a log level</td>
                </tr>
            </tbody>
        </table>
    </details>
    <dd><details>
        <summary>COLORS</summary>
        <p>contain ansi color codes for following colors:</p>
        <table>
            <thead>
                <th>Member name</th>
                <th>value</th>
            </thead>
            <tbody>
                <tr>
                    <td><code>RED</code></td>
                    <td><code>\x1b[91m</code></td>
                </tr>
                <tr>
                    <td><code>DARK_RED</code></td>
                    <td><code>\x1b[91m\x1b[1m</code></td>
                </tr>
                <tr>
                    <td><code>GREEN</code></td>
                    <td><code>\x1b[92m</code></td>
                </tr>
                <tr>
                    <td><code>YELLOW</code></td>
                    <td><code>\x1b[93m</code></td>
                </tr>
                <tr>
                    <td><code>BLUE</code></td>
                    <td><code>\x1b[94m</code></td>
                </tr>
                <tr>
                    <td><code>RESET</code></td>
                    <td><code>\x1b[0m</code></td>
                </tr>
                <tr>
                    <td><code>NONE</code></td>
                    <td>empty string</td>
                </tr>
            </tbody>
        </table>
    </details>
    <dd><details>
        <summary>SENSITIVE_LEVELS</summary>
        <p>Values used to define how the logger should handle sensitive data</p>
        <table>
            <thead>
                <th>Member name</th>
                <th>parameter</th>
                <th>value</th>
                <th>Description</th>
            </thead>
            <tbody>
                <tr>
                    <td><code>SHOW</code></td>
                    <td></td>
                    <td><code>1</code></td>
                    <td>Display sensitive data</td>
                </tr>
                <tr>
                    <td><code>HIDE</code></td>
                    <td></td>
                    <td><code>0</code></td>
                    <td>Hide sensitive data</td>
                </tr>
                <tr>
                    <td><u>from_string</u></td>
                    <td><code>level: str</code></td>
                    <td><code>SENSITIVE_LEVELS</code></td>
                    <td>Get the level corresponding to a string</td>
                </tr>
                <tr>
                    <td><u>from_bool</u></td>
                    <td><code>value: bool</code></td>
                    <td><code>SENSITIVE_LEVELS</code></td>
                    <td>Get the level corresponding to a boolean (True = SHOW, False = HIDE)</td>
                </tr>
            </tbody>
        </table>
    </details>
</details>

> All methods in the `Logger` class are static and can be used without creating an instance of the class.

You may note that the logging function are also available as static methods in the `Logger` class. This allow you to have them encapsulated in a class and use them in a more object oriented way:
```python
from gamuLogger import Logger

Logger.info('This is an info message')
Logger.warning('This is a warning message')
Logger.error('This is an error message')
```


## Configuration
You can configure the logger using the `Logger` class. Here is an example of how you can do it:
```javascript
import { Logger, LEVELS, SENSITIVE_LEVELS } from '@gamunetwork/logger';

// default target is the terminal, name is 'terminal'

Logger.setLevel("terminal", LEVELS.INFO); // all logs with level less than INFO will be ignored

Logger.setSensitiveLevel("terminal", SENSITIVE_LEVELS.HIDE); // If a log message contains sensitive data, it will be hidden

Logger.addSensitiveData('password'); // add 'password' to the tdst of sensitive data (if a log message contains 'password', it will be hidden)

Logger.setModule('my-module'); // set the module name for this file to 'my-module' (this will be displayed in the log message) (by default, no module name is set)
```

> Please note that the logger can be used without any configuration. The default configuration is:
> - target: terminal
>   - level: `INFO`
>   - sensitive mode: `HIDE`
> - sensitive data: `[]`
> - module name: `None`

> Note also that the module name is set only for the current file. If you want to set the module name for all files, you need to set it in each file.

## Examples
Here are some examples of how you can use the logger:
```python
from gamuLogger import Logger, LEVELS, SENSITIVE_LEVELS, deepDebug, info, warning, error, critical

Logger.setLevel("terminal", LEVELS.INFO)
info("A more detailled log file is available at out.log")

Logger.addTarget("out.log", LEVELS.DEEP_DEBUG, SENSITIVE_LEVELS.SHOW)

info('This is an info message')
warning('This is a warning message')
debug('This is a debug message') # this message will only be displayed in the log file, not in the console
error('This is an error message')
```

```python
from gamuLogger import Logger, LEVELS, SENSITIVE_LEVELS, deepDebug, info, warning, error, critical
from json import loads

config = loads(open('config.json').read())

Logger.setLevel("terminal", config['logLevel'])

# ask the user for 2 numbers
const number1 = prompt('Enter the first number:')
const number2 = prompt('Enter the second number:')
deepDebug(f"The user entered the numbers {number1} and {number2}")

# calculate the division
try
    const result = number1 / number2
    info(f"The result of the division is {result}")
except error as e:
    critical(f"An error occured: {e}")

```

