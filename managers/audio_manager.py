import pygame

from utils.paths.assets_paths import DETECTED_SOUND, DEATH_SOUND, INCREASE_HEALTH_SOUND, MOVEMENT_SOUND, \
    PICK_UP_KEY_SOUND, \
    FINISH_LEVEL_SOUND, MUSIC_BACKGROUND, MUSIC_MEDIEVAL


class AudioManager:
    def __init__(self):
        # Initialize the audio mixer with pre-defined parameters
        pygame.mixer.pre_init(44100, -16, 2, 4096)  # Adjust pre-init parameters
        pygame.mixer.init()
        pygame.mixer.set_reserved(3)  # Reserve 3 channels for the mixer

        # Load sound assets
        self.sound_detected = pygame.mixer.Sound(DETECTED_SOUND)
        self.sound_death = pygame.mixer.Sound(DEATH_SOUND)
        self.sound_increase_health = pygame.mixer.Sound(INCREASE_HEALTH_SOUND)
        self.sound_movement = pygame.mixer.Sound(MOVEMENT_SOUND)
        self.sound_pick_up_key = pygame.mixer.Sound(PICK_UP_KEY_SOUND)
        self.sound_finish_level = pygame.mixer.Sound(FINISH_LEVEL_SOUND)

        # Initialize channels for sound playback
        self.channel_increase_health = pygame.mixer.Channel(0)
        self.channel_detected = pygame.mixer.Channel(1)
        self.channel_movement = pygame.mixer.Channel(2)

        # Set initial volumes for channels
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

        # Store all channels in a list for easy access
        self.all_channels = [self.channel_increase_health, self.channel_detected, self.channel_movement]

    def pause(self):
        """
        Pause all sound channels.
        """
        for channel in self.all_channels:
            channel.pause()

    def music_game(self):
        """
        Play game background music.
        """
        pygame.mixer.music.stop()
        self.pause()
        pygame.mixer.music.load(MUSIC_BACKGROUND)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

    def music_menu(self):
        """
        Play menu background music.
        """
        pygame.mixer.music.stop()
        self.pause()
        pygame.mixer.music.load(MUSIC_MEDIEVAL)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1)

    def play_finish(self):
        """
        Play the level finish sound.
        """
        self.pause()
        self.sound_finish_level.play()

    def play_key(self):
        """
        Play the key pickup sound.
        """
        self.sound_pick_up_key.play()

    def play_movement(self):
        """
        Resume movement sound.
        """
        self.channel_movement.unpause()

    def stop_movement(self):
        """
        Pause movement sound.
        """
        self.channel_movement.pause()

    def play_death(self):
        """
        Play death sound.
        """
        self.channel_detected.pause()
        self.sound_death.play()

    def play_detected(self):
        """
        Resume detection sound.
        """
        self.channel_detected.unpause()

    def stop_detected(self):
        """
        Pause detection sound.
        """
        self.channel_detected.pause()

    def play_recovering(self):
        """
        Resume health recovery sound.
        """
        self.channel_increase_health.unpause()

    def stop_recovering(self):
        """
        Pause health recovery sound.
        """
        self.channel_increase_health.pause()
