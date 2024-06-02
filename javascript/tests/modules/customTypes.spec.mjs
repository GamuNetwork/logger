import { Target, TargetType, TerminalTargets } from '#dist/customTypes.js';
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
        expect(target.type).toBe(TargetType.FILE);
    });
    it("target representation should conatain right values", () => {
        expect(target.repr()).toEqual({name: "func", type: TargetType.FILE, properties: {}});
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
        expect(target.type).toBe(TargetType.FILE);
    });
    it("target representation should conatain right values", () => {
        expect(target.repr()).toEqual({name: filename, type: TargetType.FILE, properties: {}});
    });
    fs.unlinkSync(filename);
});

describe('testing Target.constructor with stderr', () => {
    let target = new Target(TerminalTargets.STDERR, 'stderr');
    it('target should be defined', () => {
        expect(target).toBeDefined();
    });
    it('target name should be func', () => {
        expect(target.name).toBe("stderr");
    });
    it('target type should be a terminal', () => {
        expect(target.type).toBe(TargetType.TERMINAL);
    });
    it("target properties should be empty", () => {
        expect(target.repr()["properties"]).toEqual({});
    });
});
