def command_handler(func):
    async def wrapper(self, *args, **kwargs):
        async with self.uow:
            try:
                result = await func(self, *args, **kwargs)
                await self.uow.commit()
                return result
            except Exception:
                await self.uow.rollback()
                raise

    return wrapper


def query_handler(func):
    async def wrapper(self, *args, **kwargs):
        async with self.uow:
            result = await func(self, *args, **kwargs)
            return result

    return wrapper
