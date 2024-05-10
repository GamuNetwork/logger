

export function replaceNewLine(str, indent = 33){ 
    return str.replace(/\n/g, "\n"+" ".repeat(indent)+"| "); // replace all new lines with new line, 4 tabs and a pipe
}

export function getTime(){ //format : "%Y-%m-%d %H:%M:%S"
    return new Date().toISOString().replace(/T/, ' ').replace(/\..+/, '');
}

export function centerString(str, length){
    return str.padStart((length-str.length)/2 + str.length).padEnd(length);
}

export function GetCallerInfo(){
    let oldPrepareStackTrace = Error.prepareStackTrace;
    Error.prepareStackTrace = function (err, stack) { return stack; }
    let stack = new Error().stack;
    Error.prepareStackTrace = oldPrepareStackTrace;
    return stack[2].getFileName();
}
