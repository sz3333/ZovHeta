__version__ = (3, 2, 2)
# meta developer: @Foxy437
# change-log: 🎉 REWORK SEARCHING!!!!!! Bug fix.

import requests
import asyncio
import aiohttp
from .. import loader, utils
import json
import io
import inspect
from hikkatl.types import Message
from difflib import get_close_matches
import random

@loader.tds
class FHeta(loader.Module):
    '''Module for searching modules! Upload your modules to FHeta via fheta_robot.t.me!'''
    
    strings = {
        "name": "FHeta",
        "search": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Searching...</b>",
        "no_query": "<emoji document_id=5348277823133999513>❌</emoji> <b>Enter a query to search.</b>",
        "no_modules_found": "<emoji document_id=5348277823133999513>❌</emoji> <b>No modules found.</b>",
        "commands": "\n<emoji document_id=5190498849440931467>👨‍💻</emoji> <b>Commands:</b>\n{commands_list}",
        "description": "\n<emoji document_id=5433653135799228968>📁</emoji> <b>Description:</b> {description}",
        "result": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Result {index} for:</b> <code>{query}</code>\n<b>{module_name}</b> by {author}\n<emoji document_id=4985961065012527769>🖥</emoji> <b>Repository:</b> {repo_url}\n<emoji document_id=5307585292926984338>💾</emoji> <b>Command for installation:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "<emoji document_id=5348277823133999513>❌</emoji> <b>Failed to fetch the FHeta.</b>",
        "actual_version": "<emoji document_id=5436040291507247633>🎉</emoji> <b>You have the actual</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "<emoji document_id=5260293700088511294>⛔️</emoji> <b>You have the old version </b><code>FHeta (v{version})</code><b>.</b>\n\n<emoji document_id=5382357040008021292>🆕</emoji> <b>New version</b> <code>v{new_version}</code><b> available!</b>\n",
        "update_whats_new": "<emoji document_id=5307761176132720417>⁉️</emoji> <b>Change-log:</b><code> {whats_new}</code>\n\n",
        "update_command": "<emoji document_id=5298820832338915986>🔄</emoji> <b>To update type: <code>{update_command}</code></b>",
        "closest_match": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Closest match found:</b>\n<code>{module_name}</code> by {author}\n<emoji document_id=4985961065012527769>🖥</emoji> <b>Repository:</b> {repo_url}\n<emoji document_id=5307585292926984338>💾</emoji> <b>Command for installation:</b> <code>{install_command}</code>{description}{commands}\n\n"
    }

    strings_ru = {
        "name": "FHeta",
        "search": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Поиск...</b>",
        "no_query": "<emoji document_id=5348277823133999513>❌</emoji> <b>Введите запрос для поиска.</b>",
        "no_modules_found": "<emoji document_id=5348277823133999513>❌</emoji> <b>Модули не найдены.</b>",
        "commands": "\n<emoji document_id=5190498849440931467>👨‍💻</emoji> <b>Команды:</b>\n{commands_list}",
        "description": "\n<emoji document_id=5433653135799228968>📁</emoji> <b>Описание:</b> {description}",
        "result": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Результат {index} для:</b> <code>{query}</code>\n<b>{module_name}</b> от {author}\n<emoji document_id=4985961065012527769>🖥</emoji> <b>Репозиторий:</b> {repo_url}\n<emoji document_id=5307585292926984338>💾</emoji> <b>Команда для установки:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "<emoji document_id=5348277823133999513>❌</emoji> <b>Не удалось получить данные для FHeta.</b>",
        "actual_version": "<emoji document_id=5436040291507247633>🎉</emoji> <b>У вас актуальная версия</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "<emoji document_id=5260293700088511294>⛔️</emoji> <b>У вас старая версия </b><code>FHeta (v{version})</code><b>.</b>\n\n<emoji document_id=5382357040008021292>🆕</emoji> <b>Доступна новая версия</b> <code>v{new_version}</code><b>!</b>\n",
        "update_whats_new": "<emoji document_id=5307761176132720417>⁉️</emoji> <b>Change-log:</b><code> {whats_new}</code>\n\n",
        "update_command": "<emoji document_id=5298820832338915986>🔄</emoji> <b>Чтобы обновиться напишите: <code>{update_command}</code></b>",
        "closest_match": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Ближайшое совпадение:</b>\n<code>{module_name}</code> от {author}\n<emoji document_id=4985961065012527769>🖥</emoji> <b>Репозиторий:</b> {repo_url}\n<emoji document_id=5307585292926984338>💾</emoji> <b>Команда для установки:</b> <code>{install_command}</code>{description}{commands}\n\n"
    }

    @loader.command(ru_doc="<запрос> - искать модули.")
    async def fheta(self, message):
        '''<query> - search modules.'''
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_query"])
            return

        await utils.answer(message, self.strings["search"])
        modules = await self.search_modules(args)

        if not modules:
            modules = await self.search_modules(args.replace(" ", ""))

        if not modules:
            modules = await self.get_closest_match(args)

            if modules:
                await self.send_result_with_video(message, modules)
            else:
                await utils.answer(message, self.strings["no_modules_found"])
        else:
            if len(modules) == 1:
                await self.send_result_with_video(message, await self.format_module(modules[0], args))
            else:
                results = ""
                seen_modules = set()
                result_index = 1

                for module in modules:
                    repo_url = f"https://github.com/{module['repo']}"
                    install = module['install']

                    commands_section = ""
                    if "commands" in module:
                        commands_list = "\n".join([f"<code>{self.get_prefix()}{cmd['name']}</code> {cmd['description']}" for cmd in module['commands']])
                        commands_section = self.strings["commands"].format(commands_list=commands_list)

                    description_section = ""
                    if "description" in module:
                        description_section = self.strings["description"].format(description=module["description"])

                    author_info = module.get("author", "???")
                    module_name = module['name'].replace('.py', '')
                    module_key = f"{module_name}_{author_info}"

                    if module_key in seen_modules:
                        continue
                    seen_modules.add(module_key)

                    result = self.strings["result"].format(
                        index=result_index,
                        query=args,
                        module_name=module_name,
                        author=author_info,
                        repo_url=repo_url,
                        install_command=f"{self.get_prefix()}{install}",
                        description=description_section,
                        commands=commands_section
                    )
                    results += result
                    result_index += 1

                await utils.answer(message, results)

    @loader.command(ru_doc=' - проверить обновления.')
    async def fupdate(self, message: Message):
        ''' - check update.'''
        module_name = "FHeta"
        module = self.lookup(module_name)
        sys_module = inspect.getmodule(module)

        local_file = io.BytesIO(sys_module.__loader__.data)
        local_file.name = f"{module_name}.py"
        local_file.seek(0)
        local_first_line = local_file.readline().strip().decode("utf-8")
        
        correct_version = sys_module.__version__
        correct_version_str = ".".join(map(str, correct_version))

        async with aiohttp.ClientSession() as session:
            async with session.get("https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/FHeta.py") as response:
                if response.status == 200:
                    remote_content = await response.text()
                    remote_lines = remote_content.splitlines()

                    new_version = remote_lines[0].split("=", 1)[1].strip().strip("()").replace(",", "").replace(" ", ".")
                    what_new = remote_lines[2].split(":", 1)[1].strip() if len(remote_lines) > 2 and remote_lines[2].startswith("# change-log:") else ""
                    
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

    async def get_closest_match(self, query: str):
        url = "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/modules.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.text()
                    modules = json.loads(data)
                    
                    module_names = [module['name'] for module in modules]
                    closest_matches = get_close_matches(query, module_names, n=1, cutoff=0.5)

                    if closest_matches:
                        module = next((m for m in modules if m['name'] == closest_matches[0]), None)
                        if module:
                            return await self.format_module(module, query)
                    return None

    async def search_modules(self, query: str):
        url = "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/modules.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.text()
                    modules = json.loads(data)

                    found_modules = [
                        module for module in modules
                        if query.lower() in module.get("name", "").lower()
                    ]
                    
                    if not found_modules:
                        found_modules = [
                            module for module in modules
                            if any(query.lower() in cmd.get("name", "").lower() for cmd in module.get("commands", []))
                        ]
                    
                    if not found_modules:
                        found_modules = [
                            module for module in modules
                            if query.lower() in module.get("author", "").lower()
                        ]

                    if not found_modules:
                        found_modules = [
                            module for module in modules
                            if query.lower() in module.get("description", "").lower()
                        ]

                    return found_modules

    async def format_module(self, module, query):
        repo_url = f"https://github.com/{module['repo']}"
        install = module['install']

        commands_section = ""
        if "commands" in module:
            commands_list = "\n".join([f"<code>{self.get_prefix()}{cmd['name']}</code> {cmd['description']}" for cmd in module['commands']])
            commands_section = self.strings["commands"].format(commands_list=commands_list)

        description_section = ""
        if "description" in module:
            description_section = self.strings["description"].format(description=module["description"])

        author_info = module.get("author", "???")
        module_name = module['name'].replace('.py', '')

        return self.strings["closest_match"].format(
            module_name=module_name,
            author=author_info,
            repo_url=repo_url,
            install_command=f"{self.get_prefix()}{install}",
            description=description_section,
            commands=commands_section
        )

    async def send_result_with_video(self, message, result_text):
        await message.delete()
        if message.chat.permissions and "video" in message.chat.permissions:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/videos.json") as response:
                    if response.status == 200:
                        content = await response.text()
                        try:
                            videos = json.loads(content)
                            video_url = random.choice(videos) if videos else None
                            if video_url:
                                await message.client.send_file(message.to_id, video_url, caption=result_text)
                            else:
                                await utils.answer(message, result_text)
                        except json.JSONDecodeError:
                            await utils.answer(message, result_text)
                    else:
                        await utils.answer(message, result_text)
        else:
            await utils.answer(message, result_text)
            
