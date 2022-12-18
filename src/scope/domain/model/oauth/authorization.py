from ... import security


class Authorization:
    def __init__(
        self,
        state=None,
        provider='Own'
    ) -> None:
        self.state = state if state else self._generate_state()
        self.provider = provider

    def _generate_state(self):
        return security.generate_secret()
