import fs from 'fs';
import path from 'path';

import { replaceNewLine, getTime, centerString, GetCallerInfo } from './utils.mjs';
import { stdout } from 'process';

class COLORS{
    static RED = new COLORS("\x1b[91m");
    static DARK_RED = new COLORS("\x1b[91m\x1b[1m");
    static GREEN = new COLORS("\x1b[92m");
    static YELLOW = new COLORS("\x1b[93m");
    static BLUE = new COLORS("\x1b[94m");
    static RESET = new COLORS("\x1b[0m");
    static NONE = new COLORS("");

    constructor(code){
        this.code = code;
    }
    toString(){
        return this.code;
    }
}

class LEVELS{
    static DEEP_DEBUG = new LEVELS(0, COLORS.BLUE);
    static DEBUG = new LEVELS(1, COLORS.BLUE);
    static INFO = new LEVELS(2, COLORS.GREEN);
    static WARNING = new LEVELS(3, COLORS.YELLOW);
    static ERROR = new LEVELS(4, COLORS.RED);
    static CRITICAL = new LEVELS(5, COLORS.DARK_RED);

    constructor(level, color){
        this._level = level;
        this._color = color;
    }

    isLowerOrEqual(level){
        return this._level <= level._level;
    }

    toValue(){ // convert to number
        return this._level;
    }

    toString(){
        switch(this._level){
            case 0:
                return "  DEBUG   ";
            case 1:
                return "  DEBUG   ";
            case 2:
                return "   INFO   ";
            case 3:
                return " WARNING  ";
            case 4:
                return "  ERROR   ";
            case 5:
                return " CRITICAL ";
        }
    }

    get color(){
        return this._color;
    }
}

class SENSITIVE_LEVELS{
    HIDE = new SENSITIVE_LEVELS(0);
    ENCODE = new SENSITIVE_LEVELS(1);
    SHOW = new SENSITIVE_LEVELS(2);

    constructor(level){
        this._level = level;
    }
}

class Logger{
    static _instance = new Logger();
    constructor(){
        if(Logger._instance){
            return Logger._instance;
        }
        Logger._instance = this;

        this._level = LEVELS.INFO;
        this._target = console.log; // default target, can be a file path
        this._sensitive_level = SENSITIVE_LEVELS.HIDE;
        this._sensitive_data = [];
        this._module_map = {}; // filepath -> module name

        return this;
    }

// ----------------- CONFIGURATION METHODS -----------------

    static setLevel(level){
        if(!level instanceof LEVELS){
            throw new Error("Invalid level");
        }
        Logger()._level = level;
    }

    static setTarget(target){
        // target can be either a function or a file path; if it's a file path, it will be created if it doesn't exist
        if(typeof target === 'string'){

            // create the file if it doesn't exist, clear it if it does
            if(fs.existsSync(target)){
                fs.unlinkSync(target);
            }
            fs.writeFileSync(target, '');
            Logger._instance._target = (message) => {
                fs.appendFileSync(target, message + '\n');
            }
        }
        else if(typeof target === 'function'){
            Logger._instance._target = target;
        }
        else{
            throw new Error("Invalid target");
        }
    }

    static setSensitiveLevel(level){
        if(!level instanceof SENSITIVE_LEVELS){
            throw new Error("Invalid level");
        }
        Logger._instance._sensitive_level = level;
    }

    static addSensitiveData(data){
        Logger._instance._sensitive_data.push(data);
    }

    static setModule(moduleName){
        if(moduleName.length > 10){
            throw new Error("Module name '" + moduleName + "' is too long");
        }
        Logger._instance._module_map[GetCallerInfo()] = moduleName;
    }

// ------------------- INTERNAL METHODS --------------------

    static #log(level, message, filename){
        if(!level instanceof LEVELS){
            throw new Error("Invalid level");
        }
        if(!Logger._instance._level.isLowerOrEqual(level)){
            return;
        }
        Logger._instance._target(Logger.#format(level, message, filename));
    }

    static colorString(color, message){
        if(Logger._instance._target != console.log){
            return message; // no color support for file output
        }
        return color.toString() + message + COLORS.RESET.toString();
    }

    static #format(level, message, filename){
        let moduleName = Logger._instance._module_map[filename];
        let indent = 33 + (moduleName ? 15 : 0);
        message = replaceNewLine(message, indent);
        let result = `[${Logger.colorString(COLORS.BLUE, getTime())}] [${Logger.colorString(level.color, level.toString())}] `;
        if(moduleName){
            result += `[ ${Logger.colorString(COLORS.BLUE, centerString(moduleName, 10))} ] `;
        }
        result += message;
        return result;
    }

// ------------------- LOGGING METHODS ---------------------

    static message(message, color = COLORS.NONE){
        Logger._instance._target(color.toString() + message + COLORS.RESET.toString());
    }

    static deepDebug(message, filename = GetCallerInfo()){
        Logger.#log(LEVELS.DEEP_DEBUG, message, filename);
    }

    static debug(message, filename = GetCallerInfo()){
        Logger.#log(LEVELS.DEBUG, message, filename);
    }
    
    static info(message, filename = GetCallerInfo()){
        Logger.#log(LEVELS.INFO, message, filename);
    }

    static warning(message, filename = GetCallerInfo()){
        Logger.#log(LEVELS.WARNING, message, filename);
    }

    static error(message, filename = GetCallerInfo()){
        Logger.#log(LEVELS.ERROR, message, filename);
    }

    static critical(message, filename = GetCallerInfo()){
        Logger.#log(LEVELS.CRITICAL, message, filename);
    }
}


function deepDebug(message){
    Logger.deepDebug(message, GetCallerInfo());
}

function debug(message){
    Logger.debug(message, GetCallerInfo());
}

function info(message){
    Logger.info(message, GetCallerInfo());
}

function warning(message){
    Logger.warning(message, GetCallerInfo());
}

function error(message){
    Logger.error(message, GetCallerInfo());
}

function critical(message){
    Logger.critical(message, GetCallerInfo());
}


export {
    Logger,
    COLORS,
    LEVELS,
    SENSITIVE_LEVELS,

    deepDebug,
    debug,
    info,
    warning,
    error,
    critical
}