import random
from threading import Lock

from scouterx.common.netdata.xlogpack import XLOG_DISCARD_NONE, XLOG_DISCARD_PROFILE, XLOG_DISCARD_ALL
from scouterx.common.util.strmatch import CommaSeparatedChainedStrMatcher
from scouterx.conf.configure import Configure
from scouterx.conf.opserver import add_to_conf_observer

ac = Configure()
xlog_sampler_instance = None
xlog_sampler_lock = Lock()


class XlogSampler:
    def __init__(self):
        self.current_exclude_sampling_pattern = ac.xlog_sampling_exclude_patterns
        self.current_discard_service_patterns = ac.xlog_discard_service_patterns
        self.current_sampling_service_patterns = ac.xlog_patterned_sampling_service_patterns
        self.current_sampling2_service_patterns = ac.xlog_patterned2_sampling_service_patterns
        self.current_sampling3_service_patterns = ac.xlog_patterned3_sampling_service_patterns

        self.exclude_sampling_pattern_matcher = CommaSeparatedChainedStrMatcher(self.current_exclude_sampling_pattern)
        self.discard_pattern_matcher = CommaSeparatedChainedStrMatcher(self.current_discard_service_patterns)
        self.sampling_pattern_matcher = CommaSeparatedChainedStrMatcher(self.current_sampling_service_patterns)
        self.sampling2_pattern_matcher = CommaSeparatedChainedStrMatcher(self.current_sampling2_service_patterns)
        self.sampling3_pattern_matcher = CommaSeparatedChainedStrMatcher(self.current_sampling3_service_patterns)

        add_to_conf_observer("XlogSampler", self)

    def run(self):
        if self.current_exclude_sampling_pattern != ac.xlog_sampling_exclude_patterns:
            self.current_exclude_sampling_pattern = ac.xlog_sampling_exclude_patterns
            self.exclude_sampling_pattern_matcher = CommaSeparatedChainedStrMatcher(ac.xlog_sampling_exclude_patterns)
        if self.current_discard_service_patterns != ac.xlog_discard_service_patterns:
            self.current_discard_service_patterns = ac.xlog_discard_service_patterns
            self.discard_pattern_matcher = CommaSeparatedChainedStrMatcher(ac.xlog_discard_service_patterns)
        if self.current_sampling_service_patterns != ac.xlog_patterned_sampling_service_patterns:
            self.current_sampling_service_patterns = ac.xlog_patterned_sampling_service_patterns
            self.sampling_pattern_matcher = CommaSeparatedChainedStrMatcher(ac.xlog_patterned_sampling_service_patterns)
        if self.current_sampling2_service_patterns != ac.xlog_patterned2_sampling_service_patterns:
            self.current_sampling2_service_patterns = ac.xlog_patterned2_sampling_service_patterns
            self.sampling2_pattern_matcher = CommaSeparatedChainedStrMatcher(ac.xlog_patterned2_sampling_service_patterns)
        if self.current_sampling3_service_patterns != ac.xlog_patterned3_sampling_service_patterns:
            self.current_sampling3_service_patterns = ac.xlog_patterned3_sampling_service_patterns
            self.sampling3_pattern_matcher = CommaSeparatedChainedStrMatcher(ac.xlog_patterned3_sampling_service_patterns)

    def evaluate_xlog_discard(self, elapsed, service_name):
        discard_mode = XLOG_DISCARD_NONE

        if ac.xlog_sampling_enabled and self.is_exclude_sampling_service_pattern(service_name):
            return XLOG_DISCARD_NONE

        discarded = False
        if ac.xlog_patterned_sampling_enabled:
            discarded = self.is_sampling_service_pattern(service_name)
            if discarded:
                discard_mode = self.sampling_patterned(elapsed, discard_mode, 1)
        if not discarded and ac.xlog_patterned2_sampling_enabled:
            discarded = self.is_sampling2_service_pattern(service_name)
            if discarded:
                discard_mode = self.sampling_patterned(elapsed, discard_mode, 2)
        if not discarded and ac.xlog_patterned3_sampling_enabled:
            discarded = self.is_sampling3_service_pattern(service_name)
            if discarded:
                discard_mode = self.sampling_patterned(elapsed, discard_mode, 3)
        if not discarded and ac.xlog_sampling_enabled:
            discard_mode = self.sampling_elapsed(elapsed, discard_mode)

        return discard_mode

    def sampling_elapsed(self, elapsed, discard_mode):
        steps = [(ac.xlog_sampling_step1_ms, ac.xlog_sampling_step1_rate_pct),
                 (ac.xlog_sampling_step2_ms, ac.xlog_sampling_step2_rate_pct),
                 (ac.xlog_sampling_step3_ms, ac.xlog_sampling_step3_rate_pct),
                 (float('inf'), ac.xlog_sampling_over_rate_pct)]

        for step_ms, rate_pct in steps:
            if elapsed < step_ms:
                if random.randint(0, 99) >= rate_pct:
                    return self.refer_to_profile_mode(ac.xlog_sampling_only_profile)
        return discard_mode

    def sampling_patterned(self, elapsed, discard_mode, pattern_level):
        config = {
            1: (ac.xlog_patterned_sampling_step1_ms, ac.xlog_patterned_sampling_step1_rate_pct),
            2: (ac.xlog_patterned2_sampling_step1_ms, ac.xlog_patterned2_sampling_step1_rate_pct),
            3: (ac.xlog_patterned3_sampling_step1_ms, ac.xlog_patterned3_sampling_step1_rate_pct),
        }
        step_ms, rate_pct = config[pattern_level]

        if elapsed < step_ms:
            if random.randint(0, 99) >= rate_pct:
                return self.refer_to_profile_mode(ac.xlog_patterned_sampling_only_profile)
        return discard_mode

    def refer_to_profile_mode(self, only_profile):
        if only_profile:
            return XLOG_DISCARD_PROFILE
        else:
            return XLOG_DISCARD_ALL

    def is_exclude_sampling_service_pattern(self, service_name):
        return self.exclude_sampling_pattern_matcher.is_match(service_name)

    def is_discard_service_pattern(self, service_name):
        return self.discard_pattern_matcher.is_match(service_name)

    def is_sampling_service_pattern(self, service_name):
        return self.sampling_pattern_matcher.is_match(service_name)

    def is_sampling2_service_pattern(self, service_name):
        return self.sampling2_pattern_matcher.is_match(service_name)

    def is_sampling3_service_pattern(self, service_name):
        return self.sampling3_pattern_matcher.is_match(service_name)


def get_xlog_sampler():
    global xlog_sampler_instance
    if xlog_sampler_instance is None:
        with xlog_sampler_lock:
            if xlog_sampler_instance is None:
                xlog_sampler_instance = XlogSampler()
    return xlog_sampler_instance
