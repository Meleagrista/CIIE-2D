import pygame

from utils.filepaths import DETECTED_SOUND, DEATH_SOUND, INCREASE_HEALTH_SOUND, MOVEMENT_SOUND, PICK_UP_KEY_SOUND, \
    FINISH_LEVEL_SOUND, MUSIC_BACKGROUND, MUSIC_MEDIEVAL, MUSIC_FALL_FROM_GRACE


class AudioManager:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 4096)  # Adjust pre-init parameters
        pygame.mixer.init()
        pygame.mixer.set_reserved(3)

        self.sound_detected = pygame.mixer.Sound(DETECTED_SOUND)
        self.sound_death = pygame.mixer.Sound(DEATH_SOUND)
        self.sound_increase_health = pygame.mixer.Sound(INCREASE_HEALTH_SOUND)
        self.sound_movement = pygame.mixer.Sound(MOVEMENT_SOUND)
        self.sound_pick_up_key = pygame.mixer.Sound(PICK_UP_KEY_SOUND)
        self.sound_finish_level = pygame.mixer.Sound(FINISH_LEVEL_SOUND)

        # Initialize channels
        self.channel_increase_health = pygame.mixer.Channel(0)
        self.channel_detected = pygame.mixer.Channel(1)
        self.channel_movement = pygame.mixer.Channel(2)

        # Set initial volumes
        self.channel_increase_health.set_volume(1)
        self.channel_detected.set_volume(1)
        self.channel_movement.set_volume(1)

        # Play sounds and pause them initially
        self.channel_increase_health.play(self.sound_increase_health, loops=-1)
        self.channel_increase_health.pause()

        self.channel_detected.play(self.sound_detected, loops=-1)
        self.channel_detected.pause()

        self.channel_movement.play(self.sound_movement, loops=-1)
        self.channel_movement.pause()

        self.all_channels = [self.channel_increase_health, self.channel_detected, self.channel_movement]

        pygame.mixer.music.load(MUSIC_FALL_FROM_GRACE)
        pygame.mixer.music.play(-1)

    def pause(self):
        for channel in self.all_channels:
            channel.pause()

    def music_game(self):
        pygame.mixer.music.stop()
        self.pause()
        pygame.mixer.music.load(MUSIC_BACKGROUND)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

    def music_menu(self):
        pygame.mixer.music.stop()
        self.pause()
        pygame.mixer.music.load(MUSIC_MEDIEVAL)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1)

    def play_finish(self):
        self.pause()
        self.sound_finish_level.play()
        pygame.time.wait(3500)

    def play_key(self):
        self.sound_pick_up_key.play()

    def play_movement(self):
        self.channel_movement.unpause()

    def stop_movement(self):
        self.channel_movement.pause()

    def play_death(self):
        self.channel_detected.pause()
        self.sound_death.play()

    def play_detected(self):
        self.channel_detected.unpause()

    def stop_detected(self):
        self.channel_detected.pause()

    def play_recovering(self):
        self.channel_increase_health.unpause()

    def stop_recovering(self):
        self.channel_increase_health.pause()
