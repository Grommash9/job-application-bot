from bot_app import db


class Param:
    param_title: str
    is_enabled: bool
    internal_id: int

    def __init__(self, title: str, internal_id: int, is_enabled=False):
        self.param_title = title
        self.is_enabled = is_enabled
        self.internal_id = internal_id

    def switch(self):
        if self.is_enabled:
            self.is_enabled = False
        else:
            self.is_enabled = True


class Params:
    param_list: list[Param]

    def __init__(self, params_list: list):
        self.param_list = [Param(params_data['title'], params_data['internal_id'], params_data['is_enabled'])
                          for params_data in params_list]

    def get_dict(self):
        return [{'title': param.param_title,
                 'is_enabled': param.is_enabled,
                 'internal_id': param.internal_id} for param in self.param_list]

    def switch_job(self, job_id):
        for param in self.param_list:
            if param.internal_id == int(job_id):
                param.switch()
                break
        return self.param_list, self.get_dict()

    def get_all_enabled_str(self) -> str:
        enabled_params = [param.param_title for param in self.param_list if param.is_enabled]
        if len(enabled_params) == 0:
            return 'Ничего не выбрано'
        enabled_params = ', '.join(enabled_params)
        return enabled_params

