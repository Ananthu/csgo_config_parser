def find_settings_by_key(file_content, key_list):
    settings = {}
    for key in key_list:
        temp_settings = {
            line.strip().split(' ')[0]: line.strip().split(' ')[-1].strip('"') for line in file_content if key in line and 'bind ' not in line
        }
        settings.update(temp_settings)
    return settings


def find_sensitivity(file_content):
    for item in file_content:
        if item.split(' ')[0].strip() == 'sensitivity':
            return item.split(' ')[-1].strip('"').strip()


def filter_settings(file_content, filter_key_list):
    filtered_list = []
    for item in filter_key_list:
        for line in file_content:
            if item in line:
                continue
            filtered_list.append(line)
    return filtered_list


def find_key_binding(file_content):
    bind_settings = {}
    for item in file_content:
        if item.startswith('bind '):
            item = item.split('bind ')[-1].replace('"', '')
            bind_settings.update({
                item.split(' ')[0].strip(): item.split(' ')[-1].strip()
            })
    return bind_settings


class CsgoConfigParser:
    """For parsing csgo settings config"""

    def __init__(self, file_content) -> None:
        self.config_content = file_content

    def get_crosshair(self):
        """To find the crosshair settings
        """
        key_list = ["cl_crosshair"]
        crosshair_settigs_dict = find_settings_by_key(
            self.config_content, key_list)
        return crosshair_settigs_dict

    def get_viewmodel(self):
        """To find the view model settings
        """
        key_list = ["viewmodel_", "cl_righthand"]
        view_model_dict = find_settings_by_key(self.config_content, key_list)
        return view_model_dict

    def get_bob(self):
        """To find the Bob values
        """
        key_list = ["cl_bob"]
        view_model_dict = find_settings_by_key(self.config_content, key_list)
        return view_model_dict

    def get_sensitivity(self):
        """To find the sensitivity
        """
        sensitivity = find_sensitivity(self.config_content)
        key_list = ['zoom_sensitivity']
        other_sens_settings = find_settings_by_key(
            self.config_content, key_list)
        other_sens_settings['sensitivity'] = sensitivity
        return other_sens_settings

    def get_all_settings(self):
        """retuns all the settings from the parse as dict except bind settings"""
        filter_list = ['bind']
        settngs = filter_settings(self.config_content, filter_list)
        key_list = [' ']
        settngs = find_settings_by_key(settngs, key_list)
        return settngs

    def get_radar_settings(self):
        """To find the radar settings
        """
        key_list = ['cl_radar']
        settngs = find_settings_by_key(self.config_content, key_list)
        return settngs

    def get_hud_settings(self):
        """To find the hud settings
        """
        key_list = ['cl_hud']
        settngs = find_settings_by_key(self.config_content, key_list)
        return settngs

    def get_key_bindings(self):
        """To find the key bindings
        """
        return find_key_binding(self.config_content)
    
    def get_video_settings(self):
        """finds video settings from the config file"""
        key_list = ['mat_monitorgamma']
        settings = find_settings_by_key(self.config_content, key_list)
        return settings
