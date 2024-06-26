# <div align="center">Gamu Logger - Main Page</div>

### <div align="center">🏠 Main page | <a href="./python/readme.md">🐍 Python</a> | <a href="./javascript/readme.md">🌐 Javascript</a></div>

## <div align="center">📚 Table of Contents</div>
<div align="center">
    <h3><a href="#-features">✨ Features</a></h3>
    <h3><a href="#-installation">🔨 Installation</a></h3>
    <h3><a href="#-examples">💡 Examples</a></h3>
    <h3><a href="#-issue">🚨 Issue</a></h3>
</div>

The goal of this module is to provide a simple, easy to use but powerful logging module for both python and javascript.

## ✨ Features
- Simple and easy to use (see examples below)
- Supports multiple log levels (DEEP_DEBUG, DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Supports multiple log outputs (console, file) with separated level configuration
- Supports colors in console output
- Contain project modules features based on the current file (see examples below)
- Add decorators to log function calls (see examples below) (python only for now)


## 💡 Examples
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

> a variant of this decorator named `@deep_debug_func` is also available. It will do the same thing, but will set it output to DEEP_DEBUG instead of DEBUG.

## 🚨 Issue
If you encounter any problem, please let us know by creating an issue here, on github !
