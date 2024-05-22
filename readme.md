# <div align="center">logger module for python and javascript </div>

The goal of this module is to provide a simple, easy to use but powerful logging module for both python and javascript.

## Features
- Simple and easy to use (see examples below)
- Supports multiple log levels (DEEP_DEBUG, DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Supports multiple log outputs (console, file, etc)
- Supports colors in console output
- Contain project modules features based on the current file (see examples below)
- Add decorators to log function calls (see examples below) (python only for now)

## Installation
### Python
The python package is available in the assets of the latest release on [github](https://github.com/GamuNetwork/logger/releases/latest).
You can manually download the package and install it with pip:
```bash
pip install path/to/gamu_logger-x.x.x-py3-none-any.whl
```
Or you can install it directly from github:
```bash
pip install https://github.com/GamuNetwork/logger/releases/download/1.1.4/gamu_logger-1.1.4-py3-none-any.whl
```
> note: replace `1.1.4` with the latest version number.

### Javascript
The javascript package is available in the package of our [github](https://github.com/GamuNetwork/logger/releases/latest) repository. To install it with npm, you will need to add a file named `.npmrc` at the root of your project with the following content:
```properties
@gamunetwork:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
```
and create a environment variable named `GITHUB_TOKEN` with a github token that has access to the `@gamunetwork` package. See github official documentation on how to create a token [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token).

Then you can install the package with npm:
```bash
npm install @gamunetwork/logger
```

## Examples
### Python
```python
from gamuLogger import error, info, critical

error("This is an error message")
info("This is an info message")
critical("This is a critical message")
```
will output:
```log
[ current datetime ] [  ERROR   ] This is an error message
[ current datetime ] [   INFO   ] This is an info message
[ current datetime ] [ CRITICAL ] This is a critical message
```

### Javascript
```javascript
import { Logger, error, info, critical } from '@gamunetwork/logger';

info("This is an info message before setting the module name");

Logger.setModule('module_name'); // set the module name, for this file only

error("This is an error message");
info("This is an info message");
critical("This is a critical message");
```
will output:
```log
[ current datetime ] [   INFO   ] This is an info message before setting the module name
[ current datetime ] [  ERROR   ] [ module_name ] This is an error message
[ current datetime ] [   INFO   ] [ module_name ] This is an info message
[ current datetime ] [ CRITICAL ] [ module_name ] This is a critical message
```

### Configuration
You can configure the logger with the following methods:
- `Logger.setLevel(level: str)`: set the log level (default: INFO)
- `Logger.setModule(module: str)`: set the module name (default: None)
- `Logger.setTarget(target: str)`: set the log target (default: console)

### Decorators
#### debug_func
You can use the `@debug_func(chrono = false)` decorator to log function calls:
```python
from gamuLogger import debug_func

@debug_func()
def my_function():
    info("This is a function")

@debug_func(True)
def my_function2():
    info("This is a function")

my_function()
my_function2()
```

will output:
```log
[ current datetime ] [   DEBUG  ] Calling my_function with:
                                | args: ()
                                | kwargs: {}
[ current datetime ] [   INFO   ] This is a function
[ current datetime ] [   DEBUG  ] Function my_function returned: None
[ current datetime ] [   DEBUG  ] Calling my_function2 with:
                                | args: ()
                                | kwargs: {}
[ current datetime ] [   INFO   ] This is a function
[ current datetime ] [   DEBUG  ] Function my_function2 took 0.000s and returned: None
```

> a variant of this decorator named `@deep_debug_func` is also available. It will do the same thing, but will set it output to DEEP_DEBUG instead of DEBUG.

#### chrono
You can use the `@chrono` decorator to log the time taken by a function to execute:
```python
from gamuLogger import chrono

@chrono
def my_function():
    info("This is a function")

my_function()
```
will output:
```log
[ current datetime ] [   INFO   ] This is a function
[ current datetime ] [   DEBUG  ] Function my_function took 0.000s to execute
```

### message
A `message` function is also available to print a message without any prefix the logs:
```python
from gamuLogger import message, info, COLORS

message("This is a message", COLORS.RED)
info("This is an info message")
```
will output:
```log
This is a message
[ current datetime ] [   INFO   ] This is an info message
```
> if written in a file, the color parameter will be ignored.
