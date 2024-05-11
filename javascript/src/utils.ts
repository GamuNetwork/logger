

export function replaceNewLine(str : string, indent = 33){ 
    return str.replace(/\n/g, "\n"+" ".repeat(indent)+"| "); // replace all new lines with new line, 4 tabs and a pipe
}

export function getTime(){ //format : "%Y-%m-%d %H:%M:%S"
    return new Date().toISOString().replace(/T/, ' ').replace(/\..+/, '');
}

export function centerString(str: string, length : number) {
    return str.padStart((length-str.length)/2 + str.length).padEnd(length);
}

export function GetCallerInfo(){
    let oldPrepareStackTrace = Error.prepareStackTrace;
    Error.prepareStackTrace = function (err : any, stack : any) { return stack; }
    let stack = new Error().stack;
    Error.prepareStackTrace = oldPrepareStackTrace;
    // @ts-ignore
    return stack[2].getFileName();
}
