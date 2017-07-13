# coding=utf-8

from pages.challenge_task import Challenge
from windows.pipelines.pipeline import Pipeline


class ChallengeTask(Pipeline):
    def __init__(self, times, app, config):
        super().__init__(["开始挑战", "打怪"], app)
        self.times = times
        self.task = Challenge(config["d"])

    def run_task(self):
        for num in range(self.times):
            self.status = {"开始挑战": "going", "打怪": "ready"}
            if not self.task.start_challenge():
                self.status["等待开始"] = "fail"
                break
            self.status["开始挑战"] = "pass"
            self.status["打怪"] = "going"
            self.task.challenge_fight()
            self.status["打怪"] = "pass"
            self.times_done = self.task.times
            self.task.analysis()
