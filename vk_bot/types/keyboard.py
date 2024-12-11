from typing import List, Optional
from pydantic import BaseModel, Field

from ..enums import ButtonType, ButtonColor


"""
    Docs:
    https://dev.vk.com/ru/api/bots/development/keyboard
"""


class ButtonAction(BaseModel):
    """
        Object describing the action of a button
    """
    type: ButtonType  # Type of the action (e.g., text, callback, etc.)
    label: Optional[str] = Field(
        None, description="Label of the button, applicable for text and callback types. Max length: 40 characters."
    )
    payload: Optional[dict] = Field(
        None, description="Additional data sent with the button press as a JSON object. Max length: 255 characters."
    )
    link: Optional[str] = Field(
        None, description="URL to open for open_link buttons."
    )
    hash: Optional[str] = Field(
        None, description="Hash for navigation within the app, applicable for open_app buttons."
    )
    app_id: Optional[int] = Field(
        None, description="App ID for the mini-app or game, applicable for open_app buttons."
    )
    owner_id: Optional[int] = Field(
        None, description="Owner ID for the app context, applicable for open_app buttons."
    )


class Button(BaseModel):
    """
        Object describing a button
    """
    action: ButtonAction  # The action the button performs
    color: Optional[ButtonColor] = Field(
        None, description="The color of the button, applicable for text and callback types."
    )


class Keyboard(BaseModel):
    """
        Object describing a keyboard
    """
    buttons: List[List[Button]] = Field(
        ..., description="Array of button rows, each row is a list of Button objects."
    )
    one_time: Optional[bool] = Field(
        default=False,
        description="Whether the keyboard should hide after a button is pressed (true) or stay visible (false).",
    )
    inline: Optional[bool] = Field(
        default=False,
        description="Defines the type of keyboard. Inline keyboards are shown attached to the message.",
    )

    def build(self) -> str:
        """
            Build a JSON string representation of the keyboard object.
        """
        return self.model_dump_json(exclude_none=True)
