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

namespace LEVELS{
    export enum LEVELS {
        DEEP_DEBUG = 0,
        DEBUG = 1,
        INFO = 2,
        WARNING = 3,
        ERROR = 4,
        CRITICAL = 5
    }

    export function name(level : LEVELS){
        switch(level){
            case LEVELS.DEEP_DEBUG:
                return "DEEP_DEBUG";
            case LEVELS.DEBUG:
                return "DEBUG";
            case LEVELS.INFO:
                return "INFO";
            case LEVELS.WARNING:
                return "WARNING";
            case LEVELS.ERROR:
                return "ERROR";
            case LEVELS.CRITICAL:
                return "CRITICAL";
        }
        
    }

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

enum TargetType{
    FILE,
    TERMINAL
}

class Target{
    private static instances : Record<string, Target> = {};
    private _target : Function = (x : string) => {};
    private _name : string = "";
    private _properties : Record<string, any> = {};
    private _type : TargetType = TargetType.FILE;


    constructor(targetFunc: Function, name: string|null = null){
        if(name == null){
            name = targetFunc.name;
        }
        if(Target.instances[name]){
            return Target.instances[name];
        }

        this._target = targetFunc;
        this._name = name;
        if(targetFunc === console.log){
            this._type = TargetType.TERMINAL;
        }
        else{
            this._type = TargetType.FILE;
        }

        Target.instances[name] = this;
    }

    static fromFile(path: string){
        fs.writeFileSync(path, "");
        return new Target((message : string) => {
            fs.appendFileSync(path, message + '\n');
        }, path);
    }

    call(message: string){
        this._target(message);
    }

    toString(){
        return this._name;
    }

    getProperty(key: string){
        return this._properties[key];
    }

    setProperty(key: string, value: any){
        this._properties[key] = value;
    }

    get type(){
        return this._type;
    }

    static get(targetName: string){
        if(Target.instances[targetName]){
            return Target.instances[targetName];
        }
        throw new Error("Target '" + targetName + "' not found");
    }

    static exist(targetName: string){
        return Target.instances[targetName] != null;
    }
}

class Logger{
    static _instance = new Logger();

    // private _level : LEVELS.LEVELS = LEVELS.LEVELS.INFO;
    // private _target : Function = console.log;
    private _targets : Target[] = [];
    private _sensitive_level : SENSITIVE_LEVELS = SENSITIVE_LEVELS.HIDE;
    private _sensitive_data : string[] = [];
    private _module_map : Record<string, string> = {}; // filepath -> module name

    constructor(){
        if(Logger._instance){
            return Logger._instance;
        }
        Logger._instance = this;

        Logger._instance._targets.push(new Target(console.log, "terminal"));
        Target.get("terminal").setProperty('level', LEVELS.LEVELS.INFO);

        return this;
    }

// ----------------- CONFIGURATION METHODS -----------------

    static setLevel(targetName: string, level: LEVELS.LEVELS){
        let target = Target.get(targetName);
        target.setProperty('level', level);
    }

    static addTarget(targetSource : string|Function){
        let target : Target;
        if(typeof targetSource === 'string'){
            if(Target.exist(targetSource)){
                throw new Error("Target '" + targetSource + "' already exists");
            }
            target = Target.fromFile(targetSource);
        }
        else if(typeof targetSource === 'function'){
            target = new Target(targetSource);
        }
        else{
            throw new Error("Invalid target source");
        }
        Logger._instance._targets.push(target);
        target.setProperty('level', LEVELS.LEVELS.INFO);
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

    private static log(level : LEVELS.LEVELS, message : string, filename : string){
        for(let target of Logger._instance._targets){
            console.log(target.toString(), target.getProperty('level'), level);
            if(target.getProperty('level') <= level){
                let result = "";
                let moduleName = Logger._instance._module_map[filename];
                let indent = 33 + (moduleName ? 15 : 0);
                message = replaceNewLine(message, indent);
                if(target.type === TargetType.TERMINAL){
                    result = `[${COLORS.BLUE.toString()}${getTime()}${COLORS.RESET.toString()}] [${LEVELS.getColor(level)}${LEVELS.toString(level)}${COLORS.RESET.toString()}] `;
                    if(moduleName){
                        result += `[ ${COLORS.BLUE.toString()}${centerString(moduleName, 10)}${COLORS.RESET.toString()} ] `;
                    }
                }
                else{
                    //same as terminal but without colors
                    result = `[${getTime()}] [${LEVELS.toString(level)}] `;
                    if(moduleName){
                        result += `[ ${centerString(moduleName, 10)} ] `;
                    }
                }
                result += message;
                target.call(result);
            }
        }
    }

// ------------------- LOGGING METHODS ---------------------

    static message(message : string, color = COLORS.NONE){
        for(let target of Logger._instance._targets){
            if(target.type === TargetType.TERMINAL){
                target.call(color.toString() + message + COLORS.RESET.toString());
            }
            else{
                target.call(message);
            }
        }
    }

    static deepDebug(message : string, filename = GetCallerInfo()){
        Logger.log(LEVELS.LEVELS.DEEP_DEBUG, message, filename);
    }

    static debug(message : string, filename = GetCallerInfo()){
        Logger.log(LEVELS.LEVELS.DEBUG, message, filename);
    }
    
    static info(message : string, filename = GetCallerInfo()){
        Logger.log(LEVELS.LEVELS.INFO, message, filename);
    }

    static warning(message : string, filename = GetCallerInfo()){
        Logger.log(LEVELS.LEVELS.WARNING, message, filename);
    }

    static error(message : string, filename = GetCallerInfo()){
        Logger.log(LEVELS.LEVELS.ERROR, message, filename);
    }

    static critical(message : string, filename = GetCallerInfo()){
        Logger.log(LEVELS.LEVELS.CRITICAL, message, filename);
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