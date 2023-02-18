from requests          import post
from capmonster_python import HCaptchaTask
from random            import choice, choices
from os                import system
from colorama          import Fore

system('cls')

class Aura:
    def __init__(self):
        self.created           = 0
        self.errors            = 0
        self.email             = ''.join(choices('abcdefghijklmnopqrstuvwxyz1234567890', k=6)) + "@randommail.com"
        self.name              = ''.join(choices('abcdefghijklmnopqrstuvwxyz1234567890', k=7))
        self.password          = ''.join(choices('abcdefghijklmnopqrstuvwxyz1234567890', k=8))
        self.api_key           = str(input(f"{Fore.CYAN}[{Fore.LIGHTGREEN_EX}+{Fore.CYAN}]{Fore.BLUE} Enter Capmonster Key: {Fore.RESET}"))
        self.amount_to_create  = int(input(f"{Fore.CYAN}[{Fore.LIGHTGREEN_EX}+{Fore.CYAN}]{Fore.BLUE} Amount to Create: {Fore.RESET}"))


    def create(self):
        for _ in range(self.amount_to_create):
            system(f'title Aura gen ^| Created: {self.created}^| Errors: {self.errors}')

            capmonster = HCaptchaTask(self.api_key)
            task_id    = capmonster.create_task("https://signup-api.riotgames.com/v1/accounts", "a010c060-9eb5-498c-a7b9-9204c881f9dc")
            result     = capmonster.join_task_result(task_id)
            captcha    = result.get("gRecaptchaResponse")

            headers = {
                'authority'          : 'signup-api.riotgames.com',
                'accept'             : '*/*',
                'accept-language'    : 'en-US,en;q=0.9,nl-NL;q=0.8,nl;q=0.7',
                'content-type'       : 'application/json',
                'origin'             : 'https://auth.riotgames.com',
                'referer'            : 'https://auth.riotgames.com/',
                'sec-ch-ua'          : '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',   
                'sec-ch-ua-mobile'   : '?0',
                'sec-ch-ua-platform' : '"Windows"',
                'sec-fetch-dest'     : 'empty',
                'sec-fetch-mode'     : 'cors',
                'sec-fetch-site'     : 'same-site',
                'user-agent'         : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like    Gecko)     Chrome/110.0.0.0 Safari/537.36',
            }

            json_data = {
                'tou_agree'        : True,
                'newsletter'       : True,
                'date_of_birth'    : f'1999-04-23',
                'email'            : self.email,
                'username'         : self.name,
                'password'         : f"{self.password}",
                'confirm_password' : f"{self.password}",
                'client_id'        : 'prod-xsso-playvalorant',
                'redirect_uri'     : 'https://xsso.playvalorant.com/redirect',
                'locale'           : 'en',
                'token'            : f'hcaptcha {captcha}'
            }

            response = post('https://signup-api.riotgames.com/v1/accounts', headers=headers, json=json_data)
            if response.status_code == 200:
                self.created += 1
                print(f'{Fore.CYAN}[{Fore.LIGHTGREEN_EX}{self.created}{Fore.CYAN}] {Fore.BLUE}Email: {self.email} Name: {self.name} Password: {self.password} {Fore.RESET}')
                with open('accounts.txt', 'a+') as f:
                    f.write(self.email + ':' + self.name + ':' + self.password + '\n')
            else:
                print(response.json())
                self.errors += 1

Aura().create()