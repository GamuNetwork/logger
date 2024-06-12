import { replaceNewLine, getTime, centerString, GetCallerFilePath, splitLongString } from './utils.js';
import { COLORS, LEVELS, SENSITIVE_LEVELS, Target, TARGET_TYPE, TERMINAL_TARGETS } from './customTypes.js';



class Logger{
    static _instance = new Logger();

    private _targets : Target[] = [];
    private _sensitive_data : string[] = [];
    private _module_map : Record<string, string> = {}; // filepath -> module name

    constructor(){
        if(Logger._instance){
            return Logger._instance;
        }
        Logger._instance = this;

        return this;
    }

// ----------------- CONFIGURATION METHODS -----------------

    static setLevel(targetName: string, level: LEVELS.LEVELS){
        let target = Target.get(targetName);
        target.setProperty('level', level);
    }

    static addDefaultTarget(){
        if(!Logger._instance._targets.length){
            Logger.addTarget(TERMINAL_TARGETS.STDOUT);
        }
    }

    static setSensitiveMode(targetName: string, level: SENSITIVE_LEVELS.SENSITIVE_LEVELS){
        let target = Target.get(targetName);
        target.setProperty('sensitiveMode', level);

        if(level === SENSITIVE_LEVELS.SHOW){
            Logger.messageInTarget(target, "Sensitive data may be visible in this file, do not share this file with anyone", COLORS.YELLOW);
        }
    }

    static addTarget(targetSource : string|Function|TERMINAL_TARGETS.TERMINAL_TARGETS, level = LEVELS.INFO, sensitiveMode = SENSITIVE_LEVELS.HIDE){
        let target : Target;
        if(typeof targetSource === 'string'){
            if(Target.exist(targetSource)){
                throw new Error("Target '" + targetSource + "' already exists");
            }
            target = Target.fromFile(targetSource);
        }
        else if(typeof targetSource === 'function' || typeof targetSource === 'number'){
            target = new Target(targetSource);
        }
        else{
            throw new Error("Invalid target source");
        }
        Logger._instance._targets.push(target);
        
        Logger.setLevel(target.name, level);
        Logger.setSensitiveMode(target.name, sensitiveMode);

        return target;
    }

    static addSensitiveData(data: string){
        Logger._instance._sensitive_data.push(data);
    }

    static setModule(moduleName: string){
        if(moduleName.length > 10){
            throw new Error("Module name '" + moduleName + "' is too long");
        }
        Logger._instance._module_map[GetCallerFilePath()] = moduleName;
    }

// ------------------- INTERNAL METHODS --------------------

    private static log(level : LEVELS.LEVELS, message : string, filename : string){
        Logger.addDefaultTarget(); //print to terminal if no target is set
        for(let target of Logger._instance._targets){
            if(target.getProperty('level') <= level){
                let result = "";
                let moduleName = Logger._instance._module_map[filename];
                let indent = 33 + (moduleName ? 15 : 0);
                if(typeof message !== 'string'){
                    message = JSON.stringify(message, null, 4);
                }
                message = splitLongString(message, 100);
                message = replaceNewLine(message, indent);
                message = Logger.parseSensitiveData(message, target);
                if(target.type === TARGET_TYPE.TERMINAL){
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
                result += message + "\n";
                target.call(result);
            }
        }
    }

    private static parseSensitiveData(message : string, target : Target){
        if(target.getProperty('sensitiveMode') === SENSITIVE_LEVELS.HIDE){
            for(let data of Logger._instance._sensitive_data){
                message = message.replace(data, "*".repeat(data.length));
            }
        }
        return message;
    }

    private static messageInTarget(target : Target, message : string, color = COLORS.NONE){
        message = Logger.parseSensitiveData(message, target);
        if(target.type === TARGET_TYPE.TERMINAL){
            target.call(color.toString() + message + COLORS.RESET.toString());
        }
        else{
            target.call(message);
        }
    }

// ------------------ DEBUGGING METHODS --------------------

    static repr(){
        let result = {"targets": [], "SensitiveDatas" : []} as Record<string, any>;
        for(let target of Logger._instance._targets){
            result["targets"].push(target.repr());
        }
        result["SensitiveDatas"] = Logger._instance._sensitive_data;
        result["moduleMap"] = Logger._instance._module_map;
        return result;
    }

    static clear(){
        Logger._instance._targets = [];
        Logger._instance._sensitive_data = [];
        Logger._instance._module_map = {};
        Target.clear();
    }

// ------------------- LOGGING METHODS ---------------------

    static message(message : string, color = COLORS.NONE){
        for(let target of Logger._instance._targets){
            Logger.messageInTarget(target, message, color);
        }
    }

    static deepDebug(message : string, filename = GetCallerFilePath()){
        Logger.log(LEVELS.DEEP_DEBUG, message, filename);
    }

    static debug(message : string, filename = GetCallerFilePath()){
        Logger.log(LEVELS.DEBUG, message, filename);
    }
    
    static info(message : string, filename = GetCallerFilePath()){
        Logger.log(LEVELS.INFO, message, filename);
    }

    static warning(message : string, filename = GetCallerFilePath()){
        Logger.log(LEVELS.WARNING, message, filename);
    }

    static error(message : string, filename = GetCallerFilePath()){
        Logger.log(LEVELS.ERROR, message, filename);
    }

    static critical(message : string, filename = GetCallerFilePath()){
        Logger.log(LEVELS.CRITICAL, message, filename);
    }
}


function deepDebug(message: string){
    Logger.deepDebug(message, GetCallerFilePath());
}

function debug(message : string){
    Logger.debug(message, GetCallerFilePath());
}

function info(message : string){
    Logger.info(message, GetCallerFilePath());
}

function warning(message : string){
    Logger.warning(message, GetCallerFilePath());
}

function error(message : string){
    Logger.error(message, GetCallerFilePath());
}

function critical(message : string){
    Logger.critical(message, GetCallerFilePath());
}

function message(message : string, color = COLORS.NONE){
    Logger.message(message, color);
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
    critical,
    message
}