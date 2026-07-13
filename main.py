import os
import sys
import asyncio
import discord
from discord.ext import commands
from colorama import Fore, Style, init


init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    banner = f"""
{Fore.CYAN}==================================================================
{Fore.MAGENTA}  _____ _      ____  _   _ ______ _____  
{Fore.MAGENTA} / ____| |    / __ \| \ | |  ____|  __ \ 
{Fore.MAGENTA}| |    | |   | |  | |  \| | |__  | |__) |
{Fore.MAGENTA}| |    | |   | |  | | . ` |  __| |  _  / 
{Fore.MAGENTA}| |____| |___| |__| | |\  | |____| | \ \ 
{Fore.MAGENTA} \_____|______\____/|_| \_|______|_|  \_\
                                         
{Fore.BLUE}          >> DISCORD SERVER CLONER v1.0 <<
{Fore.CYAN}==================================================================
{Fore.GREEN}[1] Bot Token ile Giriş Yap (Güvenli)
{Fore.YELLOW}[2] User Token (Selfbot) ile Giriş Yap (Riskli!)
{Fore.RED}[3] Çıkış
{Fore.CYAN}==================================================================
{Fore.LIGHTBLACK_EX}Enes tarafından yapılmıştır.
{Fore.CYAN}==================================================================
"""
    print(banner)

async def clone_server(client, source_id, target_id):
    try:
        source_guild = client.get_guild(source_id) or await client.fetch_guild(source_id)
        target_guild = client.get_guild(target_id) or await client.fetch_guild(target_id)
    except Exception as e:
        print(f"\n{Fore.RED}[!] Sunuculara erişilirken hata oluştu: {e}")
        return

    if not source_guild or not target_guild:
        print(f"\n{Fore.RED}[!] Belirtilen ID'lere sahip sunucular bulunamadı!")
        return

    print(f"\n{Fore.YELLOW}[*] Klonlama işlemi başlatılıyor...")
    print(f"{Fore.BLUE}[*] Kaynak Sunucu: {source_guild.name}")
    print(f"{Fore.BLUE}[*] Hedef Sunucu: {target_guild.name}")

    print(f"\n{Fore.MAGENTA}[*] Hedef sunucudaki eski kanallar temizleniyor...")
    for channel in target_guild.channels:
        try:
            await channel.delete()
            print(f"{Fore.RED}[-] Silindi: {channel.name}")
            await asyncio.sleep(0.5)
        except:
            pass

    print(f"\n{Fore.MAGENTA}[*] Roller kopyalanıyor...")
   
    for role in reversed(source_guild.roles):
        if role.is_default():
            continue
        try:
            await target_guild.create_role(
                name=role.name,
                permissions=role.permissions,
                color=role.color,
                hoist=role.hoist,
                mentionable=role.mentionable
            )
            print(f"{Fore.GREEN}[+] Rol Oluşturuldu: {role.name}")
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"{Fore.RED}[!] Rol oluşturulamadı ({role.name}): {e}")

    print(f"\n{Fore.MAGENTA}[*] Kategoriler ve Kanallar kopyalanıyor...")
    for category in source_guild.categories:
        try:
            new_category = await target_guild.create_category(name=category.name)
            print(f"{Fore.GREEN}[+] Kategori Oluşturuldu: {category.name}")
            
            for channel in category.channels:
                if isinstance(channel, discord.TextChannel):
                    await target_guild.create_text_channel(
                        name=channel.name,
                        category=new_category,
                        topic=channel.topic,
                        nsfw=channel.nsfw,
                        slowmode_delay=channel.slowmode_delay
                    )
                    print(f"{Fore.GREEN}[+] Metin Kanalı Oluşturuldu: #{channel.name}")
                elif isinstance(channel, discord.VoiceChannel):
                    await target_guild.create_voice_channel(
                        name=channel.name,
                        category=new_category,
                        user_limit=channel.user_limit,
                        bitrate=min(channel.bitrate, 96000) 
                    )
                    print(f"{Fore.GREEN}[+] Ses Kanalı Oluşturuldu: 🔊 {channel.name}")
                await asyncio.sleep(0.8)
        except Exception as e:
            print(f"{Fore.RED}[!] Kategori/Kanal oluşturulamadı ({category.name}): {e}")

    for channel in source_guild.channels:
        if channel.category is None:
            try:
                if isinstance(channel, discord.TextChannel):
                    await target_guild.create_text_channel(name=channel.name)
                    print(f"{Fore.GREEN}[+] Kanal Oluşturuldu (Kategorisiz): #{channel.name}")
                elif isinstance(channel, discord.VoiceChannel):
                    await target_guild.create_voice_channel(name=channel.name)
                    print(f"{Fore.GREEN}[+] Ses Kanalı Oluşturuldu (Kategorisiz): 🔊 {channel.name}")
                await asyncio.sleep(0.8)
            except:
                pass

    print(f"\n{Fore.GREEN}[✓] Klonlama işlemi başarıyla tamamlandı!")
    print(f"{Fore.LIGHTBLACK_EX}Enes tarafından yapılmıştır. Programdan çıkmak için CMD'yi kapatabilirsiniz.")

def start_bot(token, is_user_token):
    intents = discord.Intents.all()
    
    if is_user_token:
        client = commands.Bot(command_prefix=".", self_bot=True, intents=intents)
    else:
        client = commands.Bot(command_prefix=".", intents=intents)

    @client.event
    async def on_ready():
        print(f"\n{Fore.GREEN}[+] {client.user} olarak giriş yapıldı!")
        try:
            source_id = int(input(f"{Fore.YELLOW}[?] Kaynak Sunucu ID (Kopyalanacak): "))
            target_id = int(input(f"{Fore.YELLOW}[?] Hedef Sunucu ID (Yapıştırılacak): "))
            await clone_screen_process(client, source_id, target_id)
        except ValueError:
            print(f"{Fore.RED}[!] Lütfen geçerli bir sayısal ID girin.")
            await client.close()

    async def clone_screen_process(client, source_id, target_id):
        await clone_server(client, source_id, target_id)
        await client.close()

    try:
        client.run(token, bot=not is_user_token)
    except Exception as e:
        print(f"\n{Fore.RED}[!] Giriş başarısız! Token hatalı olabilir veya rate limit yemiş olabilirsiniz.\nHata: {e}")
        input("\nDevam etmek için ENTER tuşuna basın...")

def main():
    while True:
        print_banner()
        secim = input(f"{Fore.CYAN}[?] Seçiminiz: ")
        
        if secim == "1":
            token = input(f"\n{Fore.YELLOW}[?] Bot Tokeninizi Girin: ").strip()
            if token:
                start_bot(token, is_user_token=False)
        elif secim == "2":
            token = input(f"\n{Fore.RED}[?] User (Hesap) Tokeninizi Girin: ").strip()
            if token:
                start_bot(token, is_user_token=True)
        elif secim == "3":
            print(f"\n{Fore.GREEN}Görüşmek üzere!")
            sys.exit()
        else:
            print(f"\n{Fore.RED}[!] Geçersiz seçim!")
            asyncio.sleep(1)

if __name__ == "__main__":
    main()
