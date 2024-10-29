# <div align="center">Gamu Logger - Javascript Version</div>

### <div align="center"><a href="../readme.md">🏠 Main page</a> | <a href="../python/readme.md">🐍 Python</a> | 🌐 Javascript</div>

## <div align="center">📚 Table of Contents</div>
<div align="center">
    <h3><a href="#-installation">🔨 Installation</a></h3>
    <h3><a href="#-usage">💡 Usage</a></h3>
    <h3><a href="#️-configuration">⚙️ Configuration</a></h3>
    <h3><a href="#-examples">📁 Examples</a></h3>
    <h3><a href="#-license">📜 License</a></h3>
</div>


## <div align="center">🔨 Installation</div>

install the package using npm:
```bash
npm install @gamunetwork/logger
```



## <div align="center">💡 Usage</div>
- first you need to import the package:
    ```javascript
    import { info, warning, error } from '@gamunetwork/logger';
    ```
- then you can use the functions like this:
    ```javascript
    info('This is an info message');
    warning('This is a warning message');
    error('This is an error message');
    ```

> You may note that the logging function are also available as static methods in the `Logger` class. This allow you to have them encapsulated in a class and use them in a more object oriented way:
> ```javascript
> import { Logger } from '@gamunetwork/logger';
> 
> Logger.info('This is an info message');
> Logger.warning('This is a warning message');
> Logger.error('This is an error message');
> ```



## <div align="center">⚙️ Configuration</div>
You can configure the logger using the `Logger` class. Here is an example of how you can do it:
```javascript
import { Logger, LEVELS, SENSITIVE_LEVELS } from '@gamunetwork/logger';

// default target is standard output, named 'stdout'

Logger.setLevel("stdout", LEVELS.INFO); // all logs with level less than INFO will be ignored

Logger.setSensitiveLevel("stdout", SENSITIVE_LEVELS.HIDE); // If a log message contains sensitive data, it will be hidden

Logger.addSensitiveData('password'); // add 'password' to the tdst of sensitive data (if a log message contains 'password', it will be hidden)

Logger.setModule('my-module'); // set the module name for the current file to 'my-module' (this will be displayed in the log message) (by default, no module name is set)
```

> Please note that the logger can be used without any configuration. The default configuration is:
> - target: stdout
>   - level: `INFO`
>   - sensitive mode: `HIDE`
> - sensitive data: `[]`
> - module name: `None`

> Note also that the module name is set only for the current file. If you want to set the module name for all files, you need to set it in each file.
> From 2.1.0, sub-modules are supported. You can set the module name for a sub-module like this:
> ```javascript
> Logger.setModule('my-module.sub-module');
> ```
> **Warning**: You can nest as many as sub-modules you want, but keep in mind this will increase significantly the length of every log message. This can make the log messages harder to read. So, use sub-modules wisely.



## <div align="center">📁 Examples</div>

you can find examples in the [example](./example) directory.
- [example 1](./example/example1) - very simple calculator
- [example 2](./example/example2) - web server using express, implementing modules



## <div align="center">📜 License</div>

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
