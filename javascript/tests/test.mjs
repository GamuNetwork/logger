import { Logger, info, error } from '#dist/index.js';
import { Target, LEVELS, SENSITIVE_LEVELS, TARGET_TYPE } from '#dist/customTypes.js';
import fs from 'fs';
import tmp from 'tmp';

const randomName = tmp.tmpNameSync();
    let target = Target.fromFile(randomName);
    target.name = "newLog.txt";

    // it('target name should be newLog.txt', () => {
    //     expect(target.name).toBe("newLog.txt");
    // });