__version__ = (3, 0, 2)
# meta developer: @foxy437
# what new: New repository github.com/TheKsenon/MyHikkaModules

import requests
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from .. import loader, utils
import re
import os
import gdown
import inspect
import io
import ast
from hikkatl.types import Message

@loader.tds
class FHeta(loader.Module):
    '''Module for searching modules! Upload your modules to FHeta via fheta_robot.t.me!'''
    strings = {
        "name": "FHeta",
        "search": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Searching...</b>",
        "no_query": "<emoji document_id=5348277823133999513>❌</emoji> <b>Enter a query to search.</b>",
        "searching_by_command": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Searching by name failed, starting to search by command...</b>\n\n<emoji document_id=5325783112309817646>❕</emoji> <b>This is a long process, approximate waiting time is 2-3 minutes.</b>",
        "no_modules_found": "<emoji document_id=5348277823133999513>❌</emoji> <b>No modules found.</b>",
        "commands": "\n<emoji document_id=5190498849440931467>👨‍💻</emoji> <b>Commands:</b>\n{commands_list}",
        "description": "\n<emoji document_id=5433653135799228968>📁</emoji> <b>Description:</b> {description}",
        "result": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Result {index} for:</b> <code>{query}</code>\n<b>{module_name}</b> by {author}\n<emoji document_id=4985961065012527769>🖥</emoji> <b>Repository:</b> {repo_url}\n<emoji document_id=5307585292926984338>💾</emoji> <b>Command for installation:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "<emoji document_id=5348277823133999513>❌</emoji> <b>Failed to fetch the FHeta.</b>",
        "actual_version": "<emoji document_id=5436040291507247633>🎉</emoji> <b>You have the actual</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "<emoji document_id=5260293700088511294>⛔️</emoji> <b>You have the old version </b><code>FHeta (v{version})</code><b>.</b>\n\n<emoji document_id=5382357040008021292>🆕</emoji> <b>New version</b> <code>v{new_version}</code><b> available!</b>\n",
        "update_whats_new": "<emoji document_id=5307761176132720417>⁉️</emoji> <b>What’s new:</b><code> {whats_new}</code>\n\n",
        "update_command": "<emoji document_id=5298820832338915986>🔄</emoji> <b>To update type: <code>{update_command}</code></b>"
    }

    strings_ru = {
        "name": "FHeta",
        "search": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Поиск...</b>",
        "no_query": "<emoji document_id=5348277823133999513>❌</emoji> <b>Введите запрос для поиска.</b>",
        "searching_by_command": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Поиск по названию не дал результатов, начинаем поиск по командам...</b>\n\n<emoji document_id=5325783112309817646>❕</emoji> <b>Это займет немного больше времени, приблизительно 2-3 минуты.</b>",
        "no_modules_found": "<emoji document_id=5348277823133999513>❌</emoji> <b>Модули не найдены.</b>",
        "commands": "\n<emoji document_id=5190498849440931467>👨‍💻</emoji> <b>Команды:</b>\n{commands_list}",
        "description": "\n<emoji document_id=5433653135799228968>📁</emoji> <b>Описание:</b> {description}",
        "result": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Результат {index} для:</b> <code>{query}</code>\n<b>{module_name}</b> от {author}\n<emoji document_id=4985961065012527769>🖥</emoji> <b>Репозиторий:</b> {repo_url}\n<emoji document_id=5307585292926984338>💾</emoji> <b>Команда для установки:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "<emoji document_id=5348277823133999513>❌</emoji> <b>Не удалось получить данные для FHeta.</b>",
        "actual_version": "<emoji document_id=5436040291507247633>🎉</emoji> <b>У вас актуальная версия</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "<emoji document_id=5260293700088511294>⛔️</emoji> <b>У вас старая версия </b><code>FHeta (v{version})</code><b>.</b>\n\n<emoji document_id=5382357040008021292>🆕</emoji> <b>Доступна новая версия</b> <code>v{new_version}</code><b>!</b>\n",
        "update_whats_new": "<emoji document_id=5307761176132720417>⁉️</emoji> <b>Что нового:</b><code> {whats_new}</code>\n\n",
        "update_command": "<emoji document_id=5298820832338915986>🔄</emoji> <b>Чтобы обновиться, напишите: <code>{update_command}</code></b>"
    }

    repos = [
        "Fixyres/Modules",
        "C0dwiz/H.Modules",
        "AmoreForever/amoremods",
        "vsecoder/hikka_modules",
        "iamnalinor/FTG-modules",
        "musiczhara0/sosat",
        "Den4ikSuperOstryyPer4ik/Astro-modules",
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
        "idiotcoders/idiotmodules",
        "TheKsenon/MyHikkaModules"
    ]

    def __init__(self):
        file_id = "1j1MG4wpPv0JPHOyctCRkHTDAgUD-Nh_v"
        url = f"https://drive.google.com/uc?id={file_id}"
        output = "token.txt"
        gdown.download(url, output, quiet=False)
        with open(output, "r") as file:
            self.token = file.read().strip()

    @loader.command(
             en_doc="<query> - search modules.", 
             ru_doc="<запрос> - искать модули."
    )
    async def fheta(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_query"))
            return

        await utils.answer(message, self.strings("search"))
        modules = await self.search_modules_parallel(args)

        if not modules:
            args = args.replace(" ", "")
            modules = await self.search_modules_parallel(args)

        if not modules:
            await utils.answer(message, self.strings("searching_by_command"))
            modules = await self.search_modules_by_command_parallel(args)

        if not modules:
            await utils.answer(message, self.strings("no_modules_found"))
        else:
            results = ""
            seen_modules = set()
            result_index = 1

            for module in modules:
                repo_url = f"https://github.com/{module['repo']}"
                download_url = module['download_url']

                commands_section = ""
                if module['commands']:
                    commands_list = "\n".join([f"<code>{self.get_prefix()}{cmd['name']}</code> {cmd['description']}" for cmd in module['commands']])
                    commands_section = self.strings("commands").format(commands_list=commands_list)

                description_section = ""
                description = await self.get_module_description(download_url)
                if description:
                    description_section = self.strings("description").format(description=description)

                author_info = await self.get_author_from_file(download_url)
                module_name = module['name'].replace('.py', '')
                module_key = f"{module_name}_{author_info}"

                if module_key in seen_modules:
                    continue
                seen_modules.add(module_key)

                result = self.strings("result").format(
                    index=result_index,
                    query=args,
                    module_name=module_name,
                    author=author_info,
                    repo_url=repo_url,
                    install_command=f"{self.get_prefix()}dlm {download_url}",
                    description=description_section,
                    commands=commands_section
                )
                results += result
                result_index += 1

            await utils.answer(message, results)
            
    @loader.command(
        en_doc = ' - check update.', 
        ru_doc = ' - проверить обновления.'
    )
    async def fupdate(self, message: Message):
        module_name = "FHeta"
        module = self.lookup(module_name)
        sys_module = inspect.getmodule(module)

        local_file = io.BytesIO(sys_module.__loader__.data)
        local_file.name = f"{module_name}.py"
        local_file.seek(0)
        local_first_line = local_file.readline().strip().decode("utf-8")
        
        correct_version = sys_module.__version__
        correct_version_str = ".".join(map(str, correct_version))

        headers = {'Authorization': f'token {self.token}'}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get("https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/FHeta.py") as response:
                if response.status == 200:
                    remote_content = await response.text()
                    remote_lines = remote_content.splitlines()

                    new_version = remote_lines[0].split("=", 1)[1].strip().strip("()").replace(",", "").replace(" ", ".")
                    what_new = remote_lines[2].split(":", 1)[1].strip() if len(remote_lines) > 2 and remote_lines[2].startswith("# what new:") else ""
                    
                else:
                    await utils.answer(message, self.strings("fetch_failed"))
                    return

        if local_first_line.replace(" ", "") == remote_lines[0].strip().replace(" ", ""):
            await utils.answer(message, self.strings("actual_version").format(version=correct_version_str))
        else:
            update_message = self.strings("old_version").format(version=correct_version_str, new_version=new_version)
            if what_new:
                update_message += self.strings("update_whats_new").format(whats_new=what_new)
            update_message += self.strings("update_command").format(update_command=f"{self.get_prefix()}dlm https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/FHeta.py")
            await utils.answer(message, update_message)
                                  
    async def search_modules_parallel(self, query: str):
        found_modules = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.search_repo(repo, query, session) for repo in self.repos]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    found_modules.extend(result)
        return found_modules

    async def search_modules_by_command_parallel(self, query: str):
        found_modules = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.search_repo_by_command(repo, query, session) for repo in self.repos]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    found_modules.extend(result)
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

    async def search_modules_parallel(self, query: str):
        found_modules = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.search_repo(repo, query, session) for repo in self.repos]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    found_modules.extend(result)
        return found_modules

    async def search_modules_by_command_parallel(self, query: str):
        found_modules = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.search_repo_by_command(repo, query, session) for repo in self.repos]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    found_modules.extend(result)
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
                        if any(isinstance(cmd, dict) and 'name' in cmd and query.lower() in cmd['name'].lower() for cmd in commands):
                            result.append({
                                "name": item['name'],
                                "repo": repo,
                                "commands": commands,
                                "download_url": item['download_url']
                            })
                return result
            return []

    async def get_commands_from_module(self, download_url, session):
        async with session.get(download_url) as response:
            if response.status == 200:
                content = await response.text()
                return self.extract_commands(content)
        return {}

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
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef) and any(
                            isinstance(base, ast.Attribute) and base.attr == "Module" 
                            for base in node.bases
                        ):
                            return ast.get_docstring(node) or ""
        return ""

    @staticmethod
    def extract_commands(content):
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        commands = []
        def get_decorator_names(decorator_list):
            return [ast.unparse(decorator) for decorator in decorator_list]

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for class_body_node in node.body:
                    if isinstance(class_body_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        decorators = get_decorator_names(class_body_node.decorator_list)
                        is_loader_command = any("command" in decorator for decorator in decorators)

                        if is_loader_command or class_body_node.name.endswith("cmd"):
                            method_docstring = ast.get_docstring(class_body_node)
                            command_name = class_body_node.name
                            if command_name.endswith("cmd"):
                                command_name = command_name[:-3]

                            command_info = {
                                "name": command_name,
                                "description": method_docstring or ""
                            }
                            commands.append(command_info)

        return commands
