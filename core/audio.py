class AudioManager:
    def __init__(self, assets, music_file: str, volume: float):
        self.assets = assets
        self.music = self.assets.sound(music_file)
        self.music.set_volume(volume)

    def play_music_loop(self):
        if self.music:
            self.music.play(loops=-1)
