import customTypes, { LEVELS } from '#dist/customTypes.js';
const { Target, TARGET_TYPE, TERMINAL_TARGETS, LoggerConfig } = customTypes;
import tmp from 'tmp';
import fs from 'fs';

// ------------------- Target -------------------

describe('testing Target.constructor', () => {
    const func = () => { return; };
    let target = new Target(func);
    it('target should be defined', () => {
        expect(target).toBeDefined();
    });
    it('target name should be func', () => {
        expect(target.name).toBe("func");
    });
    it('target type should be a file', () => {
        expect(target.type).toBe(TARGET_TYPE.FILE);
    });
    it("target representation should conatain right values", () => {
        expect(target.repr()).toEqual({name: "func", type: TARGET_TYPE.FILE, properties: {}});
    });
});

describe('testing Target.fromFile', () => {
    const filename = tmp.tmpNameSync();
    let target = Target.fromFile(filename);
    it('target should be defined', () => {
        expect(target).toBeDefined();
    });
    it('target name should be filename', () => {
        expect(target.name).toBe(filename);
    });
    it('target type should be a file', () => {
        expect(target.type).toBe(TARGET_TYPE.FILE);
    });
    it("target representation should conatain right values", () => {
        expect(target.repr()).toEqual({name: filename, type: TARGET_TYPE.FILE, properties: {}});
    });
    fs.unlinkSync(filename);
});

describe('testing Target.constructor with stderr', () => {
    let target = new Target(TERMINAL_TARGETS.STDERR, 'stderr');
    it('target should be defined', () => {
        expect(target).toBeDefined();
    });
    it('target name should be func', () => {
        expect(target.name).toBe("stderr");
    });
    it('target type should be a terminal', () => {
        expect(target.type).toBe(TARGET_TYPE.TERMINAL);
    });
    it("target properties should be empty", () => {
        expect(target.repr()["properties"]).toEqual({});
    });
});

describe('testing Target.fromJson', () => {
    const randomName = tmp.tmpNameSync();

    const target = Target.fromJson({
        "file": randomName,
        "level": "info",
        "sensitiveMode": "hide"
    });

    it('target should be defined', () => {
        expect(target).toBeDefined();
    });
    it('target name should be the name of the file', () => {
        expect(target.name).toBe(randomName);
    });
    it('target type should be a file', () => {
        expect(target.type).toBe(TARGET_TYPE.FILE);
    });
    it('target level should be info', () => {
        expect(target.getProperty("level")).toBe(LEVELS.INFO);
    });
    it('target sensitiveMode should be hide', () => {
        expect(target.getProperty("sensitiveMode")).toBe("hide");
    });
});

describe('testing Target.fromXml', () => {
    const randomName = tmp.tmpNameSync();

    const target = Target.fromXml({"target" :
        {
            "µ_file": randomName,
            "µ_level": "info",
            "µ_sensitiveMode": "hide"
        }
    });

    it('target should be defined', () => {
        expect(target).toBeDefined();
    });
    it('target name should be the name of the file', () => {
        expect(target.name).toBe(randomName);
    });
    it('target type should be a file', () => {
        expect(target.type).toBe(TARGET_TYPE.FILE);
    });
    it('target level should be info', () => {
        expect(target.getProperty("level")).toBe(LEVELS.INFO);
    });
    it('target sensitiveMode should be hide', () => {
        expect(target.getProperty("sensitiveMode")).toBe("hide");
    });
});

describe('testing Target.setName', () => {
    
    const randomName = tmp.tmpNameSync();
    let target = Target.fromFile(randomName);
    target.name = "newLog.txt";

    it('target name should be newLog.txt', () => {
        expect(target.name).toBe("newLog.txt");
    });
});