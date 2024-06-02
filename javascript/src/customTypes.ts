import * as fs from 'fs';

export enum COLORS{
    RED = "\x1b[91m",
    DARK_RED = "\x1b[91m\x1b[1m",
    GREEN = "\x1b[92m",
    YELLOW = "\x1b[93m",
    BLUE = "\x1b[94m",
    RESET = "\x1b[0m",
    NONE = ""
}

export namespace LEVELS{
    export enum LEVELS {
        DEEP_DEBUG = 0,
        DEBUG = 1,
        INFO = 2,
        WARNING = 3,
        ERROR = 4,
        CRITICAL = 5
    }

    //expose the content of the enum for easy access (LEVELS.DEBUG instead of LEVELS.LEVELS.DEBUG)
    export const DEEP_DEBUG = LEVELS.DEEP_DEBUG;
    export const DEBUG = LEVELS.DEBUG;
    export const INFO = LEVELS.INFO;
    export const WARNING = LEVELS.WARNING;
    export const ERROR = LEVELS.ERROR;
    export const CRITICAL = LEVELS.CRITICAL;

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

export enum SENSITIVE_LEVELS{
    HIDE = 10,
    SHOW
}

export enum TargetType{
    FILE = 20,
    TERMINAL
}

export enum TerminalTargets{
    STDOUT = 30,
    STDERR
}

export class Target{
    private static instances : Record<string, Target> = {};
    private _target : Function = (_ : string) => {};
    private _name : string = "";
    private _properties : Record<string, any> = {};
    private _type : TargetType = TargetType.FILE;


    constructor(targetFunc: Function | TerminalTargets, name: string|null = null){

        if(typeof targetFunc == 'number'){
            switch(targetFunc){
                case TerminalTargets.STDOUT:
                    targetFunc = process.stdout.write.bind(process.stdout);
                    break;
                case TerminalTargets.STDERR:
                    targetFunc = process.stderr.write.bind(process.stderr);
                    break;
                default:
                    throw new Error("Invalid target");
            }
            if(name == null){
                name = "terminal";
            }

            this._type = TargetType.TERMINAL;

        }
        else{
            if(name == null){
                name = targetFunc.name;
            }

            this._type = TargetType.FILE;
        }

        this._target = targetFunc;
        this._name = name;
        if(Target.instances[name]){
            return Target.instances[name];
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

    repr(){
        return {
            "name": this._name,
            "type": this._type,
            "properties": this._properties
        };
    }

    set name(name: string){
        let oldName = this._name;
        this._name = name;
        Target.instances[name] = this;
        delete Target.instances[oldName];

    }
    
    get name(){
        return this._name;
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