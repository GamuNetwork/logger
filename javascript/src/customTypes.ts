import * as fs from 'fs';
import { json } from 'stream/consumers';

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
    export let DEEP_DEBUG = LEVELS.DEEP_DEBUG;
    export let DEBUG = LEVELS.DEBUG;
    export let INFO = LEVELS.INFO;
    export let WARNING = LEVELS.WARNING;
    export let ERROR = LEVELS.ERROR;
    export let CRITICAL = LEVELS.CRITICAL;

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
    HIDE,
    SHOW
}

export enum TargetType{
    FILE,
    TERMINAL
}

export class Target{
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