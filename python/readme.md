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
<details>
<summary>Logging functions</summary>
    <ul>
        <li><code>deepDebug(message: str) : None</code></li>
        <li><code>debug(message: str) : None</code></li>
        <li><code>info(message: str) : None</code></li>
        <li><code>warning(message: str) : None</code></li>
        <li><code>error(message: str) : None</code></li>
        <li><code>critical(message: str) : None</code></li>
    </ul>
</details>
<details>
<summary>Classes</summary>
    <ul>
        <li><code>Logger</code>
            <ul>
            <li><code>setLevel(targetName: str, level: LEVELS.LEVELS) : None</code></li>
            <li><code>setSensitiveMode(targetName: str, mode: SENSITIVE_LEVELS) : None</code></li>
            <li><code>setModule(name: str) : None</code></li>
            <li><code>addTarget(Callable[[str], None] | str | Target, level : LEVELS, sensitiveMode : SENSITIVE_LEVELS) : None</code></li>
            <li><code>addSensitive(sensitive: Any) : None</code></li>
            <li><code>configArgparse(parser: argparse.ArgumentParser) : None</code></li>
            <li><code>parseArgs(args: argparse.Namespace) : None</code></li>
            <li><code>deepDebug(message: str) : None</code></li>
            <li><code>debug(message: str) : None</code></li>
            <li><code>info(message: str) : None</code></li>
            <li><code>warning(message: str) : None</code></li>
            <li><code>error(message: str) : None</code></li>
            <li><code>critical(message: str) : None</code></li>
            </ul>
        </li>
    </ul>