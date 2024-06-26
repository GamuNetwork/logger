const fs = require('fs');
const packageJson = require('../../package.json');

function int(value){
    return parseInt(value, 10);
}

function sweetMerge(dict1, dict2){
    for (var key in dict2){
        if (dict1.hasOwnProperty(key)){
            if (typeof dict1[key] === 'object' && typeof dict2[key] === 'object'){
                dict1[key] = sweetMerge(dict1[key], dict2[key]);
            } else {
                dict1[key] = dict2[key];
            }
        }
        else {
            dict1[key] = dict2[key];
        }
    }
    return dict1;
}

function exportCodeFile(Filepath, lineNumber, contextLines = 5){
    if(Filepath !== undefined && Filepath !== ""){
        var file = fs.readFileSync(Filepath, 'utf8').split('\n');
        var start = Math.max(0, lineNumber - contextLines);
        var end = Math.min(file.length, int(lineNumber) + int(contextLines));
        var lines = file.slice(start, end);
        let linesWithNumbers = {};
        for (var i = 0; i < lines.length; i++){
            linesWithNumbers[start+i+1] = lines[i];
        }
        return linesWithNumbers;
    }
    return [];
}

function parseStack(stack){ //type: string
    if(stack !== undefined && stack !== ""){
        stack = stack.split("    at");

        var newStack = [];

        for (var i = 1; i < stack.length; i++){
            var line = stack[i].replace(/\n/g, "")
            //find if the line contain a file path
            var filePath = line.match(/((\/|[A-Z]).*\.js):([0-9]*):([0-9]*)/);
            if(filePath !== null){
                let tokens = filePath[0].split(":");
                newStack.push({
                    columnNumber: tokens[tokens.length-1],
                    lineNumber: tokens[tokens.length-2],
                    filePath: tokens.slice(0, tokens.length-2).join(":").split("(")[1]
                });
            }
        }
        return newStack;
    }
    return [];
}


function getOS(){
    switch(process.platform){
        case 'win32':
            return 'windows';
        case 'darwin':
            return 'macos';
        case 'linux':
            return 'ubuntu';
        default:
            return "Unknown OS"
    }
}

const JsonExporter = function(outputFile){

    var suites = {};
    var orphans = {
        passed: 0,
        failed: 0,
        pending: 0,
        skipped: 0,
        duration: 0,
        specs: {}
    };

    var FilesToExport = {};

    var summary = {
        appName: packageJson.name,
        appVersion: packageJson.version,
        os: getOS(),
        specs: 0,
        failures: 0,
        passed: 0,
        pending: 0,
        skipped: 0,
        duration: 0,
        startDate: new Date().toISOString()
    };

    this.suiteStarted = function(suiteInfo) {
        suites[suiteInfo.id] = sweetMerge(suiteInfo, {passed: 0, failed: 0, pending: 0, skipped: 0, duration: 0, specs: {}});
    }

    this.specDone = function(result) {
        parentSuite = null;

        const cloneResult = structuredClone(result);

        if(cloneResult.parentSuiteId){
            parentSuite = suites[cloneResult.parentSuiteId]
        }
        else{
            parentSuite = orphans;
        }

        parentSuite.specs[cloneResult.id] = cloneResult;

        passedExpectations = parentSuite.specs[cloneResult.id].passedExpectations;
        failedExpectations = parentSuite.specs[cloneResult.id].failedExpectations;
        for (var i = 0; i < passedExpectations.length; i++){
            passedExpectations[i].stack = parseStack(passedExpectations[i].stack);
        }
        for (var i = 0; i < failedExpectations.length; i++){
            let stack = parseStack(failedExpectations[i].stack);
            failedExpectations[i].stack = stack;
            for (var j = 0; j < stack.length; j++){
                let lines = exportCodeFile(stack[j].filePath, stack[j].lineNumber);
                FilesToExport[stack[j].filePath+":"+stack[j].lineNumber] = lines;
            }
        }

        summary.specs++;
        summary.duration += cloneResult.duration;
        parentSuite.duration += cloneResult.duration;

        if(cloneResult.pendingReason === 'Temporarily disabled with xit'){
            summary.skipped++;
            parentSuite.skipped++;
        }
        else if(cloneResult.status === 'failed'){
            summary.failures++;
            parentSuite.failed++;
        }
        else if(cloneResult.status === 'pending'){
            summary.pending++;
            parentSuite.pending++;
        }
        else{
            summary.passed++;
            parentSuite.passed++;
        }
    }
    
    this.suiteDone = function(result) {
        let SuiteSpecs = {};
        for (let spec in suites[result.id].specs){
            SuiteSpecs[spec] = suites[result.id].specs[spec];
        }
        suites[result.id].specs = SuiteSpecs;
        suites[result.id] =
        sweetMerge(suites[result.id], result)
    }

    this.jasmineDone = function(suiteInfo) {
        fs.writeFileSync(outputFile, JSON.stringify({
            summary: summary,
            suites: suites,
            orphans: orphans,
            files: FilesToExport
        }, null, 4));
    }
};

reporter = new JsonExporter(getOS()+".report.json");

jasmine.getEnv().addReporter(reporter);