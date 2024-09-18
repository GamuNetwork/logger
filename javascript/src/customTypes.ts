import * as fs from 'fs';

import { XMLParser, XMLValidator} from "fast-xml-parser";
XMLValidator;

export type CallerInfo = [string, string];

export class Module{
    private static instances = {} as Record<string, Module>;

    private name : string;
    private parent : Module|null;
    private file : string;
    private func : string;

    constructor(name : string, parent : Module|null = null, file : string, func : string){
        this.name = name;
        this.parent = parent;
        this.file = file;
        this.func = func;

        Module.instances[file+": "+func] = this;
    }

    getCompleteName() : string{
        return this.parent ? this.parent.getCompleteName() + "." + this.name : this.name;
    }

    getCompletePath() : string[]{
        return this.parent ? this.parent.getCompletePath().concat([this.name]) : [this.name];
    }

    static get([func, file] : CallerInfo) : Module{
        if (Module.exist([func, file])){
            return Module.instances[file+": "+func];
        }
        else{
            throw new Error("No module found for file '"+file+"' and function '"+func+"'");
        }
    }

    static exist([func, file] : CallerInfo) : boolean{
        return Module.instances[file+": "+func] != null;
    }

    static delete([func, file] : CallerInfo){
        if (Module.exist([func, file])){
            delete Module.instances[file+": "+func];
        }
        else{
            throw new Error("No module found for file '"+file+"' and function '"+func+"'");
        }
    }

    static getByName(name : string) : Module{
        for (let key in Module.instances){
            if (Module.instances[key].getCompleteName() == name){
                return Module.instances[key];
            }
        }
        throw new Error("No module found for name '"+name+"'");
    }

    static existByName(name : string) : boolean{
        for (let key in Module.instances){
            if (Module.instances[key].getCompleteName() == name){
                return true;
            }
        }
        return false;
    }

    static deleteByName(name : string){
        for (let key in Module.instances){
            if (Module.instances[key].getCompleteName() == name){
                delete Module.instances[key];
                return;
            }
        }
        throw new Error("No module found for name '"+name+"'");
    }

    static clear(){
        Module.instances = {};
    }

    static new(name : string, [func, file] : CallerInfo) : Module{
        if (Module.existByName(name)){
            let existing = Module.getByName(name);
            if (existing.file == file && existing.func == func){
                return existing;
            }
            else{
                throw new Error("Module '"+name+"' already exists with file '"+existing.file+"' and function '"+existing.func+"'");
            }
        }

        if (name.includes(".")){
            let [parentName, moduleName] = name.split('.').reverse();
            if (Module.existByName(parentName)){
                let parent = Module.getByName(parentName);
                return new Module(moduleName, parent, file, func);
            }
            else{
                throw new Error("Parent module '"+parentName+"' not found for module '"+name+"'");
            }
        }

        return new Module(name, null, file, func);
    }

    static getNameList() : string[]{
        return Object.values(Module.instances).map(module => module.getCompleteName());
    }
}

export namespace COLORS{
    export enum COLORS{
        RED = "\x1b[91m",
        DARK_RED = "\x1b[91m\x1b[1m",
        GREEN = "\x1b[92m",
        YELLOW = "\x1b[93m",
        BLUE = "\x1b[94m",
        RESET = "\x1b[0m",
        NONE = ""
    }

    export const RED = COLORS.RED;
    export const DARK_RED = COLORS.DARK_RED;
    export const GREEN = COLORS.GREEN;
    export const YELLOW = COLORS.YELLOW;
    export const BLUE = COLORS.BLUE;
    export const RESET = COLORS.RESET;
    export const NONE = COLORS.NONE;

    export function fromString(color : string){
        switch(color.toLowerCase()){
            case "red":
                return COLORS.RED;
            case "dark_red":
                return COLORS.DARK_RED;
            case "green":
                return COLORS.GREEN;
            case "yellow":
                return COLORS.YELLOW;
            case "blue":
                return COLORS.BLUE;
            case "reset":
                return COLORS.RESET;
            case "none":
                return COLORS.NONE;
            default:
                throw new Error("Invalid color : " + color);
        }
    }

    export function toString(color : COLORS){
        switch(color){
            case COLORS.RED:
                return "red";
            case COLORS.DARK_RED:
                return "dark_red";
            case COLORS.GREEN:
                return "green";
            case COLORS.YELLOW:
                return "yellow";
            case COLORS.BLUE:
                return "blue";
            case COLORS.RESET:
                return "reset";
            case COLORS.NONE:
                return "none";
        }
    }
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

    export function fromString(level : string){
        switch(level.toLowerCase()){
            case "deep_debug":
                return LEVELS.DEEP_DEBUG;
            case "debug":
                return LEVELS.DEBUG;
            case "info":
                return LEVELS.INFO;
            case "warning":
                return LEVELS.WARNING;
            case "error":
                return LEVELS.ERROR;
            case "critical":
                return LEVELS.CRITICAL;
            default:
                throw new Error("Invalid level : " + level);
        }
    }
}

export namespace SENSITIVE_LEVELS{
    export enum SENSITIVE_LEVELS{
        HIDE = 10,
        SHOW
    }

    export const HIDE = SENSITIVE_LEVELS.HIDE;
    export const SHOW = SENSITIVE_LEVELS.SHOW;
}

export namespace TARGET_TYPE{
    export enum TARGET_TYPE{
        FILE = 20,
        TERMINAL
    }

    export const FILE = TARGET_TYPE.FILE;
    export const TERMINAL = TARGET_TYPE.TERMINAL;
}

export namespace TERMINAL_TARGETS{
    export enum TERMINAL_TARGETS{
        STDOUT = 30,
        STDERR
    }

    export const STDOUT = TERMINAL_TARGETS.STDOUT;
    export const STDERR = TERMINAL_TARGETS.STDERR;

    export function fromString(target : string){
        switch(target.toLowerCase()){
            case "stdout":
                return TERMINAL_TARGETS.STDOUT;
            case "stderr":
                return TERMINAL_TARGETS.STDERR;
            default:
                throw new Error("Invalid terminal target : " + target);
        }
    }

    export function toString(target : TERMINAL_TARGETS){
        switch(target){
            case TERMINAL_TARGETS.STDOUT:
                return "stdout";
            case TERMINAL_TARGETS.STDERR:
                return "stderr";
            default:
                throw new Error("Invalid terminal target : " + target);
        }
    }
}

export class Target{
    private static instances : Record<string, Target> = {};
    private _target : Function = (_ : string) => {};
    private _name : string = "";
    private _properties : Record<string, any> = {};
    private _type : TARGET_TYPE.TARGET_TYPE = TARGET_TYPE.FILE;


    constructor(target: Function | TERMINAL_TARGETS.TERMINAL_TARGETS, name: string|null = null){
        if(typeof target == 'function'){
            this._name = name || target.name;
            this._target = target;
            this._type = TARGET_TYPE.FILE;
        }
        else if(typeof target == 'string'){
            throw new Error("Invalid target; use Target.fromFile to create a file target");
        }
        else{
            this._name = name || TERMINAL_TARGETS.toString(target);
            this._type = TARGET_TYPE.TERMINAL;
            switch(target){
                case TERMINAL_TARGETS.STDOUT:
                    this._target = process.stdout.write.bind(process.stdout);
                    break;
                case TERMINAL_TARGETS.STDERR:
                    this._target = process.stderr.write.bind(process.stderr);
                    break;
                default:
                    throw new Error("Invalid target : " + target);
            }
        }

        if(Target.instances[this._name]){
            return Target.instances[this._name];
        }

        Target.instances[this._name] = this;
    }

    static fromFile(path: string){
        fs.writeFileSync(path, "");
        const func = (message : string) => {
            fs.appendFileSync(path, message + '\n');
        }
        return new Target(func, path);
    }

    /*
        examples of json data:
        File:
        ```json
        {
            "file": "log.txt",
            "level": "info",
            "sensitiveMode": "hide"
        }
        ```
        Stdout (console):
        ```json	
        {
            "name": "stdout",
            "terminal": "stdout"
        }
        ```
    */
    static fromJson(data: string|Record<string, any>){
        let obj = typeof data === 'string' ? JSON.parse(data) : data;
        
        let result = null as Target|null;

        if('file' in obj){
            result = Target.fromFile(obj.file);
        }
        else if('terminal' in obj){
            result = new Target(TERMINAL_TARGETS.fromString(obj.terminal));
        }
        else{
            throw new Error("The target must be a file or a terminal");
        }

        if('name' in obj){
            result.name = obj.name;
        }
        result.setProperty('level', LEVELS.fromString(obj.level) || LEVELS.INFO);
        result.setProperty('sensitiveMode', obj.sensitiveMode || SENSITIVE_LEVELS.HIDE);

        return result;
    }

    /*
        examples of xml data:
        File:
        ```xml
        <target level="info" sensitiveMode="hide" file="log.txt"/>
        ```
        Stdout (console):
        ```xml
        <target name="stdout" terminal="stdout"/>
        ```
    */
    static fromXml(data: string|Record<string, any>){
        const parser = new XMLParser({attributeNamePrefix : "µ_", ignoreAttributes : false});
        const obj = typeof data === 'string' ? parser.parse(data) : data;
        
        let result = null as Target|null;

        if(!obj.target){
            throw new Error("the root element must be 'target'");
        }

        if(obj.target.µ_file){
            result = Target.fromFile(obj.target.µ_file);
        }
        else if(obj.target.µ_terminal){
            result = new Target(TERMINAL_TARGETS.fromString(obj.target.µ_terminal));
        }
        else{
            throw new Error("The target must be a file or a terminal");
        }

        if(obj.target.µ_name){
            result.name = obj.target.µ_name;
        }
        result.setProperty('level', obj.target.µ_level ? LEVELS.fromString(obj.target.µ_level) : LEVELS.INFO);
        result.setProperty('sensitiveMode', obj.target.µ_sensitiveMode || SENSITIVE_LEVELS.HIDE);
    
        return result;
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

    static list(){
        return Object.keys(Target.instances);
    }

    static clear(){
        Target.instances = {};
    }
}

export class LoggerConfig{
    public sensitiveDatas : string[] = [];
    public targets : Target[] = [];

    constructor(sensitiveDatas : string[] = [], targets : Target[] = []){
        this.sensitiveDatas = sensitiveDatas;
        this.targets = targets;
    }

    public clear(){
        this.sensitiveDatas = [];
        this.targets = [];
    }

    /*
    examples of json data:
    ```json
    {
        "sensitiveDatas": ["password", "token"],
        "targets": [
            {
                "file": "log.txt",
                "level": "info",
                "sensitiveMode": "hide"
            },
            {
                "name": "stdout",
                "terminal": "stdout"
            }
        ]
    }
    */
    public static fromJson(data: string|Record<string, any>){
        let obj = typeof data === 'string' ? JSON.parse(data) : data;
        
        let sensitiveDatas = obj.sensitiveDatas || [];
        let targets = obj.targets ? obj.targets.map((target : any) => Target.fromJson(target)) : [];

        return new LoggerConfig(sensitiveDatas, targets);
    }

    /*
    examples of xml data:
    ```xml
    examples of xml data:
    ```xml
    <config>
        <sensitiveDatas>
            <data>password</data>
            <data>token</data>
        </sensitiveDatas>
        <targets>
            <target file='log.txt' level='info' sensitiveMode='hide'/>
            <target terminal='stdout' name='stdout'/>
        </targets>
    </config>
    ```
    */
    public static fromXml(data: string|Record<string, any>){
        const parser = new XMLParser({attributeNamePrefix : "µ_", ignoreAttributes : false});
        const obj = typeof data === 'string' ? parser.parse(data) : data;
        
        let sensitiveDatas = obj.config.µ_sensitiveDatas ? obj.config.µ_sensitiveDatas.map((data : any) => data.µ_data) : [];
        let targets = obj.config.µ_targets ? obj.config.µ_targets.map((target : any) => Target.fromXml(target)) : [];

        return new LoggerConfig(sensitiveDatas, targets);
    }

    public static fromConfigFile(path: string){
        if(!fs.existsSync(path)){
            throw new Error("Config file not found");
        }
        if(path.endsWith(".json")){
            return LoggerConfig.fromJson(fs.readFileSync(path, 'utf8'));
        }
        else if(path.endsWith(".xml")){
            return LoggerConfig.fromXml(fs.readFileSync(path, 'utf8'));
        }
        else{
            throw new Error("The file must be a json or xml file");
        }
    }

    public toString(){
        return "LoggerConfig(sensitiveDatas=[" + this.sensitiveDatas.join(", ") + "], targets=[" + this.targets.map(target => target.toString()).join(", ") + "])";
    }
}
