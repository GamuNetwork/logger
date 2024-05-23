# Gamu Logger - Javascript Version

## Installation
- first you need to create a file named `.npmrc` in the root of your project and add the following line to it:
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

## Usage
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

### List of available members:
<details>
<summary>Logging functions</summary>
    <ul>
        <li><code>deepDebug(message: string) : void</code></li>
        <li><code>debug(message: string) : void</code></li>
        <li><code>info(message: string) : void</code></li>
        <li><code>warning(message: string) : void</code></li>
        <li><code>error(message: string) : void</code></li>
        <li><code>critical(message: string) : void</code></li>
    </ul>
</details>
<details>
<summary>Classes</summary>
    <ul>
        <li><code>Logger</code>
            <ul>
            <li><code>setLevel(level: LEVELS.LEVELS) : void</code></li>
            <li><code>setTarget(target: any) : void</code></li>
            <li><code>setSensitiveLevel(level: SENSITIVE_LEVELS) : void</code></li>
            <li><code>addSensitiveData(data: string) : void</code></li>
            <li><code>setModule(moduleName: string) : void</code></li>
            <li><code>deepDebug(message: string) : void</code></li>
            <li><code>debug(message: string) : void</code></li>
            <li><code>info(message: string) : void</code></li>
            <li><code>warning(message: string) : void</code></li>
            <li><code>error(message: string) : void</code></li>
            <li><code>critical(message: string) : void</code></li>
            </ul>
        </li>
    </ul>
</details>

<details>
<summary>Namespaces</summary>
    <ul>
        <li><code>LEVELS</code>
            <ul>
                <li><code>LEVELS</code>
                    <ul>
                        <li><code>DEEP_DEBUG</code></li>
                        <li><code>DEBUG</code></li>
                        <li><code>INFO</code></li>
                        <li><code>WARNING</code></li>
                        <li><code>ERROR</code></li>
                        <li><code>CRITICAL</code></li>
                    </ul>
                </li>
                <li><code>name(level: LEVELS) : string</code></li>
                <li><code>toString(level: LEVELS) : string</code></li>
                <li><code>getColor(level: LEVELS) : COLORS</code></li>
            </ul>
        </li>
    </ul>
</details>

<details>
<summary>Enums</summary>
    <ul>
        <li><code>COLORS</code>
            <ul>
                <li><code>RED</code></li>
                <li><code>DARK_RED</code></li>
                <li><code>GREEN</code></li>
                <li><code>YELLOW</code></li>
                <li><code>BLUE</code></li>
                <li><code>RESET</code></li>
                <li><code>NONE</code></li>
            </ul>
        </li>
        <li><code>SENSITIVE_LEVELS</code>
            <ul>
                <li><code>HIDE</code></li>
                <li><code>ENCODE</code></li>
                <li><code>SHOW</code></li>
            </ul>
        </li>
    </ul>
</details>

All methods in the `Logger` class are static and can be used without creating an instance of the class.

You may note that the logging function are also available as static methods in the `Logger` class. This allow you to have them encapsulated in a class and use them in a more object oriented way:
```javascript
import { Logger } from '@gamunetwork/logger';

Logger.info('This is an info message');
Logger.warning('This is a warning message');
Logger.error('This is an error message');
```

## Configuration
You can configure the logger using the `Logger` class. Here is an example of how you can configure the logger:
```javascript
import { Logger, LEVELS, SENSITIVE_LEVELS } from '@gamunetwork/logger';

Logger.setLevel(LEVELS.INFO); // all logs with level less than INFO will be ignored

Logger.setSensitiveLevel(SENSITIVE_LEVELS.HIDE); // If a log message contains sensitive data, it will be hidden

Logger.addSensitiveData('password'); // add 'password' to the list of sensitive data (if a log message contains 'password', it will be hidden)

Logger.setModule('my-module'); // set the module name for this file to 'my-module' (this will be displayed in the log message) (by default, no module name is set)

Logger.setTarget(console.log); // set the target of the logger to console.log (by default, the target is console.log) (can be a function that takes a string as argument, or a filename)
```
> Please note that the logger can be used without any configuration. The default configuration is:
    Level: INFO  
    Sensitive Level: HIDE  
    Sensitive Data: []  
    No module name

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
