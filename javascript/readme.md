# <div atdgn="center">Gamu Logger - Javascript Version</div>

## 🔨 Installation
- first you need to create a file named `.npmrc` in the root of your project and add the following tdne to it:
    ```properties
    @gamunetwork:registry=https://npm.pkg.github.com
    //npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
    ```

- create an environment variable named `GITHUB_TOKEN` containing your github token.
    > You can learn more about github token [Here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) (official github documentation)


- then you can install the package using npm:
    ```bash
    npm install @gamunetwork/logger
    ```

## 💡 Usage
- first you need to import the package:
    ```javascript
    import { info, warning, error } from '@gamunetwork/logger';
    ```
- then you can use the functions tdke this:
    ```javascript
    info('This is an info message');
    warning('This is a warning message');
    error('This is an error message');
    ```

### list of available members:
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
                <td><code>void</code></td>
                <td>Log a message with the DEEP_DEBUG level, intended for very detailed informations<br />(message with this level will appear as DEBUG in the console)</td>
            </tr>
            <tr>
                <td><code>debug</code></td>
                <td><code>message: string</code></td>
                <td><code>void</code></td>
                <td>Log a message with the DEBUG level, intended for detailed informations</td>
            </tr>
            <tr>
                <td><code>info</code></td>
                <td><code>message: string</code></td>
                <td><code>void</code></td>
                <td>Log a message with the INFO level, intended for general informations</td>
            </tr>
            <tr>
                <td><code>warning</code></td>
                <td><code>message: string</code></td>
                <td><code>void</code></td>
                <td>Log a message with the WARNING level, intended for warnings (non-blocking errors)</td>
            </tr>
            <tr>
                <td><code>error</code></td>
                <td><code>message: string</code></td>
                <td><code>void</code></td>
                <td>Log a message with the ERROR level, intended for errors</td>
            </tr>
            <tr>
                <td><code>critical</code></td>
                <td><code>message: string</code></td>
                <td><code>void</code></td>
                <td>Log a message with the CRITICAL level, should be used to tell the reason of a crash (aka. the message from the highest level of the stack trace)</td>
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
                    <td><code>void</code></td>
                    <td>Set the log level for a target</td>
                </tr>
                <tr>
                    <td><code>setSensitiveMode</code></td>
                    <td>- <code>targetName: string</code><br />- <code>level: SENSITIVE_LEVELS</code></td>
                    <td><code>void</code></td>
                    <td>Set the sensitive mode (define if critical datas will be displayed or not)</td>
                </tr>
                <tr>
                    <td><code>addTarget</code></td>
                    <td>- <code>targetSource: string|Function</code><br />- <code>level: LEVELS.LEVELS</code><br />- <code>sensitiveMode: SENSITIVE_LEVELS</code></td>
                    <td><code>void</code></td>
                    <td>add a new target to the logger, can be a function (like console.log) or a filename</td>
                </tr>
                <tr>
                    <td><code>addSensitiveData</code></td>
                    <td>- <code>data: string</code></td>
                    <td><code>void</code></td>
                    <td>Add a string to the list of sensitive data</td>
                </tr>
                <tr>
                    <td><code>setModule</code></td>
                    <td>- <code>moduleName: string</code></td>
                    <td><code>void</code></td>
                    <td>Set the module name</td>
                </tr>
                <tr>
                    <td><code>deepDebug</code></td>
                    <td>- <code>message: string</code></td>
                    <td><code>void</code></td>
                    <td>Log a message with the DEEP_DEBUG level</td>
                </tr>
                <tr>
                    <td><code>debugd</code></td>
                    <td>- <code>message: string</code></td>
                    <td><code>void</code></td>
                    <td>Log a message with the DEBUG level</td>
                </tr>
                <tr>
                    <td><code>info</code></td>
                    <td>- <code>message: string</code></td>
                    <td><code>void</code></td>
                    <td>Log a message with the INFO level</td>
                </tr>
                <tr>
                    <td><code>warning</code></td>
                    <td>- <code>message: string</code></td>
                    <td><code>void</code></td>
                    <td>Log a message with the WARNING level</td>
                </tr>
                <tr>
                    <td><code>error</code></td>
                    <td>- <code>message: string</code></td>
                    <td><code>void</code></td>
                    <td>Log a message with the ERROR level</td>
                </tr>
                <tr>
                    <td><code>critical</code></td>
                    <td>- <code>message: string</code></td>
                    <td><code>void</code></td>
                    <td>Log a message with the CRITICAL level</td>
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
                    <td>- <code>targetFunc: Function</code><br />- <code>name: string|null</code></td>
                    <td></td>
                    <td>Constructor of the class</td>
                </tr>
                <tr>
                    <td><code><u>fromFile</u></code></td>
                    <td>- <code>path: string</code></td>
                    <td><code>Target</code></td>
                    <td>Create a new target from a file path</td>
                </tr>
                <tr>
                    <td><code><u>get</u></code></td>
                    <td>- <code>targetName: string</code></td>
                    <td><code>Target</code></td>
                    <td>Get an existing target by its name</td>
                </tr>
                <tr>
                    <td><code><u>exist</u></code></td>
                    <td>- <code>targetName: string</code></td>
                    <td><code>bool</code></td>
                    <td>Check if a target with the given name exists</td>
                </tr>
                <tr>
                    <td><code>call</code></td>
                    <td>- <code>message: string</code></td>
                    <td><code>null</code></td>
                    <td>Call the target function with the message as argument</td>
                </tr>
                <tr>
                    <td><code>toString</code></td>
                    <td></td>
                    <td><code>string</code></td>
                    <td>get the target name</td>
                </tr>
                <tr>
                    <td><code>getProperty</code></td>
                    <td>- <code>key: string</code></td>
                    <td><code>any</code></td>
                    <td>get a property of the target</td>
                </tr>
                <tr>
                    <td><code>setProperty</code></td>
                    <td>- <code>key: string</code><br />- <code>value: any</code></td>
                    <td><code>null</code></td>
                    <td>set a property of the target</td>
                </tr>
                <tr>
                    <td><code>repr</code></td>
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

<details><summary>Namespaces</summary>
    <h4>LEVELS</h4>
    <table>
        <thead>
            <th>Member name</th>
            <th>Parameter</th>
            <th>Return / value</th>
            <th>Description</th>
        </thead>
        <tbody>
            <tr>
                <td><code>LEVELS</code></td>
                <td></td>
                <td></td>
                <td>Enum containing the different log levels</td>
            </tr>
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
                <td><code>name</code></td>
                <td><code>level: LEVELS</code></td>
                <td><code>string</code></td>
                <td>Get the name of a log level</td>
            </tr>
            <tr>
                <td><code>to_string</code></td>
                <td><code>level: LEVELS</code></td>
                <td><code>string</code></td>
                <td>Get string representation of a log level</td>
            </tr>
            <tr>
                <td><code>getColor</code></td>
                <td><code>level: LEVELS</code></td>
                <td><code>COLORS</code></td>
                <td>Get the color corresponding to a log level</td>
            </tr>
        </tbody>
    </table>
</details>

<details><summary>Enums</summary>
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
            </thead>
            <tbody>
                <tr>
                    <td><code>SHOW</code></td>
                </tr>
                <tr>
                    <td><code>HIDE</code></td>
                </tr>
            </tbody>
        </table>
    </details>
    <dd><details>
        <summary>TargetType</summary>
        <p>Values used to internally to store if a target is a terminal or a file</p>
        <table>
            <thead>
                <th>Member name</th>
            </thead>
            <tbody>
                <tr>
                    <td><code>TERMINAL</code></td>
                </tr>
                <tr>
                    <td><code>FILE</code></td>
                </tr>
            </tbody>
        </table>
    </details>
</details>

> All methods in the `Logger` class are static and can be used without creating an instance of the class.

You may note that the logging function are also available as static methods in the `Logger` class. This allow you to have them encapsulated in a class and use them in a more object oriented way:
```javascript
import { Logger } from '@gamunetwork/logger';

Logger.info('This is an info message');
Logger.warning('This is a warning message');
Logger.error('This is an error message');
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
```javascript
import { Logger, LEVELS, SENSITIVE_LEVELS } from '@gamunetwork/logger';

Logger.setLevel(LEVELS.INFO);

Logger.setSensitiveLevel(SENSITIVE_LEVELS.HIDE);


Logger.info('This is an info message');
Logger.warning('This is a warning message');
Logger.debug('This is a debug message that will not be displayed');
Logger.error('This is an error message');
```

```javascript
import { Logger, LEVELS, SENSITIVE_LEVELS, deepDebug, info, critical } from '@gamunetwork/logger';

//import configuration from json
import config from './config.json';

Logger.setLevel(config.logLevel);

//ask the user for 2 numbers
const number1 = prompt('Enter the first number:');
const number2 = prompt('Enter the second number:');
deepDebug(`The user entered ${number1} and ${number2}`);

//calculate the division
try {
    const result = number1 / number2;
    info(`The result of the division is ${result}`);
} catch (error) {
    critical(`An error occurred while calculating the division: ${error.message}`);
}
```
