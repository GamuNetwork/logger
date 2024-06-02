import { Logger } from '#dist/index.js';
import { Target, LEVELS, SENSITIVE_LEVELS, TargetType } from '#dist/customTypes.js';
import { describe } from 'node:test';

import fs from 'fs';
//redirect stdout to file
function redirectStream(stream, filename) {
    let file = fs.createWriteStream(filename);
    stream.write = file.write.bind(file);
}

describe('testing default configuration', () => {
    it('terminal should exist', () => {
        expect(Target.exist("terminal")).toBe(true);
    });

    let terminalTarget = Target.get("terminal");
    it('sensitiveMode should be HIDE', () => {
        expect(terminalTarget.getProperty("sensitiveMode")).toBe(SENSITIVE_LEVELS.HIDE);
    });
    it('level should be INFO', () => {
        expect(terminalTarget.getProperty("level")).toBe(LEVELS.INFO);
    });
    it('type should be terminal', () => {
        expect(terminalTarget.type).toBe(TargetType.TERMINAL);
    });
    it('sensitive data list should be empty', () => {
        expect(Logger.repr()["SensitiveDatas"]).toEqual([]);
    });
    it('module map should be empty', () => {
        expect(Logger.repr()["moduleMap"]).toEqual({});
    });
});

describe('testing logging functions', () => {
    // redirectStream(process.stdout, "tests/logs/stdout.log");
    
    it('should log INFO message', () => {
        process.stdout.write = jasmine.createSpy("stdout").and.callFake(function (data) {
            // console.log(data);
            return true;
        });
        Logger.info("info message");
        expect(process.stdout.write).toHaveBeenCalledWith("info message\n");
    });
});