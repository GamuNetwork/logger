import { centerString, getTime, replaceNewLine, getCallerInfo, splitLongString } from '#dist/utils.js';
import process from 'node:process';

const OS = process.platform;

describe('replaceNewLine', () => {
    it('should add indentation to new line', () => {
        const str = "Hello\nWorld!";
        expect(replaceNewLine(str)).toBe("Hello\n                                 | World!");
    });
    it('should set indentation to given value', () => {
        const str = "Hello\nWorld!";
        expect(replaceNewLine(str, 2)).toBe("Hello\n  | World!");
    });
});

describe('centerString', () => {
    it('should center string', () => {
        const str = "Hello";
        expect(centerString(str, 10)).toBe("  Hello   ");
    });
});

describe('getTime', () => {
    it('should return time', () => {
        const time = getTime();
        expect(time).toBeInstanceOf(String);
        expect(time).toMatch(/\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}/);
    });
});

describe('getCallerInfo', () => {
    it('should return caller informations', () => {
        const [func, file] = getCallerInfo();
        expect(file).toMatch(/.+jasmine\.js/);
        expect(func).toBe('attempt');
    });
    it('should return an absolute path', () => {
        const file = getCallerInfo()[1];
        if(OS === 'win32'){
            expect(file).toMatch(/^[A-Z]:\\.*jasmine\.js/);
        }
        else{
            expect(file).toMatch(/^.+jasmine\.js/);
        }
    });
});

describe('splitLongString', () => {
    it('should split long string', () => {
        const str = "Hello World!";
        expect(splitLongString(str, 5)).toBe("Hello\nWorld!");
    });
    it('should not split short string', () => {
        const str = "Hello";
        expect(splitLongString(str, 5)).toBe("Hello");
    });
    it('should split on space', () => {
        const str = "Hello World!";
        expect(splitLongString(str, 6)).toBe("Hello\nWorld!");
    });
});