"""Обработчики команд и событий

Команды и события генерируются в точках входа, см. /entrypoints
"""

from .. import config
from ..domain import commands, events, model
from . import exceptions, oauth_provider, unit_of_work


async def create_authorization(
    cmd: commands.CreateAuthorization,
    uow: unit_of_work.AbstractUnitOfWork
) -> str:
    with uow:
        state = model.State()
        auth = model.Authorization(
            state=state,
            provider_name=cmd.provider_name
        )
        uow.authorizations.add(auth)
        uow.commit()
        return state.state


async def auth_code_recieved(
    evt: events.AuthCodeRecieved,
    uow: unit_of_work.AbstractUnitOfWork
):
    """Обработчик команды Обработать код авторизации
    """
    with uow:
        auth = uow.authorizations.get_by_state_code(evt.state_code)
        if auth is None or not auth.is_active:
            raise exceptions.InvalidState("No active authorization found")

        # Exception: are we under attack?
        if not auth.state.is_active:
            # if we are, then invoke authorization
            auth.deactivate()
            uow.commit()
            # auth.events.append(commands.deactivate!!!)
            raise exceptions.InactiveState("State is inactive")
        auth.state.deactivate()

        grant = model.Grant(
            grant_type="authorization_code",
            code=evt.grant_code
        )
        auth.grants.append(grant)
        uow.commit()
        # Now, authorization must get access token using the auth code
        auth.events.append(
            commands.RequestToken(grant_code=grant.code),
        )


async def request_token(
    cmd: commands.RequestToken,
    uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        if cmd.grant_code:
            auth = uow.authorizations.get_by_grant_code(cmd.grant_code)
        elif cmd.token:
            auth = uow.authorizations.get_by_token(cmd.token)
        if not auth or not auth.is_active:
            raise exceptions.InvalidGrant("No active authorization found")

        old_grant = auth.get_grant_by_code(cmd.grant_code)
        if not old_grant or not old_grant.is_active:
            raise exceptions.InvalidGrant(
                "No grant found for token requesting"
            )
        old_grant.deactivate()

        old_token = auth.get_active_token()
        if old_token:
            old_token.deactivate()

        oauth = cmd.oauth
        if not oauth:
            scopes, urls = config.get_oauth_params(auth.provider_name)
            oauth = oauth_provider.OAuthProvider(
                provider_name=auth.provider_name,
                scopes=scopes,
                code_url=urls['code'],
                token_url=urls['token'],
                public_keys_url=urls['public_keys']
            )
        await oauth.request_token(grant=old_grant)

        new_token = await oauth.get_token()
        auth.tokens.append(new_token)

        new_grant = await oauth.get_grant()
        if new_grant:
            auth.grants.append(new_grant)

        uow.commit()
        return new_token.access_token
