class CompType:
    EQU = 0
    STR = 1
    STR_MID = 2
    STR_END = 3
    MID = 4
    MID_MID = 5
    MID_END = 6
    END = 7
    ANY = 8


class StrMatch:
    def __init__(self, pattern):
        self.pattern = pattern
        self.comp = None
        self.start = self.end = self.mid = self.mid2 = ''

        if pattern in ('*', '**'):
            self.comp = CompType.ANY
        else:
            length = len(pattern)
            if length < 2:
                self.comp = CompType.EQU
                self.mid = pattern
            else:
                any_start = pattern[0] == '*'
                any_end = pattern[-1] == '*'
                apos = pattern[1:].find('*') + 1
                any_mid = 0 < apos < length - 1

                if any_mid:
                    if any_start and any_end:
                        self.comp = CompType.MID_MID
                        self.mid = pattern[1:apos]
                        self.mid2 = pattern[apos + 1:-1]
                    elif any_start:
                        self.comp = CompType.MID_END
                        self.mid = pattern[1:apos]
                        self.end = pattern[apos + 1:]
                    elif any_end:
                        self.comp = CompType.STR_MID
                        self.start = pattern[:apos]
                        self.mid = pattern[apos + 1:-1]
                    else:
                        self.comp = CompType.STR_END
                        self.start = pattern[:apos]
                        self.end = pattern[apos + 1:]
                else:
                    if any_start and any_end:
                        self.comp = CompType.MID
                        self.mid = pattern[1:-1]
                    elif any_start:
                        self.comp = CompType.END
                        self.end = pattern[1:]
                    elif any_end:
                        self.comp = CompType.STR
                        self.start = pattern[:-1]
                    else:
                        self.comp = CompType.EQU
                        self.mid = pattern

    def include(self, target):
        if not target:
            return False
        if self.comp == CompType.ANY:
            return True
        elif self.comp == CompType.EQU:
            return self.mid == target
        elif self.comp == CompType.STR:
            return target.startswith(self.start)
        elif self.comp == CompType.STR_MID:
            return target.startswith(self.start) and self.mid in target
        elif self.comp == CompType.STR_END:
            return target.startswith(self.start) and target.endswith(self.end)
        elif self.comp == CompType.MID:
            return self.mid in target
        elif self.comp == CompType.MID_MID:
            x = target.find(self.mid)
            return x >= 0 and self.mid2 in target[target.find(self.mid2):] and target.endswith(self.end)
        elif self.comp == CompType.MID_END:
            return self.mid in target and target.endswith(self.end)
        elif self.comp == CompType.END:
            return target.endswith(self.end)
        return False


class CommaSeparatedChainedStrMatcher:
    def __init__(self, patterns):
        self.str_matches = [StrMatch(pattern) for pattern in patterns.split(',')]

    def is_match(self, target):
        return any(match.include(target) for match in self.str_matches)


if __name__ == '__main__':
    matcher = CommaSeparatedChainedStrMatcher("ab*,*cd,efg")
    print(matcher.is_match("abcdef"))  # True
    print(matcher.is_match("efg"))  # True
