"""
Wrappers for custom emojis in guilds.

.. currentmodule:: curious.dataclasses.emoji
"""

import typing

from curious.dataclasses import guild as dt_guild, role as dt_role
from curious.dataclasses.bases import Dataclass


class Emoji(Dataclass):
    """
    Represents a custom emoji uploaded to a guild.
    """
    __slots__ = ("id", "name", "role_ids", "require_colons", "managed", "guild_id", "animated")

    def __init__(self, **kwargs):
        super().__init__(int(kwargs.get("id")), kwargs.get("client"))

        #: The name of this emoji.
        self.name = kwargs.get("name", None)  # type: str

        #: A list of role IDs that this emoji can be used by.
        self.role_ids = kwargs.get("roles", [])  # type: typing.List[int]

        #: If this emoji requires colons to use.
        self.require_colons = kwargs.get("require_colons", False)  # type: bool

        #: If this emoji is managed or not.
        self.managed = kwargs.get("managed", False)  # type: bool

        #: The ID of the guild this emoji is associated with.
        self.guild_id = None  # type: int

        #: If this emoji is animated or not.
        self.animated = kwargs.get("animated", False)  # type: bool

    def __eq__(self, other):
        if isinstance(other, str):
            return False

        return self.id == other.id

    def __str__(self):
        return "<{}:{}:{}>".format('a' if self.animated else '', self.name, self.id)

    def __repr__(self):
        return "<Emoji guild={!r} id={!r} name={!r}>".format(self.guild, self.id, self.name)

    async def edit(self, *,
                   name: str = None,
                   roles: 'typing.List[dt_role.Role]' = None) -> 'Emoji':
        """
        Edits this emoji.

        :param name: The new name of the emoji.
        :param roles: The new list of roles that can use this emoji.
        :return: This emoji.
        """
        if roles is not None:
            roles = [r.id for r in roles]

        await self._bot.http.edit_guild_emoji(guild_id=self.guild_id, emoji_id=self.id,
                                              name=name, roles=roles)
        return self

    async def delete(self):
        """
        Deletes this emoji.
        """
        await self._bot.http.delete_guild_emoji(self.guild_id, emoji_id=self.id)

    @property
    def guild(self) -> 'dt_guild.Guild':
        """
        :return: The :class:`.Guild` this emoji object is associated with.
        """
        return self._bot.guilds.get(self.guild_id)

    @property
    def roles(self) -> 'typing.List[dt_role.Role]':
        """
        :return: A list of :class:`.Role` this emoji can be used by.
        """
        if len(self.role_ids) <= 0:
            return [self.guild.default_role]

        return [self.guild.roles[r_id] for r_id in self.role_ids]

    @property
    def url(self) -> str:
        """
        :return: The URL to this emoji.
        """
        if not self.animated:
            return "https://cdn.discordapp.com/emojis/{}.png".format(self.id)

        return f"https://cdn.discordapp.com/emojis/{self.id}.gif"
