

import asyncio


class Shell(object):

    async def command(self, *args, **kwargs):
        """Run command in subprocess
        """
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            **kwargs)
        print(
            'Started command:',
            args,
            '(pid = ' + str(process.pid) + ')')
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            print(
                'Command finished:',
                args,
                '(pid = ' + str(process.pid) + ')')
        else:
            print(
                'Command failed:',
                args,
                '(pid = ' + str(process.pid) + ')')
        return stdout.decode().strip()
