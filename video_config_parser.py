import json
import re

enable_or_disable = {
    0: 'Disabled',
    1: 'Enabled'
}

aspect_ratio = {
    0: '4:3',
    1: '16:9',
    2: '16:10'
}

quality_settings = {
    0: 'LOW',
    1: 'MEDIUM',
    2: 'HIGH',
    3: 'VERY HIGH',

}

effect_settings = {
    0: 'LOW',
    1: 'MEDIUM',
    2: 'HIGH',
}

shadow_quality_settings = {
    0: 'VERY LOW',
    1: 'LOW',
    2: 'MEDIUM',
    3: 'HIGH',
}

FXAA = {

}

MSAA = {
    0: 'None',
    2: '2X MSAA',
    4: '4X MSAA',
    8: '8X MSAA',
    16: '16X MSAA',
}

texture_filtering_mode = {
    0: "Bilinear",
    1: "Trilinear",
    2: "2x",
    4: "4x",
    8: "8x",
    16: "16x",
}


def create_settings_dict(file_content):
    settings = {}
    for item in file_content:
        if 'setting.' in item:
            item = " ".join(item.split()).replace('"', '')
            settings.update({
                item.split(' ')[0].strip(): item.split(' ')[-1].strip()
            })
    return settings


class CsgoVideoConfigParser:
    """For parsing csgo video settings config"""

    def __init__(self, file_content) -> None:
        file_content = file_content.splitlines()
        self.settings = create_settings_dict(file_content)

    def get_resolution(self):
        """To get resolution from video config
        """
        width = self.settings['setting.defaultres']
        height = self.settings['setting.defaultresheight']
        return "{} x {}".format(width, height)

    def get_aspect_ratio(self):
        """To get aspect ratio from video settings
        """
        video_aspect_ratio = self.settings['setting.aspectratiomode']
        ratio = aspect_ratio[int(video_aspect_ratio)]
        return ratio

    def get_display_mode(self):
        """To find the setting in fullscreen or not"""
        fullscreen = self.settings.get('setting.fullscreen')
        if fullscreen == '1':
            return 'Fullscreen'
        return 'Windowed'

    def get_shadow_quality(self):
        """To find the shadow quality from the video settings file"""
        shadow_quality = self.settings.get('setting.csm_quality_level')
        shadow_value = shadow_quality_settings[int(shadow_quality)]
        return shadow_value

    def get_texture_details(self):
        """To find the shadow quality from the video settings file"""
        texture_details = self.settings.get('setting.gpu_mem_level')
        texture_value = quality_settings[int(texture_details)]
        return texture_value

    def get_texture_streaming(self):
        """To find the texture streaming value from video settings"""
        texture_streaming = self.settings.get(
            'setting.mat_texturestreaming', '')
        if texture_streaming == '1':
            return 'Enabled'
        return 'Disabled'

    def get_effect_details(self):
        """To find effect details from video settings"""
        effect_details = self.settings.get('setting.cpu_level', 0)
        effect_value = effect_settings[int(effect_details)]
        return effect_value

    def get_shader_details(self):
        """To find the shader details"""
        shader_details = self.settings.get('setting.gpu_level', 0)
        shader_value = quality_settings[int(shader_details)]
        return shader_value

    def get_rendering_mode(self):
        rendering = self.settings.get('setting.mat_queue_mode', 0)
        if rendering == '-1':
            return 'Enabled'
        return 'Disabled'

    def get_multisampling_anti_aliasing(self):
        msaa = self.settings.get('setting.mat_antialias', 0)
        msaa_value = MSAA[int(msaa)]
        return msaa_value

    def get_fxaa(self):
        fxaa = self.settings.get('setting.mat_software_aa_strength', 0)
        fxaa_value = enable_or_disable[int(fxaa)]
        return fxaa_value

    def get_texture_filtering_mode(self):
        texture_filtering = self.settings.get('setting.mat_forceaniso', 0)
        texture_filtering_value = texture_filtering_mode[int(
            texture_filtering)]
        return texture_filtering_value

    def get_veritcal_sync(self):
        # setting.mat_vsync
        vertical_sync = self.settings.get('setting.mat_vsync', 0)
        vertical_sync_value = enable_or_disable[int(vertical_sync)]
        return vertical_sync_value

    def get_motion_blur(self):
        motion_blur = self.settings.get('setting.mat_motion_blur_enabled', 0)
        motion_blur_value = enable_or_disable[int(motion_blur)]
        return motion_blur_value

    def get_triple_monitor_mode(self):
        triple_monitor = self.settings.get('setting.mat_triplebuffered', 0)
        triple_monitor_value = enable_or_disable[int(triple_monitor)]
        return triple_monitor_value

    def get_whole_settings(self):
        video_settings_dict = {
            'Resolution': self.get_resolution(),
            'Aspect Ratio': self.get_aspect_ratio(),
            # 'Scaling Mode': None,
            # 'Color Mode': None,
            'Display Mode': self.get_display_mode(),
            'Global Shadow Quality': self.get_shadow_quality(),
            'Model_Texture_Detail': self.get_texture_details(),
            'Texture Streaming': self.get_texture_streaming(),
            'Effect Detail': self.get_effect_details(),
            'Shader Detail': self.get_shader_details(),
            # 'Boost Player Contrast': None, # from the config file (r_player_visibility_mode "1")
            'Multicore Rendering': self.get_rendering_mode(),
            'Multisampling Anti-Aliasing Mode': self.get_multisampling_anti_aliasing(),
            'FXAA Anti-Aliasing': self.get_fxaa(),
            'Texture Filtering Mode': self.get_texture_filtering_mode(),
            'Wait for Vertical Sync': self.get_veritcal_sync(),
            'Motion Blur': self.get_motion_blur(),
            'Triple-Monitor Mode': self.get_triple_monitor_mode(),
            # 'Use Uber Shaders': None, Unable to find from settings
        }
        return video_settings_dict
