import { replaceNewLine, getTime, centerString, getCallerInfo, splitLongString } from './utils.js';
import { COLORS, LEVELS, SENSITIVE_LEVELS, Target, TARGET_TYPE, TERMINAL_TARGETS, LoggerConfig, Module, CallerInfo } from './customTypes.js';



class Logger{
    static _instance = new Logger();

    private config : LoggerConfig = new LoggerConfig();

    constructor(){
        if(Logger._instance){
            return Logger._instance;
        }
        Logger._instance = this;

        Logger.addTarget(TERMINAL_TARGETS.STDOUT, LEVELS.INFO, SENSITIVE_LEVELS.HIDE);

        return this;
    }

// ----------------- CONFIGURATION METHODS -----------------

    static setLevel(targetName: string, level: LEVELS.LEVELS){
        let target = Target.get(targetName);
        target.setProperty('level', level);
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
        Logger._instance.config.targets.push(target);
        
        Logger.setLevel(target.name, level);
        Logger.setSensitiveMode(target.name, sensitiveMode);

        return target;
    }

    static addSensitiveData(data: string){
        Logger._instance.config.sensitiveDatas.push(data);
    }

    static setModule(moduleName: string){
        if(moduleName.length > 10){
            throw new Error("Module name '" + moduleName + "' is too long");
        }
        // Logger._instance._module_map[GetCallerFilePath()] = moduleName;
        Module.new(moduleName, getCallerInfo());
    }

// ------------------- INTERNAL METHODS --------------------

    private static log(level : LEVELS.LEVELS, message : string, callerInfo : CallerInfo){
        for(let target of Logger._instance.config.targets){
            if(target.getProperty('level') <= level){
                let result = "";
                message = splitLongString(message, 100);
                if(target.type === TARGET_TYPE.TERMINAL){
                    result = `[${COLORS.BLUE.toString()}${getTime()}${COLORS.RESET.toString()}] [${LEVELS.getColor(level)}${LEVELS.toString(level)}${COLORS.RESET.toString()}] `;
                }
                else{
                    result = `[${getTime()}] [${LEVELS.toString(level)}] `;
                }

                if(Module.exist(callerInfo)){
                    let modules = Module.get(callerInfo).getCompletePath();
                    const indent = 33 + 15 * modules.length;
                    message = replaceNewLine(message, indent);
                    message = Logger.parseSensitiveData(message, target);
                    
                    if(target.type === TARGET_TYPE.TERMINAL){
                        for(let i = 0; i < modules.length; i++){
                            result += `[ ${COLORS.BLUE.toString()}${centerString(modules[i], 15)}${COLORS.RESET.toString()} ] `;
                        }
                    }
                    else{
                        for(let i = 0; i < modules.length; i++){
                            result += `[ ${centerString(modules[i], 15)} ] `;
                        }
                    }
                }
                result += message + "\n";
                target.call(result);
            }
        }
    }

    private static parseSensitiveData(message : string, target : Target){
        if(target.getProperty('sensitiveMode') === SENSITIVE_LEVELS.HIDE){
            for(let data of Logger._instance.config.sensitiveDatas){
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
        for(let target of Logger._instance.config.targets){
            result["targets"].push(target.repr());
        }
        result["SensitiveDatas"] = Logger._instance.config.sensitiveDatas;
        result["moduleMap"] = Module.getNameList();
        return result;
    }

    static reset(){
        Logger._instance.config.clear();
        Module.clear();
        Target.clear();
    }

// ------------------- LOGGING METHODS ---------------------

    static message(message : string, color = COLORS.NONE){
        for(let target of Logger._instance.config.targets){
            Logger.messageInTarget(target, message, color);
        }
    }

    static deepDebug(message : string, callerInfo = getCallerInfo()){
        Logger.log(LEVELS.DEEP_DEBUG, message, callerInfo);
    }

    static debug(message : string, callerInfo = getCallerInfo()){
        Logger.log(LEVELS.DEBUG, message, callerInfo);
    }
    
    static info(message : string, callerInfo = getCallerInfo()){
        Logger.log(LEVELS.INFO, message, callerInfo);
    }

    static warning(message : string, callerInfo = getCallerInfo()){
        Logger.log(LEVELS.WARNING, message, callerInfo);
    }

    static error(message : string, callerInfo = getCallerInfo()){
        Logger.log(LEVELS.ERROR, message, callerInfo);
    }

    static critical(message : string, callerInfo = getCallerInfo()){
        Logger.log(LEVELS.CRITICAL, message, callerInfo);
    }
}


function deepDebug(message: string){
    Logger.deepDebug(message, getCallerInfo());
}

function debug(message : string){
    Logger.debug(message, getCallerInfo());
}

function info(message : string){
    Logger.info(message, getCallerInfo());
}

function warning(message : string){
    Logger.warning(message, getCallerInfo());
}

function error(message : string){
    Logger.error(message, getCallerInfo());
}

function critical(message : string){
    Logger.critical(message, getCallerInfo());
}

function message(message : string, color = COLORS.NONE){
    Logger.message(message, color);
}

new Logger(); //initialize the logger

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