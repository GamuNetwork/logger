import { CallerInfo } from "./customTypes";


export function replaceNewLine(str : string, indent = 33){ 
    return str.replace(/\n/g, "\n"+" ".repeat(indent)+"| "); // replace all new lines with new line, 4 tabs and a pipe
}

export function getTime(){ //format : "%Y-%m-%d %H:%M:%S", take care of the time zone
    let date = new Date();
    return "" + date.getFullYear() + "-" + (date.getMonth()+1).toString().padStart(2, "0") + "-" + date.getDate().toString().padStart(2, "0") + " " + date.getHours().toString().padStart(2, "0") + ":" + date.getMinutes().toString().padStart(2, "0") + ":" + date.getSeconds().toString().padStart(2, "0");
}

export function centerString(str: string, length : number) {
    return str.padStart((length-str.length)/2 + str.length).padEnd(length);
}

// function getCallerFilePath(index : number) : string {
//     let oldPrepareStackTrace = Error.prepareStackTrace;
//     Error.prepareStackTrace = function (_ : any, stack : any) { return stack; }
//     let stack = new Error().stack;
//     Error.prepareStackTrace = oldPrepareStackTrace;
//     // @ts-ignore
//     return stack[index].getFileName();
// }

// function getCallerFunctionName(index : number) : string {
//     let oldPrepareStackTrace = Error.prepareStackTrace;
//     Error.prepareStackTrace = function (_ : any, stack : any) { return stack; }
//     let stack = new Error().stack;
//     Error.prepareStackTrace = oldPrepareStackTrace;
//     // @ts-ignore
//     return stack[index].getFunctionName();
// }

// export function getCallerInfo() : CallerInfo{
//     return [getCallerFunctionName(3), getCallerFilePath(3)];
// }

export function getCallerInfo(index : number = 2) : CallerInfo{
    let oldPrepareStackTrace = Error.prepareStackTrace;
    Error.prepareStackTrace = function (_ : any, stack : any) { return stack; }
    let stack = new Error().stack as any;
    Error.prepareStackTrace = oldPrepareStackTrace;
    return [stack[index].getFunctionName(), stack[index].getFileName()];
}

export function splitLongString(str : string, length : number = 100){
    if(str.length <= length){
        return str;
    }
    let result = [] as string[];
    let words = str.split(" ");
    let line = [] as string[];
    for(let word in words){ 
        if(line.length + words[word].length > length){
            result.push(line.join(" "));
            line = [];
        }
        line.push(words[word]);
    }
    result.push(line.join(" "));
    return result.join("\n");
}
