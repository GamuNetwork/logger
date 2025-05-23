import { Logger } from '#dist/index.js';
import { Target, LEVELS, SENSITIVE_LEVELS, TARGET_TYPE } from '#dist/customTypes.js';

import tmp from 'tmp';
import fs from 'fs';

describe('testing default configuration', () => {
    it('no targets should be defined', () => {
        Logger.reset();
        expect(Target.list().length).toBe(0);
    });
    it('sensitive data list should be empty', () => {
        expect(Logger.repr()["SensitiveDatas"]).toEqual([]);
    });
    it('module map should be empty', () => {
        expect(Logger.repr()["moduleMap"]).toEqual([]);
    });
});

describe('testing logging functions', () => { //deepDebug, debug, info, warning, error, critical
    it('should log DEEP_DEBUG message', function testDeepDebug() {
        Logger.reset();
        const randomName = tmp.tmpNameSync();
        Logger.addTarget(randomName);
        Logger.setLevel(randomName, LEVELS.DEEP_DEBUG);
        Logger.deepDebug("Hello World!");
        const log = fs.readFileSync(randomName, 'utf8');
        expect(log).toMatch(/\[[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\] \[  DEBUG   \] Hello World!/);
        fs.unlinkSync(randomName);
    });
    it('should log DEBUG message', function testDebug() {
        Logger.reset();
        const randomName = tmp.tmpNameSync();
        Logger.addTarget(randomName);
        Logger.setLevel(randomName, LEVELS.DEBUG);
        Logger.debug("Hello World!");
        const log = fs.readFileSync(randomName, 'utf8');
        expect(log).toMatch(/\[[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\] \[  DEBUG   \] Hello World!/);
        fs.unlinkSync(randomName);
    });
    it('should log INFO message', function testInfo() {
        Logger.reset();
        const randomName = tmp.tmpNameSync();
        Logger.addTarget(randomName);
        Logger.info("Hello World!");
        const log = fs.readFileSync(randomName, 'utf8');
        expect(log).toMatch(/\[[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\] \[   INFO   \] Hello World!/);   
        fs.unlinkSync(randomName);
    });
    it('should log WARNING message', function testWarning() {
        Logger.reset();
        const randomName = tmp.tmpNameSync();
        Logger.addTarget(randomName);
        Logger.warning("Hello World!");
        const log = fs.readFileSync(randomName, 'utf8');
        expect(log).toMatch(/\[[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\] \[ WARNING  \] Hello World!/); 
        fs.unlinkSync(randomName);  
    });
    it('should log ERROR message', function testError() {
        Logger.reset();
        const randomName = tmp.tmpNameSync();
        Logger.addTarget(randomName);
        Logger.error("Hello World!");
        const log = fs.readFileSync(randomName, 'utf8');
        expect(log).toMatch(/\[[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\] \[  ERROR   \] Hello World!/);  
        fs.unlinkSync(randomName); 
    });
    it('should log CRITICAL message', function testCritical() {
        Logger.reset();
        const randomName = tmp.tmpNameSync();
        Logger.addTarget(randomName);
        Logger.critical("Hello World!");
        const log = fs.readFileSync(randomName, 'utf8');
        expect(log).toMatch(/\[[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\] \[ CRITICAL \] Hello World!/); 
        fs.unlinkSync(randomName);  
    });
});