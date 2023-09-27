import psycopg2
import asyncio
import discord
from discord.ext import commands
from discord_buttons_plugin import  *
from discord import app_commands
from discord.ui import view 
from tokugi import tokugi_list

TOKEN = "TOKEN" #トークン

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
client = commands.Bot(command_prefix = "/",intents=intents,case_insensitive=True)
tree=client.tree

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="記載箇所",style=discord.ButtonStyle.primary) 
    async def page_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        await page_clicked(button)
        return

    @discord.ui.button(label="詳細",style=discord.ButtonStyle.primary)
    async def syosai_button(self, button:discord.ui.Button, interaction:discord.Interaction):
        await syosai_clicked(button)
        return

    @discord.ui.button(label="読み仮名",style=discord.ButtonStyle.primary) 
    async def yomigana_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        await yomigana_clicked(button)
        return

class Buttons_2(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="特技",style=discord.ButtonStyle.primary) 
    async def tokugi_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        await tokugi_clicked(button)
        return 

    @discord.ui.button(label="間合",style=discord.ButtonStyle.primary)
    async def maai_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        await maai_clicked(button)
        return 

    @discord.ui.button(label="コスト",style=discord.ButtonStyle.primary) 
    async def cost_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        await cost_clicked(button)
        return 

class Buttons_3(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="特技から逆引き検索",style=discord.ButtonStyle.primary)
    async def tokugi_another_button(self, button:discord.ui.Button, interaction:discord.Interaction):
        await tokugi_clicked_another(button)
        return 
        
    @discord.ui.button(label="あいまい検索",style=discord.ButtonStyle.primary) 
    async def aimai_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        await aimai_clicked(button)
        return

class Buttons_4(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)


# 記載ページ

async def page_clicked(user):

    def check(m):
        return  m.author.id == user.user.id

    try:
        print(user)
        await user.response.send_message("記載箇所を調べたい忍法名を入力してください。")
        ninpo_name = await client.wait_for('message',check=check,timeout=15)
        ninpo_name = ninpo_name.content
            
    except asyncio.TimeoutError:
        await user.channel.send(f"{user.user.mention}\n申し訳ございません。再度コマンドを実行の上、忍法名を入力してください。")
    else:
        sql = "select supple,page from ninpo where name = '" + ninpo_name.replace("'","") + "';"
        dict_result = sql_connect(sql)

        if not dict_result:
            await user.channel.send(f"{user.user.mention}\n「" + ninpo_name + "」ですが、見つかりませんでした。\n忍法名の記載が正しいか確認してください。")
        else:
            await user.channel.send(f"{user.user.mention}\n「" + ninpo_name + "」は" + dict_result[0][0] + "の" + str(dict_result[0][1]) + "ページに記載されています。")

    return

@tree.command(
    name="page",
    description = '忍法名を入力すると、その忍法が記載されているページを調べます。',
)
@discord.app_commands.describe(
    ninpo_name ="忍法名" # 引数名=説明
)
@discord.app_commands.guild_only
async def page(user, ninpo_name:str):
    sql = "select supple,page from ninpo where name = '" + ninpo_name.replace("'","") + "';"
    dict_result = sql_connect(sql)

    if not dict_result:
        await user.response.send_message("「" + ninpo_name + "」ですが、見つかりませんでした。\n忍法名の記載が正しいか確認してください。",ephemeral=True)

    else:
        await user.response.send_message(ninpo_name + "は" + dict_result[0][0] + "の" + str(dict_result[0][1]) + "ページに記載されています。",ephemeral=True)

    return

# 特技
async def tokugi_clicked(user):

    def check(m):
        return  m.author.id == user.user.id

    try:
        await user.response.send_message("指定特技を調べたい忍法名を入力してください。")
        ninpo_name = await client.wait_for('message',check=check,timeout=15)
        ninpo_name = ninpo_name.content
            
    except asyncio.TimeoutError:
        await user.channel.send(f"{user.user.mention}\n申し訳ございません。再度コマンドを実行の上、忍法名を入力してください。")
    else:
        sql = "select tokugi,type from ninpo where name = '" + ninpo_name.replace("'","") + "' ORDER BY id DESC;"
        dict_result = sql_connect(sql)

        if not dict_result:
            await user.channel.send(f"{user.user.mention}\n「" + ninpo_name + "」ですが、見つかりませんでした。\n忍法名の記載が正しいか確認してください。")
        else:
            if dict_result[0][1] == "装備":
                await user.channel.send(f"{user.user.mention}\n" + ninpo_name + "は装備忍法なので指定特技はありません。")
            else:
                await user.channel.send(f"{user.user.mention}\n" + ninpo_name + "の指定特技は【" + dict_result[0][0] + "】です。")
    return
    
@tree.command(
    name = 'tokugi',
    description = '忍法名を入力すると、その忍法の指定特技を調べます。',
)
@discord.app_commands.describe(
    ninpo_name ="忍法名" # 引数名=説明
)
@discord.app_commands.guild_only
async def tokugi(user,ninpo_name:str):

    sql = "select tokugi,type from ninpo where name = '" + ninpo_name.replace("'","") + "' ORDER BY id DESC;"
    dict_result = sql_connect(sql)

    if not dict_result:
        await user.response.send_message("「" + ninpo_name + "」ですが、見つかりませんでした。\n忍法名の記載が正しいか確認してください。",ephemeral=True)

    else:
        if dict_result[0][1] == "装備":
            await user.response.send_message(ninpo_name + "は装備忍法なので指定特技はありません。",ephemeral=True)
        else:
            await user.response.send_message(ninpo_name + "の指定特技は【" + dict_result[0][0] + "】です。",ephemeral=True)

    return

# 間合い
async def maai_clicked(user):

    def check(m):
        return  m.author.id == user.user.id

    try:
        await user.response.send_message("間合いを調べたい忍法名を入力してください。")
        ninpo_name = await client.wait_for('message',check=check,timeout=15)
        ninpo_name = ninpo_name.content
            
    except asyncio.TimeoutError:
        await user.channel.send(f"{user.user.mention}\n申し訳ございません。再度コマンドを実行の上、忍法名を入力してください。")
    else:
        sql = "select maai,type from ninpo where name = '" + ninpo_name.replace("'","") + "';"
        dict_result = sql_connect(sql)

        if not dict_result:
            await user.channel.send(f"{user.user.mention}\n「" + ninpo_name + "」ですが、見つかりませんでした。\n忍法名の記載が正しいか確認してください。")
        else:
            if dict_result[0][1] == "装備":
                await user.channel.send(f"{user.user.mention}\n" + ninpo_name + "は装備忍法なので間合いはありません。")
            else:
                await user.channel.send(f"{user.user.mention}\n" + ninpo_name + "の間合いは【" + dict_result[0][0] + "】です。")

    return

@tree.command(
    name = 'distance',
    description = '忍法名を入力すると、その忍法の間合いを調べます',
)
@discord.app_commands.describe(
    ninpo_name ="忍法名" # 引数名=説明
)
@discord.app_commands.guild_only
async def distance(user,ninpo_name:str):

    sql = "select maai,type from ninpo where name = '" + ninpo_name.replace("'","") + "';"
    dict_result = sql_connect(sql)

    if not dict_result:
        await user.response.send_message("「" + ninpo_name + "」ですが、見つかりませんでした。\n忍法名の記載が正しいか確認してください。",ephemeral=True)

    else:
        if dict_result[0][1] == "装備":
            await user.response.send_message(ninpo_name + "は装備忍法なので間合いはありません。",ephemeral=True)
        else:
            await user.response.send_message(ninpo_name + "の間合いは【" + dict_result[0][0] + "】です。",ephemeral=True)

    return

# コスト

async def cost_clicked(user):

    def check(m):
        return  m.author.id == user.user.id

    try:
        await user.response.send_message("コストを調べたい忍法名を入力してください。")
        ninpo_name = await client.wait_for('message',check=check,timeout=15)
        ninpo_name = ninpo_name.content
            
    except asyncio.TimeoutError:
        await user.channel.send(f"{user.user.mention}\n申し訳ございません。再度コマンドを実行の上、忍法名を入力してください。")
    else:
        sql = "select cost,type from ninpo where name = '" + ninpo_name.replace("'","") + "';"
        dict_result = sql_connect(sql)

        if not dict_result:
            await user.channel.send(f"{user.user.mention}\n「" + ninpo_name + "」ですが、見つかりませんでした。\n忍法名の記載が正しいか確認してください。")
        else:
            if dict_result[0][1] == "装備":
                await user.channel.send(f"{user.user.mention}\n" + ninpo_name + "は装備忍法なのでコストはありません。")
            else:
                await user.channel.send(f"{user.user.mention}\n" + ninpo_name + "のコストは【" + dict_result[0][0] + "】です。")

    return

@tree.command(
    name = 'cost',
    description = '忍法名を入力すると、その忍法のコストを調べます',
)
@discord.app_commands.describe(
    ninpo_name ="忍法名" # 引数名=説明
)
@discord.app_commands.guild_only
async def cost(user,ninpo_name:str):

    sql = "select cost,type from ninpo where name = '" + ninpo_name.replace("'","") + "';"
    dict_result = sql_connect(sql)

    if not dict_result:
        await user.response.send_message("「" + ninpo_name + "」ですが、見つかりませんでした。\n忍法名の記載が正しいか確認してください。",ephemeral=True)

    else:
        if dict_result[0][1] == "装備":
            await user.response.send_message(ninpo_name + "は装備忍法なのでコストはありません。",ephemeral=True)
        else:
            await user.response.send_message(ninpo_name + "のコストは【" + dict_result[0][0] + "】です。",ephemeral=True)

    return

# 詳細

async def syosai_clicked(user):

    def check(m):
        return  m.author.id == user.user.id

    try:
        await user.response.send_message("詳細を調べたい忍法名を入力してください。")
        ninpo_name = await client.wait_for('message',check=check,timeout=15)
        ninpo_name = ninpo_name.content
            
    except asyncio.TimeoutError:
        await user.channel.send(f"{user.user.mention}\n申し訳ございません。再度コマンドを実行の上、忍法名を入力してください。")
    else:
        sql = "select type,maai,cost,tokugi,supple,page,yomigana,ryuha from ninpo where name = '" + ninpo_name.replace("'","") + "' ORDER BY id DESC;"
        dict_result = sql_connect(sql)

        if not dict_result:
            await user.channel.send(f"{user.user.mention}\n「" + ninpo_name + "」ですが、見つかりませんでした。\n忍法名の記載が正しいか確認してください。")
        else:
            if dict_result[0][0] == "装備":
                await user.channel.send(f"{user.user.mention}\n忍法名："+ninpo_name + "\n流派：" + dict_result[0][7] + "\n分類：" + dict_result[0][0] + "忍法\n記載ページ："+ dict_result[0][4] + str(dict_result[0][5]) + "ページ\n読み方："+ dict_result[0][6])
            else:
                await user.channel.send(f"{user.user.mention}\n忍法名："+ninpo_name + "\n流派:" + dict_result[0][7] + "\n分類：" + dict_result[0][0] + "忍法\n間合い："+ dict_result[0][1]+ "\nコスト：" +dict_result[0][2]+ "\n指定特技："+dict_result[0][3]+ "\n記載ページ："+ dict_result[0][4] + str(dict_result[0][5]) + "ページ\n読み方："+ dict_result[0][6])

    return

@tree.command(
    name = 'detail',
    description = '忍法名を入力すると、その忍法の概要を調べます',
)
@discord.app_commands.describe(
    ninpo_name ="忍法名" # 引数名=説明
)
@discord.app_commands.guild_only
async def detail(user,ninpo_name:str):
    sql = "select type,maai,cost,tokugi,supple,page,yomigana,ryuha from ninpo where name = '" + ninpo_name.replace("'","") + "' ORDER BY id DESC;"
    dict_result = sql_connect(sql)

    if not dict_result:
        await user.response.send_message("「" + ninpo_name + "」ですが、見つかりませんでした。\n忍法名の記載が正しいか確認してください。",ephemeral=True)

    else:
        if dict_result[0][0] == "装備":
            await user.response.send_message("忍法名："+ninpo_name + "\n流派：" + dict_result[0][7] + "\n分類：" + dict_result[0][0] + "忍法\n記載ページ："+ dict_result[0][4] + str(dict_result[0][5]) + "ページ\n読み方："+ dict_result[0][6],ephemeral=True)
        else:
            await user.response.send_message("忍法名："+ninpo_name + "\n流派:" + dict_result[0][7] + "\n分類：" + dict_result[0][0] + "忍法\n間合い："+ dict_result[0][1]+ "\nコスト：" +dict_result[0][2]+ "\n指定特技："+dict_result[0][3]+ "\n記載ページ："+ dict_result[0][4] + str(dict_result[0][5]) + "ページ\n読み方："+ dict_result[0][6],ephemeral=True)

    return

# 読み仮名
@tree.command(
    name = 'yomigana',
    description = 'よみがなを入力すると、その忍法の漢字表記を調べます',
)
@discord.app_commands.describe(
    ninpo_name ="よみがな" # 引数名=説明
)
@discord.app_commands.guild_only
async def yomigana(user,ninpo_name:str):

    sql = "select distinct name from ninpo where yomigana ='" + ninpo_name.replace("'","") + "';"
    dict_result = sql_connect(sql)

    if not dict_result:
        await user.response.send_message("「" + ninpo_name + "」ですが、見つかりませんでした。\n読み仮名が正しいか確認してください。",ephemeral=True)

    else:
        m = ""
        for i in range(len(dict_result)):
            m = m +"「" +  dict_result[i][0] + "」"

        await user.response.send_message("「" + ninpo_name + "」と読む忍法としては" + m + "があります。",ephemeral=True)

    return


async def yomigana_clicked(user): # clickイベントに改変予定

    def check(m):
        return  m.author.id == user.user.id

    try:
        await user.response.send_message("漢字を調べたい忍法名の読み仮名を入力してください。")
        ninpo_name = await client.wait_for('message',check=check,timeout=15)
        ninpo_name = ninpo_name.content
            
    except asyncio.TimeoutError:
        await user.channel.send(f"{user.user.mention}\n申し訳ございません。再度コマンドを実行の上、読み仮名を入力してください。")
    else:
        sql = "select distinct name from ninpo where yomigana = '" + ninpo_name.replace("'","") + "';"
        dict_result = sql_connect(sql)

        if not dict_result:
            await user.channel.send(f"{user.user.mention}\n「" + ninpo_name + "」ですが、見つかりませんでした。\n読み仮名が正しいか確認してください。")
        else:
            m = ""
            for i in range(len(dict_result)):
                m = m +"「" +  dict_result[i][0] + "」"

            await user.channel.send(f"{user.user.mention}\n「" + ninpo_name + "」と読む忍法としては" + m + "があります。")

    return

async def aimai_clicked(user): # あいまい検索

    def check(m):
        return  m.author.id == user.user.id

    try:
        await user.response.send_message("どのような文字が入った忍法を探しますか？")
        ninpo_name = await client.wait_for('message',check=check,timeout=15)
        ninpo_name = ninpo_name.content
            
    except asyncio.TimeoutError:
        await user.channel.send(f"{user.user.mention}\n申し訳ございません。再度コマンドを実行の上、読み仮名を入力してください。")
    else:
        sql = "select distinct name from ninpo where yomigana LIKE '%" + ninpo_name.replace("'","") + "%' OR name LIKE '%" + ninpo_name.replace("'","") + "%';"
        dict_result = sql_connect(sql)

        if not dict_result:
            await user.channel.send(f"{user.user.mention}\n「" + ninpo_name + "」が含まれる忍法ですが、見つかりませんでした。")
        else:
            m = ""
            for i in range(len(dict_result)):
                m = m +"「" +  dict_result[i][0] + "」"

            await user.channel.send(f"{user.user.mention}\n「" + ninpo_name + "」を忍法名もしくは読み仮名に含む忍法は" + m + "があります。")

    return

@tree.command(
    name = 'aimai',
    description = '漢字もしくはよみがなを入力すると、その文字が入った忍法を探します',
)
@discord.app_commands.describe(
    ninpo_name ="検索文字" # 引数名=説明
)
@discord.app_commands.guild_only
async def aimai(user,ninpo_name:str):

    sql = "select distinct name from ninpo where yomigana LIKE '%" + ninpo_name.replace("'","") + "%' OR name LIKE '%" + ninpo_name.replace("'","") + "%';"
    dict_result = sql_connect(sql)

    if not dict_result:
        await user.response.send_message("「" + ninpo_name + "」を含む忍法ですが、見つかりませんでした。",ephemeral=True)

    else:
        m = ""
        for i in range(len(dict_result)):
            m = m +"「" +  dict_result[i][0] + "」"

        await user.response.send_message("「" + ninpo_name + "」と読む忍法としては" + m + "があります。",ephemeral=True)

    return

def sql_connect(sql):

    with psycopg2.connect('postgresql://{user}:{password}@{host}:{port}/{dbname}'.format( 
                    user="postgres",        #ユーザ
                    password="password",  #パスワード
                    host="localhost",       #ホスト名
                    port="1234",            #ポート
                    dbname="DB"))  as conn:
        with conn.cursor() as cur:
            cur.execute(sql)  # クエリの実行
            result = cur.fetchall()

    return result

async def kensaku_button(message):
    
    view=Buttons()
    view_2 = Buttons_2()
    view_3 = Buttons_3()
    view_4 = Buttons_4()
    view_4.add_item(discord.ui.Button(label="シノビガミサポートページ",style=discord.ButtonStyle.link,url="https://bouken.jp/pd/sg/support.html"))
    await message.channel.send(view=view)
    await message.channel.send(view=view_2)
    await message.channel.send(view=view_3)
    await message.channel.send(view=view_4)

    return

@tree.command(
    name = 'hotline',
    description = '容易に検索できるボタンを表示します。',
)
@discord.app_commands.guild_only
async def hotline(message):
    await message.response.send_message("検索方式を選んでください。")
    await kensaku_button(message)

@client.event
async def on_message(message):

    if message.author.bot:
        return
    else:
        if message.content =="hotline" or message.content == "ホットライン":
            await message.channel.send("検索方式を選んでください。")
            await kensaku_button(message)

@client.event
async def on_ready():
    await tree.sync()
    print("ready")

client.run(TOKEN)
