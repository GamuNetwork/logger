// import { info, warning, error, debug, Logger } from '@gamunetwork/logger';
import { info, critical, error, debug, Logger, LEVELS } from '../../dist/index.js';

function addNumbers(a, b) {
    debug('Adding numbers '+ a + ' and ' + b);
    let result = a + b;
    debug('Result '+ result);
    return result;
}

function subtractNumbers(a, b) {
    debug('Subtracting numbers '+ a + ' and ' + b);
    let result = a - b;
    debug('Result '+ result);
    return result;
}

function multiplyNumbers(a, b) {
    debug('Multiplying numbers '+ a + ' and ' + b);
    let result = a * b;
    debug('Result '+ result);
    return result;
}

function divideNumbers(a, b) {
    debug('Dividing numbers '+ a + ' and ' + b);
    if (b === 0) {
        error('Invalid operation: Cannot divide by zero');
        throw new Error('Invalid operation: Cannot divide by zero')
    }
    let result = a / b;
    debug('Result '+ result);
    return result;
}


function parseArguments() {
    //  expect a, operator, b and optional debug flag
    if (process.argv.length < 5) { // 3 arguments + 1 for node + 1 for script name
        error('Invalid number of arguments. Expected 3 or 4, got ' + (process.argv.length - 2));
        throw new Error('Invalid number of arguments');
    }

    let debugMode = false;
    // remove debug flag from arguments 
    if (process.argv.includes('--debug')) {
        debugMode = true;
        process.argv = process.argv.filter(arg => arg !== '--debug');
    }
    if (process.argv.includes('-d')) {
        debugMode = true;
        process.argv = process.argv.filter(arg => arg !== '-d');
    }


    let a = parseFloat(process.argv[2]);
    let operator = process.argv[3];
    let b = parseFloat(process.argv[4]);

    return { a, operator, b, debugMode };
}


function main() {
    let a, operator, b, debugMode, result;
    try{
        ({ a, operator, b, debugMode } = parseArguments());
        
        if (debugMode) {
            Logger.setLevel("stdout", LEVELS.DEBUG);
            debug('Debug mode enabled');
        }

        switch(operator) {
            case '+':
                result = addNumbers(a, b);
                break;
            case '-':
                result = subtractNumbers(a, b);
                break;
            case '*':
                result = multiplyNumbers(a, b);
                break;
            case '/':
                result = divideNumbers(a, b);
                break;
            default:
                error('Invalid operator "' + operator + '"');
                throw new Error('Invalid operator');
        }
    }
    catch(e) {
        critical(e.message);
        process.exit(1);
    }
    info(a.toString() + operator + b.toString() + ' = ' + result.toString());
}

main();