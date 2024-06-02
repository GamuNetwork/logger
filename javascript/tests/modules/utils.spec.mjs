import { centerString, getTime, replaceNewLine, GetCallerFileName } from '#dist/utils.js';

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

describe('GetCallerFileName', () => {
    it('should return caller info', () => {
        const caller = GetCallerFileName();
        expect(caller).toMatch(/.+jasmine\.js/);
    });
});