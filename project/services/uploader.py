from fastapi import UploadFile
import aiofiles
import aiofiles.os as aos
import os
import asyncio
import zipfile


def extract_zip(path: str, dest: str):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        for zip_info in zip_ref.infolist():
            if zip_info.is_dir():
                continue

            zip_info.filename = os.path.basename(zip_info.filename)
            zip_ref.extract(zip_info, dest)


class Uploader:
    @staticmethod
    async def upload(file: UploadFile):
        archive_ext = (".zip",)

        if file.filename and file.filename.endswith(archive_ext):
            async with aiofiles.tempfile.TemporaryDirectory() as temp_path:
                archive_path = os.path.join(temp_path, file.filename)

                async with aiofiles.open(archive_path, 'wb') as f:
                    content = await file.read()
                    await f.write(content)

                dest_path = os.path.join(temp_path, "extracted")
                await asyncio.to_thread(extract_zip, path=archive_path, dest=dest_path)

                files_list = [os.path.join(dest_path, f) for f in await aos.listdir(dest_path)]
                return files_list
