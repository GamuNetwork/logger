// import { info, warning, error, debug, Logger } from '@gamunetwork/logger';
import { info, critical, error, debug, Logger, LEVELS } from '../../dist/index.js';

Logger.setModule('action'); //set the module name for this file

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

export { addNumbers, subtractNumbers, multiplyNumbers, divideNumbers };