# meta developer: @foxy437

import requests
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from .. import loader, utils
import re
import os
import gdown

class FHeta(loader.Module):
    '''Module for searching modules! Upload your modules in fheta_bot.t.me'''
    strings = {"name": "FHeta"}

    repos = [
        "C0dwiz/H.Modules",
        "Den4ikSuperOstryyPer4ik/Astro-modules",
        "AmoreForever/amoremods",
        "vsecoder/hikka_modules",
        "iamnalinor/FTG-modules",
        "musiczhara0/sosat",
        "Fixyres/Modules",
        "hikariatama/ftg",
        "N3rcy/modules",
        "FajoX1/FAmods",
        "kayt3m/modules",
        "sqlmerr/hikka_mods",
        "Ijidishurka/modules",
        "dorotorothequickend/DorotoroModules",
        "kezuhiro-web/modules",
        "coddrago/modules",
        "Slaik78/ModulesHikkaFromSlaik",
        "Daniel1236n29/Modules_hikka",
        "D4n13l3k00/FTG-Modules",
        "chebupelka10/HikkaModules",
        "KorenbZla/Hikka",
        "Vsakoe/HK",
        "anon97945/hikka-mods",
        "N3rcy/modules",
        "MuRuLOSE/HikkaModulesRepo",
        "shadowhikka/sh.modules",
        "amm1edev/ame_repo",
        "1jpshiro/hikka-modules",
        "MoriSummerz/ftg-mods",
        "dekkusudev/mm-hikka-mods",
        "idiotcoders/idiotmodules"
    ]

    def __init__(self):
        file_id = "1VVPSiuKaMnVbKT6dq-6u3gYM-dSa2pkZ"
        url = f"https://drive.google.com/uc?id={file_id}"
        output = "token.txt"
        gdown.download(url, output, quiet=False)
        with open(output, "r") as file:
            self.token = file.read().strip()

    @loader.command()
    async def fheta(self, message):
        '''<query> - search modules.'''
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<emoji document_id=5348277823133999513>❌</emoji> <b>Enter a query to search.</b>")
            return

        await utils.answer(message, "<emoji document_id=5188311512791393083>🔎</emoji> <b>Searching...</b>")

        modules = await self.search_modules_parallel(args)

        if not modules:
            args = args.replace(" ", "")
            modules = await self.search_modules_parallel(args)

        if not modules:
            modules = await self.search_modules_by_command_parallel(args)

        if not modules:
            await utils.answer(message, "<emoji document_id=5348277823133999513>❌</emoji> <b>No modules found.</b>")
        else:
            results = ""
            seen_modules = set()
            result_index = 1

            for module in modules:
                repo_url = f"https://github.com/{module['repo']}"
                download_url = module['download_url']
 
                commands_section = ""
                if module['commands']:
                    commands_list = "\n".join([f"<code>{self.get_prefix()}{cmd}</code> {desc}" for cmd, desc in module['commands'].items()])
                    commands_section = f"\n<emoji document_id=5190498849440931467>👨‍💻</emoji> <b>Commands:</b>\n{commands_list}"

                description_section = ""
                description = await self.get_module_description(download_url)
                if description:
                    description_section = f"\n<emoji document_id=5433653135799228968>📁</emoji> <b>Description:</b> {description}"

                if "heta.hikariatama.ru" in download_url:
                    repo, module_name = await self.get_github_link(module['repo'], module['name'])
                    branch = await self.get_github_branch(repo, module_name)
                    download_url = f"https://raw.githubusercontent.com/{repo}/refs/heads/{branch}/{module_name}.py"
                
                author_info = await self.get_author_from_file(download_url)
                module_name = module['name'].replace('.py', '')
                module_key = f"{module_name}_{author_info}"

                if module_key in seen_modules:
                    continue
                seen_modules.add(module_key)

                result = f"<emoji document_id=5188311512791393083>🔎</emoji> <b>Result {result_index} for:</b> <code>{args}</code>\n<b>{module_name}</b> by {author_info}\n<emoji document_id=4985961065012527769>🖥</emoji> <b>Repository:</b> {repo_url}\n<emoji document_id=5307585292926984338>💾</emoji> <b>Command for installation:</b> <code>{self.get_prefix()}dlm {download_url}</code>{description_section}{commands_section}\n\n\n"
                results += result
                result_index += 1

            await utils.answer(message, results)
   
    @loader.command()
    async def fupdate(self, message):
        '''- check update.'''
        url = "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/FHeta.py"

        user = await self._client.get_me()
        user_id = str(user.id)

        current_directory = os.getcwd()
        local_file_path = os.path.join(current_directory, "loaded_modules", f"FHeta_{user_id}.py")

        try:
            with open(local_file_path, "r") as local_file:
                local_code = local_file.read().strip()
        except FileNotFoundError:
            local_code = ""

        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"token {self.token}"}
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        remote_code = (await response.text()).strip()
                    else:
                        await utils.answer(message, "<emoji document_id=5348277823133999513>❌</emoji> <b>Could not fetch update.</b>")
                        return
            except aiohttp.ClientError:
                await utils.answer(message, "<emoji document_id=5348277823133999513>❌</emoji> <b>Could not fetch update.</b>")
                return

            if local_code.replace(" ", "") != remote_code.replace(" ", ""):
                prefix = self.get_prefix()
                await utils.answer(
                    message,
                    f"<emoji document_id=5188311512791393083>🔎</emoji> <b>You are using an outdated version of </b><code>Fheta</code><b>!</b>\n\n"
                    f"<b>To update, type:</b> <code>{prefix}dlm {url}</code>"
                )
            else:
                await utils.answer(message, "<emoji document_id=5348277823133999513>✅</emoji> <b>No update found.</b>")

    async def search_modules_parallel(self, query: str):
        found_modules = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.search_repo(repo, query, session) for repo in self.repos]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    found_modules.extend(result)

        heta_results = await self.search_heta_parallel(query)
        found_modules.extend(heta_results)
        return found_modules

    async def search_repo(self, repo, query, session):
        url = f"https://api.github.com/repos/{repo}/contents"
        headers = {
            'Authorization': f'token {self.token}'
        }
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return [
                    {
                        "name": item['name'],
                        "repo": repo,
                        "commands": await self.get_commands_from_module(item['download_url'], session),
                        "download_url": item['download_url']
                    }
                    for item in data if item['name'].endswith('.py') and query.lower() in item['name'].lower()
                ]
            return []

    async def search_heta_parallel(self, query):
        found_modules = []
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.search_heta_range(query, session, i * 4, (i + 1) * 4)
                for i in range(25)
            ]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    found_modules.extend(result)
        return found_modules

    async def search_heta_range(self, query, session, start, end):
        url = "https://heta.dan.tatar/modules.json"
        async with session.get(url) as response:
            if response.status == 200:
                heta_data = await response.json()
                length = len(heta_data)
                range_data = heta_data[int(length * start / 100):int(length * end / 100)]
                return [
                    {
                        "name": module['name'],
                        "repo": module['repo'],
                        "commands": module.get('commands', {}),
                        "download_url": module['link']
                    }
                    for module in range_data if query.lower() in module['name'].lower()
                ]
            return []

    async def search_modules_by_command_parallel(self, query: str):
        found_modules = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.search_repo_by_command(repo, query, session) for repo in self.repos]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    found_modules.extend(result)

        heta_results = await self.search_heta_by_command_parallel(query)
        found_modules.extend(heta_results)
        return found_modules

    async def search_repo_by_command(self, repo, query, session):
        url = f"https://api.github.com/repos/{repo}/contents"
        headers = {
            'Authorization': f'token {self.token}'
        }
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                result = []
                for item in data:
                    if item['name'].endswith('.py'):
                        commands = await self.get_commands_from_module(item['download_url'], session) or ["<emoji document_id=5427052514094619126>🙅‍♂️</emoji>"]
                        if any(query.lower() in cmd.lower() for cmd in commands):
                            result.append({
                                "name": item['name'],
                                "repo": repo,
                                "commands": commands,
                                "download_url": item['download_url']
                            })
                return result
            return []

    async def search_heta_by_command_parallel(self, query):
        found_modules = []
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.search_heta_by_command_range(query, session, i * 4, (i + 1) * 4)
                for i in range(25)
            ]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    found_modules.extend(result)
        return found_modules

    async def search_heta_by_command_range(self, query, session, start, end):
        url = "https://heta.dan.tatar/modules.json"
        async with session.get(url) as response:
            if response.status == 200:
                heta_data = await response.json()
                length = len(heta_data)
                range_data = heta_data[int(length * start / 100):int(length * end / 100)]
                result = []
                for module in range_data:
                    commands = module.get('commands', {})
                    if any(query.lower() in cmd.lower() for cmd in commands):
                        result.append({
                            "name": module['name'],
                            "repo": module['repo'],
                            "commands": commands,
                            "download_url": module['link']
                        })
                return result
            return []

    async def get_commands_from_module(self, download_url, session):
        async with session.get(download_url) as response:
            if response.status == 200:
                content = await response.text()
                return self.extract_commands(content)
        return {}

    async def get_github_link(self, repo, module_name):
        url = f"https://api.github.com/repos/{repo}/contents"
        headers = {
            'Authorization': f'token {self.token}'
        }
        async with aiohttp.ClientSession() as session:
           async with session.get(url, headers=headers) as response:
               if response.status == 200:
                   data = await response.json()
                   for item in data:
                       if item['name'].lower() == module_name.lower():
                           return repo, item['name']
           return repo, module_name

    async def get_github_branch(self, repo, module_name):
        url = f"https://api.github.com/repos/{repo}/branches"
        headers = {
            'Authorization': f'token {self.token}'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    for branch in data:
                        branch_name = branch['name']
                        module_url = f"https://raw.githubusercontent.com/{repo}/refs/heads/{branch_name}/{module_name}.py"
                        async with session.get(module_url) as module_response:
                            if module_response.status == 200:
                                return branch_name
        return "master"

    async def get_author_from_file(self, download_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(download_url) as response:
                if response.status == 200:
                    content = await response.text()
                    author_line = next((line for line in content.split('\n') if line.startswith("# meta developer:")), None)
                    if author_line:
                        return author_line.split(":")[1].strip()
        return "???"

    async def get_module_description(self, download_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(download_url) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    match = re.search(
                        r'class\s+\w+\(loader\.Module(?:, \w+)*\):\s+[\'"]{3}([\s\S]*?)[\'"]{3}',
                        content,
                        re.DOTALL
                    )
                    if match:
                        return match.group(1).strip()
                    
                    match = re.search(
                        r'class\s+\w+\(loader\.Module(?:, \w+)*\):\s+[\'"]{3}(.+?)[\'"]{3}',
                        content
                    )
                    if match:
                        return match.group(1).strip()
        return ""

    def extract_commands(self, content):
        commands = {}
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if '@loader.command' in line or '@loader.sudo' in line:
                cmd_name_line = lines[i + 1].strip()
                if 'async def' in cmd_name_line:
                    cmd_name = cmd_name_line.split('async def ')[1].split('(')[0]
                    if cmd_name.endswith('cmd'):
                        cmd_name = cmd_name[:-3]
                    
                    description = []
                    in_description = False
                    
                    for desc_line in lines[i + 2:]:
                        desc_line = desc_line.strip()
                        if desc_line.startswith('"""') or desc_line.startswith("'''"):
                            if in_description:
                                break
                            else:
                                in_description = True
                                description.append(desc_line.strip('"""').strip("'''"))
                        elif in_description:
                            if desc_line.endswith('"""') or desc_line.endswith("'''"):
                                description.append(desc_line.strip('"""').strip("'''"))
                                break
                            description.append(desc_line)

                    if description:
                        commands[cmd_name] = " ".join(description).strip()
                        
            elif 'async def' in line:
                cmd_name = line.split('async def ')[1].split('(')[0]
                if cmd_name.endswith('cmd'):
                    cmd_name = cmd_name[:-3]
                description_match = re.search(r'"""(.*?)"""|\'\'\'(.*?)\'\'\'', lines[i + 1].strip())
                if description_match:
                    command_description = description_match.group(1) or description_match.group(2)
                    if command_description:
                        commands[cmd_name] = command_description.strip()
                        
        return commands if commands else None
