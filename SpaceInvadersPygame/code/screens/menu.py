import sys
from abc import ABC

import pygame
from design.change_design import ChangeDesign
from design.graphics import CRT
from entities.alien import extra_alien_spawn
from game import Game, GameSetup
from game_attributes import GameAttributes

pygame.init()


class MenuGroup:
    def __init__(self):
        self.main = MainMenu()
        self.pause = PauseMenu()
        self.settings = Settings()
        self.sound = SoundSettings()
        self.game_over = GameOver()
        self.victory = VictoryScreen()
        self.config = GameAttributes().config

    def check_menus(self, game: Game, setup: GameSetup):
        if setup.highscore_open:
            self.main._display_highscores(setup)
        elif setup.settings_open:
            self.settings.display_screen(game, setup)
        elif setup.sound_settings_open:
            self.sound.display_screen(game, setup)
        elif setup.game_over:
            setup.game_paused = True
            if game.endscore < self.min_highscore:
                self.game_over.display_screen(game, setup)
            else:
                self.victory.display_screen(game, setup)
        elif setup.game_paused:
            self.pause.display_screen(game, setup)
        elif not setup.game_running:
            self.main.display_screen(game, setup)
        elif not self.game_playing(game, setup):
            setup.game_over = True
            self.min_highscore = GameAttributes().highscores.get_top_ten()[9][0]

    def game_playing(self, game: Game, setup: GameSetup):
        crt = CRT(setup)
        # background = self.config.get_option_dev("colour", "background")

        while not setup.game_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == setup.ALIEN_LASER:
                    setup.alien_shoots.alien_shoot_lasers()
                if event.type == setup.EXTRA_ALIEN_SPAWN:
                    extra_alien_spawn(Game())
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        setup.game_paused = True
                    if event.key == pygame.K_ESCAPE:
                        Game.exit_game()

            if not setup.game_paused:
                setup.clock.tick(game.tick)
                game.levels.group[game.levels.nr].countdown -= game.tick / 1000.0
                game.player_sprite.verify_immunity()

            # setup.screen.fill(background)
            crt.draw()

            if game.run() == False:
                return False

            crt.fps_display(setup.clock)
            crt.mouse_pos_display()
            crt.countdown_display(int(game.levels.group[game.levels.nr].countdown))

            pygame.display.flip()
            return True


class Menus(ABC):
    def __init__(self):
        self.design = GameAttributes().design
        self.config = GameAttributes().config

    def display_screen(self, game, setup):
        pass

    def get_input(self, game, setup):
        pass

    def _display_text(self, text, y, setup):
        text_surface = self.design.get_font().render(
            text, True, self.config.get_option_dev("colour", "white")
        )
        text_rect = text_surface.get_rect(center=(self.config.screen.width // 2, y))
        setup.screen.blit(text_surface, text_rect)

    def _display_highscores(self, setup):
        setup.screen.fill(self.config.get_option_dev("colour", "black"))
        y_position = self.config.screen.height // 2 - 50
        self._display_text("High Scores: ", 400, setup)
        for rank, (score, name) in enumerate(
            GameAttributes().highscores.get_top_ten(), start=1
        ):
            rank_entry = f"{rank}. {name} - {score}"
            self._display_text(rank_entry, y_position, setup)
            y_position += 35
            self._display_text("Close with h", 800, setup)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    setup.highscore_open = False
        pygame.display.flip()

    def _enter_name(self):
        entering_name = True
        player_name = ""

        while entering_name:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        entering_name = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.unicode.isalnum() or event.unicode.isspace():
                        player_name += event.unicode
        return player_name


class MainMenu(Menus):
    def display_screen(self, game: Game, setup: GameSetup):
        setup.screen.fill(self.config.get_option_dev("colour", "black"))
        self._display_text(
            "A Space Invaders Game", self.config.screen.height // 2 - 50, setup
        )
        self._display_text(
            "Press Enter to Start", self.config.screen.height // 2 + 50, setup
        )
        self._display_text(
            "Press h for Highscores", self.config.screen.height // 2 + 200, setup
        )
        self._display_text(
            "Press s for Settings", self.config.screen.height // 2 + 250, setup
        )
        pygame.display.flip()
        self.get_input(game, setup)

    def get_input(self, game: Game, setup: GameSetup):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Start game Initial time
                if event.key == pygame.K_RETURN:
                    setup.game_running = True
                    setup.game_paused = False
                # Show highscore
                elif event.key == pygame.K_h:
                    setup.highscore_open = True
                # Show settings
                elif event.key == pygame.K_s:
                    setup.settings_open = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


class PauseMenu(Menus):
    def display_screen(self, game: Game, setup: GameSetup):
        setup.screen.fill(self.config.get_option_dev("colour", "black"))
        self._display_text("Pause", self.config.screen.height // 6, setup)
        self._display_text(
            "Press Enter to Resume", self.config.screen.height * 2 // 6, setup
        )
        self._display_text(
            "Press s for Settings", self.config.screen.height * 3 // 6, setup
        )
        self._display_text(
            "Press a for Audio Settings", self.config.screen.height * 4 // 6, setup
        )
        self._display_text("Press Q to Quit", self.config.screen.height * 5 // 6, setup)
        pygame.display.flip()
        self.get_input(game, setup)

    def get_input(self, game: Game, setup: GameSetup):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Continue game
                if event.key == pygame.K_RETURN:
                    setup.game_paused = False
                # Open settings
                elif event.key == pygame.K_s:
                    setup.settings_open = True
                # Open Audio settings
                elif event.key == pygame.K_a:
                    setup.sound_settings_open = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


class Settings(Menus):
    def display_screen(self, game: Game, setup: GameSetup):
        setup.screen.fill(GameAttributes().config.get_option_dev("colour", "black"))
        self._display_text("Settings: close with s", 200, setup)
        self._display_text(
            f"Design: {GameAttributes().design.design_name} (switch with d)",
            400,
            setup,
        )
        self._display_text(
            f"Dificulty: {GameAttributes().difficulty} (select with 1-5)",
            500,
            setup,
        )
        level_order = "in order"
        if game.levels.random == True:
            level_order = "random"

        self._display_text(
            f"Level order: {level_order} (switch with o)",
            600,
            setup,
        )
        self._display_text(
            f"Powerups random: {game.levels.items_random} (switch with p)",
            700,
            setup,
        )
        self._display_text("Sound Settings: open with a", 850, setup)
        pygame.display.flip()
        self.get_input(game, setup)

    def set_difficulty(self, difficulty):
        GameAttributes().difficulty = difficulty

    def get_input(self, game: Game, setup: GameSetup):
        change_design = ChangeDesign()
        while setup.settings_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # Close settings
                    if event.key == pygame.K_s:
                        setup.settings_open = False
                    # Open Audio settings
                    elif event.key == pygame.K_a:
                        setup.settings_open = False
                        setup.sound_settings_open = True

                    # Open change level order
                    elif event.key == pygame.K_o:
                        game.levels.random = not game.levels.random

                    # Random Powerup positions
                    elif event.key == pygame.K_p:
                        game.levels.items_random = not game.levels.items_random

                    # Change Design
                    elif event.key == pygame.K_d:
                        GameAttributes().design = change_design.create(
                            change_design.next_design(game.game_attributes.design)
                        )
                        game.music.accept(change_design.update)
                        for alien in game.alien_group:
                            alien.accept(change_design.update)
                        game.player_sprite.accept(change_design.update)
                        for block in game.block_group:
                            block.accept(change_design.update)
                        for powerup in game.powerup_group:
                            powerup.accept(change_design.update)

                    # Dificulty
                    elif event.key == pygame.K_1:
                        self.set_difficulty(1)
                    elif event.key == pygame.K_2:
                        self.set_difficulty(2)
                    elif event.key == pygame.K_3:
                        self.set_difficulty(3)
                    elif event.key == pygame.K_4:
                        self.set_difficulty(4)
                    elif event.key == pygame.K_5:
                        self.set_difficulty(5)
                    # Open Audio settings
                    elif event.key == pygame.K_s:
                        setup.settings_open = not setup.settings_open
                        setup.sound_settings_open = not setup.sound_settings_open
                self.display_screen(game, setup)


class SoundSettings(Menus):
    def display_screen(self, game: Game, setup: GameSetup):
        setup.screen.fill(self.config.get_option_dev("colour", "black"))
        self._display_text(
            "Audio Settings: close with a", self.config.screen.height // 6, setup
        )
        self._display_text(
            f"Music: {'On' if self.config.volumes.music_on else 'Off'}",
            self.config.screen.height * 2 // 6,
            setup,
        )
        self._display_text(
            f"Volume: {int(self.config.volumes.music*10)}",
            self.config.screen.height * 3 // 6,
            setup,
        )
        self._display_text(
            f"Sounds: {'On' if self.config.volumes.sound_on else 'Off'}",
            self.config.screen.height * 4 // 6,
            setup,
        )
        self._display_text(
            f"Volume: {int(self.config.volumes.sounds*10)}",
            self.config.screen.height * 5 // 6,
            setup,
        )
        pygame.display.flip()
        self.get_input(game, setup)

    def get_input(self, game: Game, setup: GameSetup):
        attributes = GameAttributes()
        while setup.sound_settings_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # Close Audio settings
                    if event.key == pygame.K_a:
                        setup.sound_settings_open = False
                        setup.game_paused = True

                    # Mute music with m
                    elif event.key == pygame.K_m:
                        game.music.mute_unmute_music(attributes.config)
                    # Mute sounds with n
                    elif event.key == pygame.K_n:
                        game.sound.mute_unmute_sounds(attributes.config)
                    # Alter volumes music
                    elif event.key == pygame.K_DOWN:
                        game.music.volume_down_music(attributes.config)
                    elif event.key == pygame.K_UP:
                        game.music.volume_up_music(attributes.config)
                    # Alter volumes sounds
                    elif event.key == pygame.K_v:
                        game.sound.volume_down_sounds(attributes.config)
                    elif event.key == pygame.K_b:
                        game.sound.volume_up_sounds(attributes.config)
                self.display_screen(game, setup)


class Endscreen(Menus, ABC):
    def display_screen(self, game, setup):
        setup.screen.fill(self.config.get_option_dev("colour", "black"))
        self._display_text(f"Your Score: {game.endscore}", 400, setup)

        self._display_text("Highscores:", 600, setup)
        y = 650
        for rank, (score, name) in enumerate(
            GameAttributes().highscores.get_top_ten()[:3], start=1
        ):
            rank_entry = f"{rank}. {name} - {score}"
            self._display_text(rank_entry, y, setup)
            y += 45
        self._display_text("Full list with h", 850, setup)

        self._display_text("Settings with s ", 900, setup)

        self._display_text("New game with 0 ", 950, setup)

    def reason_gameover(self, game: Game):
        message = ""
        if game.levels.group[game.levels.nr].countdown <= 0:
            message = message + "Time's Up!"
        if game.player_lives <= 0:
            message = message + "You're Dead!"
        return message


class GameOver(Endscreen):
    def display_screen(self, game: Game, setup: GameSetup):
        super().display_screen(game, setup)

        game_over_text = "Game Over!" + self.reason_gameover(game)
        self._display_text(game_over_text, 330, setup)

        self.get_input(game, setup)
        pygame.display.flip()

    def get_input(self, game: Game, setup: GameSetup):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Start new game
                if event.key == pygame.K_0:
                    game.levels.group[
                        game.levels.nr
                    ].countdown = GameAttributes().config.get_option_dev(
                        "game", "countdown"
                    )
                    game.new_game()
                    setup.start_game_variables()
                    self.player_name = "--press e to enter name--"
                # Open settings
                elif event.key == pygame.K_s:
                    setup.settings_open = True
                # Open highscore
                elif event.key == pygame.K_h:
                    setup.highscore_open = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


class VictoryScreen(Endscreen):
    def display_screen(self, game: Game, setup: GameSetup):
        super().display_screen(game, setup)
        attributes = GameAttributes()

        self._display_text("New Highscore entry!", 200, setup)

        victory_text = "Game over!!" + self.reason_gameover(game)
        self._display_text(victory_text, 330, setup)

        self.player_name = "--press e to enter name--"
        if game.player_name != None:
            self.player_name = game.player_name

        self._display_text(f"1. {self.player_name} : {game.endscore}", 450, setup)

        if (
            self.player_name != "--press e to enter name--"
            and not attributes.highscores.game_saved
        ):
            self._display_text("Press g to save", 500, setup)

        pygame.display.flip()
        self.get_input(game, setup)

    def get_input(self, game: Game, setup: GameSetup):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Start new game
                if event.key == pygame.K_0:
                    game.new_game()
                    setup.start_game_variables()
                    self.player_name = "--press e to enter name--"
                    game.levels.group[
                        game.levels.nr
                    ].countdown = GameAttributes().config.get_option_dev(
                        "game", "countdown"
                    )
                # Enter name:
                if event.key == pygame.K_e:
                    if not GameAttributes().highscores.game_saved:
                        game.player_name = super()._enter_name()
                    pygame.display.flip()
                # Open settings
                elif event.key == pygame.K_s:
                    setup.settings_open = True
                # Open highscore
                elif event.key == pygame.K_h:
                    setup.highscore_open = True
                # Save name
                elif event.key == pygame.K_g:
                    attributes = GameAttributes()
                    if (
                        game.player_name != None
                        and attributes.highscores.game_saved == False
                    ):
                        attributes.highscores._save_json(
                            game.endscore, game.player_name
                        )
                        attributes.highscores.game_saved = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
