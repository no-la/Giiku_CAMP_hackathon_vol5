import argparse

from config import settings
from utils import file_utils, logging_utils


parser = argparse.ArgumentParser(
    description="新しいappを作るときなどに使う"
)

parser.add_argument('--newapp', type=str, help="作りたいappの名前")
args = parser.parse_args()


if __name__ == '__main__':
    if args.newapp is not None:
        """以下のファイルを作る
        
        apps\\NEWAPP.py,
        cogs\\d_NEWAPP.py,
        tests\\test_NEWAPP.py
        """
        pathes = [
            f"{settings.APP_DIR_PATH}{args.newapp}.py",
            f"{settings.COG_DIR_PATH}cogs\\d_{args.newapp}.py",
            f"{settings.TEST_DIR_PATH}test_{args.newapp}.py",
        ]
        # appがまだ存在しないことを確認する
        for p in pathes:
            if file_utils.is_path(p):
                raise FileExistsError(f"既に存在するapp名が渡されました", p)
        
        
        TEMPLETE_DIR_PATH = f"{settings.CONFIG_DIR_PATH}\\templetes\\"
        # apps\\NEWAPP.py
        file_utils.write_file(
            pathes[0],
            file_utils.read_file(
                f"{TEMPLETE_DIR_PATH}app_templete.txt")
            )
        
        # cogs\\d_NEWAPP.py
        file_utils.write_file(
            pathes[1],
            file_utils.read_file(
                f"{TEMPLETE_DIR_PATH}cog_templete.txt"
                ).format(
                    args.newapp,
                    "".join(
                        map(
                            lambda s: s[0].capitalize()+s[1:],
                            args.newapp.split("_")
                            )
                        )
                    )
                )
        
        # tests\\test_NEWAPP.py
        file_utils.write_file(
            pathes[2],
            file_utils.read_file(
                f"{TEMPLETE_DIR_PATH}test_templete.txt").format(
                    args.newapp
                )
            )
                
        # tests\\context.py
        content = f"\nfrom apps import {args.newapp}"
        fp = f"{settings.TEST_DIR_PATH}context.py"
        if content not in file_utils.read_file(fp):
            file_utils.write_file(file_path=fp,
                                  content=content, mode="a")
        
        
        logging_utils.log_list("Created Below Files", pathes)
