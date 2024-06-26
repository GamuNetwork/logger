// create a basic web server using express

// import { info, warning, error, debug, Logger } from '@gamunetwork/logger';
import { info, critical, error, debug, Logger, LEVELS, warning } from '../../dist/index.js';

import { addNumbers, subtractNumbers, multiplyNumbers, divideNumbers } from './action.mjs';

Logger.setLevel('stdout', LEVELS.DEBUG); //set the log level for stdout
Logger.setModule('server'); //set the module name for this file

import express from 'express';

const app = express();
const port = 3000;

app.get('/', (req, res) => {
    info('Request received from ' + req.ip + ' for /');
    res.send('Hello World!');
});

app.get("/private", (req, res) => {
    warning('Request received from ' + req.ip + ' for /private, access denied');
    res.status(403).send('Access denied');
});

app.get("/stop", (req, res) => {
    info('Request received from ' + req.ip + ' for /stop, stopping server');
    res.send('Stopping server');
    process.exit(0);
});

app.get("/crash", (req, res) => {
    critical('Request received from ' + req.ip + ' for /crash, crashing server');
    res.send('Crashing server');
    process.exit(1);
});

app.get("/add", (req, res) => { // /add?a=1&b=2
    if(!req.query.a || !req.query.b) {
        warning('Invalid arguments for /add, expected numbers, got a=' + req.query.a + ' and b=' + req.query.b);
        res.status(400).send('Invalid arguments, expected numbers');
        return;
    }
    let a = parseFloat(req.query.a);
    let b = parseFloat(req.query.b);
    info('Request received from ' + req.ip + ' for /add with arguments a=' + a + ' and b=' + b);
    let result = addNumbers(a, b);
    res.send('Result: ' + result);
});

app.get("/subtract", (req, res) => { // /subtract?a=1&b=2
    if(!req.query.a || !req.query.b) {
        warning('Invalid arguments for /subtract, expected numbers, got a=' + req.query.a + ' and b=' + req.query.b);
        res.status(400).send('Invalid arguments, expected numbers');
        return;
    }
    let a = parseFloat(req.query.a);
    let b = parseFloat(req.query.b);
    info('Request received from ' + req.ip + ' for /subtract with arguments a=' + a + ' and b=' + b);
    let result = subtractNumbers(a, b);
    res.send('Result: ' + result);
});

app.get("/multiply", (req, res) => { // /multiply?a=1&b=2
    if(!req.query.a || !req.query.b) {
        warning('Invalid arguments for /multiply, expected numbers, got a=' + req.query.a + ' and b=' + req.query.b);
        res.status(400).send('Invalid arguments, expected numbers');
        return;
    }
    let a = parseFloat(req.query.a);
    let b = parseFloat(req.query.b);
    info('Request received from ' + req.ip + ' for /multiply with arguments a=' + a + ' and b=' + b);
    let result = multiplyNumbers(a, b);
    res.send('Result: ' + result);
});

app.get("/divide", (req, res) => { // /divide?a=1&b=2
    if(!req.query.a || !req.query.b) {
        warning('Invalid arguments for /divide, expected numbers, got a=' + req.query.a + ' and b=' + req.query.b);
        res.status(400).send('Invalid arguments, expected numbers');
        return;
    }
    let a = parseFloat(req.query.a);
    let b = parseFloat(req.query.b);
    info('Request received from ' + req.ip + ' for /divide with arguments a=' + a + ' and b=' + b);
    try {
        let result = divideNumbers(a, b);
        res.send('Result: ' + result);
    } catch (e) {
        res.status(400).send(e.message);
    }
});



app.listen(port, () => {
    info(`Example app listening at http://localhost:${port}`);
});