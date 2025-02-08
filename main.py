import asyncio
import sys
import api
import task


async def main():
    # parse cmd
    # await cmd_arg.parse_cmd()
    # start task
    task.start()
    # start api 
    api.start()

if __name__ == '__main__':
    try:
        # asyncio.run(main())
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        sys.exit()
