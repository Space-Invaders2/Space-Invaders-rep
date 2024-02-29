import sys
from abc import ABC, abstractmethod

import pygame
from config import ConfigDev
from design.change_design import ChangeDesign
from design.graphics import CRT, AbstractDesignFactory, ClassicDesignFactory
from entities.alien import *
from game import Game, GameSetup

pygame.init()


class Menu:
    def __init__(self, design: AbstractDesignFactory = ClassicDesignFactory()):
        self.design = design
        self.config = ConfigDev()

    def _main(self, setup: GameSetup):
        setup.screen.fill(self.config.get_option_dev("colour", "black"))
        self._display_text(
            "A Space Invaders Game", self.config.screen.height // 2 - 50, setup
        )
        self._display_text(
            "Press Enter to Start", self.config.screen.height // 2 + 50, setup
        )
        pygame.display.flip()

    def _pause(self, game: Game, setup: GameSetup):
        setup.screen.fill(self.config.get_option_dev("colour", "black"))
        self._display_text("Pause", self.config.screen.height // 6, setup)
        self._display_text(
            "Press Enter to Resume", self.config.screen.height * 2 // 6, setup
        )
        self._display_text(
            "Press s for Settings", self.config.screen.height * 3 // 6, setup
        )
        self._display_text(
            "Press a for Sound Settings", self.config.screen.height * 4 // 6, setup
        )
        self._display_text("Press Q to Quit", self.config.screen.height * 5 // 6, setup)
        pygame.display.flip()
        self._pause_input(game, setup)

    def _pause_input(self, game: Game, setup: GameSetup):
        while setup.game_paused:
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
                        setup.game_paused = not setup.game_paused
                    # Open sound settings
                    elif event.key == pygame.K_a:
                        setup.sound_settings_open = True
                        setup.game_paused = not setup.game_paused
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def _settings(self, game: Game, setup: GameSetup):
        setup.screen.fill(self.config.get_option_dev("colour", "black"))
        self._display_text(
            "Settings: close with s", self.config.screen.height // 6, setup
        )
        self._display_text(
            f"Design: {GameAttributes().design.design_name} (switch with d)",
            self.config.screen.height * 2 // 6,
            setup,
        )
        self._display_text(
            f"Dificulty: {game.difficulty} (select with 1-5)",
            self.config.screen.height * 3 // 6,
            setup,
        )
        self._display_text(
            "Sound Settings: open with a", self.config.screen.height * 5 // 6, setup
        )
        pygame.display.flip()
        self._settings_input(game, setup)

    def _settings_input(self, game: Game, setup: GameSetup):
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
                        setup.game_paused = True
                    # Open sound settings
                    elif event.key == pygame.K_a:
                        setup.settings_open = False
                        setup.sound_settings_open = True

                    # Change Design
                    elif event.key == pygame.K_d:
                        GameAttributes().design = change_design.create(
                            change_design.next_design(game.game_attributes.design)
                        )
                        # game.music.accept(change_design)
                        for alien in game.alien_group:
                            alien.accept(change_design.update)
                        game.player_sprite.accept(change_design.update)
                    # Dificulty
                    elif event.key == pygame.K_1:
                        game.difficulty = 1
                    elif event.key == pygame.K_2:
                        game.difficulty = 2
                    elif event.key == pygame.K_3:
                        game.difficulty = 3
                    elif event.key == pygame.K_4:
                        game.difficulty = 4
                    elif event.key == pygame.K_5:
                        game.difficulty = 5
                    # Open sound settings
                    elif event.key == pygame.K_s:
                        setup.settings_open = not setup.settings_open
                        setup.sound_settings_open = not setup.sound_settings_open
                self.check_menus(game, setup)

    def _sound_settings(self, game: Game, setup: GameSetup):
        setup.screen.fill(self.config.get_option_dev("colour", "black"))
        self._display_text(
            "Sound Settings: close with a", self.config.screen.height // 6, setup
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
            f"Volume: {int(self.config.volumes.explosion*10)}",
            self.config.screen.height * 5 // 6,
            setup,
        )
        pygame.display.flip()
        self._sound_settings_input(game, setup)

    def _sound_settings_input(self, game: Game, setup: GameSetup):
        attributes = GameAttributes()
        while setup.sound_settings_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # Close sound settings
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
                self.check_menus(game, setup)

    def run_game(self, game: Game, setup: GameSetup):
        crt = CRT(setup)

        background = self.config.get_option_dev("colour", "background")
        game_tick = self.config.get_option_dev("game", "time_tick")

        while not setup.game_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == setup.ALIEN_LASER:
                    setup.alien_shoots.alien_shoot_lasers(Game())
                if event.type == setup.EXTRA_ALIEN_SPAWN:
                    extra_alien_spawn(Game())
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        setup.game_paused = True
                    if event.key == pygame.K_BACKSPACE:
                        Game.exit_game()

            setup.screen.fill(background)
            game.run()
            crt.draw()
            crt.fps_display(setup.clock)
            crt.mouse_pos_display()

            pygame.display.flip()
            setup.clock.tick(game_tick)

    def _display_text(self, text, y, setup):
        text_surface = self.design.get_font().render(
            text, True, self.config.get_option_dev("colour", "white")
        )
        text_rect = text_surface.get_rect(center=(self.config.screen.width // 2, y))
        setup.screen.blit(text_surface, text_rect)

    def check_menus(self, game: Game, setup: GameSetup):
        if not setup.game_running:
            self._main(setup)
        elif setup.settings_open:
            self._settings(game, setup)
        elif setup.sound_settings_open:
            self._sound_settings(game, setup)
        elif (
            setup.game_paused
            and not setup.settings_open
            and not setup.sound_settings_open
        ):
            self._pause(game, setup)
        else:
            self.run_game(game, setup)
