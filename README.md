# vk bot framework like "aiogram"

### Description

Библиотека для написания ВК бота, подобная aiogram3

### Source docs

https://dev.vk.com/ru/reference

### Installing

```bash
git clone https://github.com/Oven29/vk_bot
pip install -r vk_bot/requirements.txt
```
or
```bash
pip install git+https://github.com/Oven29/vk_bot
```

### Example of usage

```python
import logging
import asyncio

from framework import Dispatcher, Router, API, types, filters, enums

import config


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Creating a router instance
router = Router()


@router(filters.MessageFilter())
async def echo(event: types.Event, api: API) -> int:
    keyboard = types.Keyboard(
        buttons=[
            [
                types.Button(
                    action=types.ButtonAction(
                        type=enums.ButtonType.TEXT,
                        label="Hello",
                    ),
                    color=enums.ButtonColor.POSITIVE,
                ),
            ],
            [
                types.Button(
                    action=types.ButtonAction(
                        type=enums.ButtonType.TEXT,
                        label="Goodbye",
                    ),
                    color=enums.ButtonColor.NEGATIVE,
                ),
            ],
        ],
    )

    # Must return message id or tuple of messages id to sent
    return await api.messages.send(
        user_id=event.peer_id,
        random_id=0,
        message=event.text,
        keyboard=keyboard.build(),
    )


async def main() -> None:
    dp = Dispatcher(config.VK_BOT_TOKEN)

    dp.include_routers(router)

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())

```
