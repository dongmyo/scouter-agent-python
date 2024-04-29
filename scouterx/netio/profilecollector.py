from scouterx.conf.configure import Configure
from scouterx.netio.dataproxy import send_profile

aconf = Configure()


class ProfileCollector:
    def __init__(self, tctx):
        self.tctx = tctx
        self.steps = [None] * aconf.profile_step_max_keep_in_memory_count
        self.pos = 0
        self.doingDumpStepJob = False
        self.currentLevel = 0
        self.parentLevel = 0

    def push(self, ss):
        self.check_dump_step()
        ss.set_index(self.currentLevel)
        ss.set_parent(self.parentLevel)
        self.parentLevel = self.currentLevel
        self.currentLevel += 1

    def pop(self, ss):
        self.check_dump_step()
        self.parentLevel = ss.get_parent()
        self.process(ss)

    def add(self, ss):
        self.check_dump_step()
        ss.set_index(self.currentLevel)
        ss.set_parent(self.parentLevel)
        self.currentLevel += 1
        self.process(ss)

    def process(self, ss):
        self.check_dump_step()
        self.steps[self.pos] = ss
        self.pos += 1
        if self.pos >= len(self.steps):
            o = self.steps
            self.steps = [None] * aconf.profile_step_max_keep_in_memory_count
            self.pos = 0
            send_profile(o, self.tctx)

    def close(self, ok):
        self.check_dump_step()
        if self.pos > 0 and ok:
            send_profile(self.steps[:self.pos], self.tctx)

    def check_dump_step(self):
        # TODO
        pass
