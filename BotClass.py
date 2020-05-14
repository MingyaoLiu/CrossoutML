
import Constants as const
from Constants import ScreenStep, Point
from ScreenClass import Screen
from Utils import getCorrectPos


class BotProgram():

    def __init__(self):

        self.LoginScreen = Screen(ScreenStep.Login, const.login_crops, 10)
        self.WelcomeScreen = Screen(ScreenStep.WelcomeScreen,
                                    const.welcome_crops, 20)

        self.MasterJackUpgradeScreen = Screen(
            ScreenStep.MasterJackUpgradeScreen, const.mainmenu_master_jack_crops, 10)

        self.ChallengeCompleteScreen = Screen(
            ScreenStep.ChallengeCompleteScreen, const.mainmenu_challenge_crops, 10)

        self.MainMenuScreen = Screen(
            ScreenStep.MainMenu, const.mainmenu_crops, 30)

        self.select_mode_click_pos = [
            getCorrectPos(Point(const.scrap_btn_trigger_pos_x,
                                const.scrap_btn_trigger_pos_y)),
            getCorrectPos(Point(const.wire_btn_trigger_pos_x,
                                const.wire_btn_trigger_pos_y)),
            getCorrectPos(Point(const.battery_btn_trigger_pos_x,
                                const.battery_btn_trigger_pos_y)),
            getCorrectPos(Point(const.raven_path_btn_trigger_pos_x,
                                const.raven_path_btn_trigger_pos_y))
        ]
        self.SelectModeScreen = Screen(ScreenStep.SelectMode, [], 30)

        self.ResourcePrepareBattleScreen = Screen(
            ScreenStep.GetResourceMenu, const.resource_prepare_crops, 30)

        self.BattlePreparationScreen = Screen(
            ScreenStep.BattlePrepareScreen, const.battle_preparation_crops, 1500)

        self.InBattleScreen = Screen(ScreenStep.InBattleNow, [], 30)

        self.FinishBattleScreen = Screen(
            ScreenStep.FinishBattleScreen, const.finish_battle_crops, 3000)

    def stop(self):
        print("STOP BOT")

    def start(self):
        print("START BOT")
