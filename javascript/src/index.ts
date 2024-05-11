import * as fs from 'fs';

import { replaceNewLine, getTime, centerString, GetCallerInfo } from './utils.js';

enum COLORS{
    RED = "\x1b[91m",
    DARK_RED = "\x1b[91m\x1b[1m",
    GREEN = "\x1b[92m",
    YELLOW = "\x1b[93m",
    BLUE = "\x1b[94m",
    RESET = "\x1b[0m",
    NONE = ""
}

enum LEVELS{
    DEEP_DEBUG = 0,
    DEBUG = 1,
    INFO = 2,
    WARNING = 3,
    ERROR = 4,
    CRITICAL = 5
}

namespace LEVELS{
    export function toString(level : LEVELS){
        switch(level){
            case LEVELS.DEEP_DEBUG:
            case LEVELS.DEBUG:
                return "  DEBUG   ";
            case LEVELS.INFO:
                return "   INFO   ";
            case LEVELS.WARNING:
                return " WARNING  ";
            case LEVELS.ERROR:
                return "  ERROR   ";
            case LEVELS.CRITICAL:
                return " CRITICAL ";
        }
    }

    export function getColor(level : LEVELS){
        switch(level){
            case 0:
            case 1:
                return COLORS.BLUE;
            case 2:
                return COLORS.GREEN;
            case 3:
                return COLORS.YELLOW;
            case 4:
                return COLORS.RED;
            case 5:
                return COLORS.DARK_RED;
            default:
                return COLORS.NONE;
        }
    }
}

enum SENSITIVE_LEVELS{
    HIDE,
    ENCODE,
    SHOW
}

class Logger{
    static _instance = new Logger();

    private _level : LEVELS = LEVELS.INFO;
    private _target : Function = console.log;
    private _sensitive_level : SENSITIVE_LEVELS = SENSITIVE_LEVELS.HIDE;
    private _sensitive_data : string[] = [];
    private _module_map : Record<string, string> = {};

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

    static setLevel(level: LEVELS){
        Logger._instance._level = level;
    }

    static setTarget(target: any){
        // target can be either a function or a file path; if it's a file path, it will be created if it doesn't exist
        if(target instanceof String){
            // create the file if it doesn't exist, clear it if it does
            let path = target.toString();
            if(fs.existsSync(path)){
                fs.unlinkSync(path);
            }
            fs.writeFileSync(path, '');
            Logger._instance._target = (message : string) => {
                fs.appendFileSync(path, message + '\n');
            }
        }
        else if(target instanceof Function){
            Logger._instance._target = target;
        }
        else{
            throw new Error("Invalid target type");
        }
    }

    static setSensitiveLevel(level: SENSITIVE_LEVELS){
        Logger._instance._sensitive_level = level;
    }

    static addSensitiveData(data: string){
        Logger._instance._sensitive_data.push(data);
    }

    static setModule(moduleName: string){
        if(moduleName.length > 10){
            throw new Error("Module name '" + moduleName + "' is too long");
        }
        Logger._instance._module_map[GetCallerInfo()] = moduleName;
    }

// ------------------- INTERNAL METHODS --------------------

    static #log(level : LEVELS, message : string, filename : string){
        if(Logger._instance._level <= level){
        Logger._instance._target(Logger.#format(level, message, filename));
        }
    }

    static colorString(color : COLORS, message : string){
        if(Logger._instance._target != console.log){
            return message; // no color support for file output
        }
        return color.toString() + message + COLORS.RESET.toString();
    }

    static #format(level : LEVELS, message : string, filename : string){
        let moduleName = Logger._instance._module_map[filename];
        let indent = 33 + (moduleName ? 15 : 0);
        message = replaceNewLine(message, indent);
        let result = `[${Logger.colorString(COLORS.BLUE, getTime())}] [${Logger.colorString(LEVELS.getColor(level), LEVELS.toString(level))}] `;
        if(moduleName){
            result += `[ ${Logger.colorString(COLORS.BLUE, centerString(moduleName, 10))} ] `;
        }
        result += message;
        return result;
    }

// ------------------- LOGGING METHODS ---------------------

    static message(message : string, color = COLORS.NONE){
        Logger._instance._target(color.toString() + message + COLORS.RESET.toString());
    }

    static deepDebug(message : string, filename = GetCallerInfo()){
        Logger.#log(LEVELS.DEEP_DEBUG, message, filename);
    }

    static debug(message : string, filename = GetCallerInfo()){
        Logger.#log(LEVELS.DEBUG, message, filename);
    }
    
    static info(message : string, filename = GetCallerInfo()){
        Logger.#log(LEVELS.INFO, message, filename);
    }

    static warning(message : string, filename = GetCallerInfo()){
        Logger.#log(LEVELS.WARNING, message, filename);
    }

    static error(message : string, filename = GetCallerInfo()){
        Logger.#log(LEVELS.ERROR, message, filename);
    }

    static critical(message : string, filename = GetCallerInfo()){
        Logger.#log(LEVELS.CRITICAL, message, filename);
    }
}


function deepDebug(message: string){
    Logger.deepDebug(message, GetCallerInfo());
}

function debug(message : string){
    Logger.debug(message, GetCallerInfo());
}

function info(message : string){
    Logger.info(message, GetCallerInfo());
}

function warning(message : string){
    Logger.warning(message, GetCallerInfo());
}

function error(message : string){
    Logger.error(message, GetCallerInfo());
}

function critical(message : string){
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