from code import interact
import discord, asyncio
from discord.ext import commands
from userDB import *
from discord.ui import Button, View
from discord.utils import get

bot = commands.Bot(command_prefix="!", intents= discord.Intents.all())
TOKEN = "MTAxNjY0MTY0NDI5ODI0MDA3MA.GwkvGM.A86AAV3Rc1AzJXUWPrpHb4ekY_FDSNeFEu2Evw"

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready.")

@bot.command()
async def 보드카페이(ctx):
    button1 = Button(label= "📔 회원가입", style = discord.ButtonStyle.green)
    button2 = Button(label= "🔍 내정보 확인", style = discord.ButtonStyle.green)
    button3 = Button(label= "👨‍👨‍👦‍👦 엔빵", style = discord.ButtonStyle.blurple)
    button4 = Button(label= "😋 각자 다른거 먹기", style = discord.ButtonStyle.blurple)
    button5 = Button(label= "📲 계좌등록", style = discord.ButtonStyle.green)
    button6 = Button(label= "💸 월말정산", style = discord.ButtonStyle.red)
    button7 = Button(label= "📚 장부확인", style = discord.ButtonStyle.url, url = "https://docs.google.com/spreadsheets/d/1LLtLOmhxKLJ2Zn04mnCCDaF9po8Bf5QlPrzmWLbEHSA/edit#gid=0")

    async def button_callback1(interaction):
        await interaction.response.defer()
        check_if = sp_find(ctx.author.id)
        if check_if == False:
            embed=discord.Embed(title="회원가입이 완료되었습니다", description="계좌번호를 등록해주세요", color=0x3d56d1)
            sp_joinup(ctx.author.id)
            await interaction.followup.send(embed=embed, ephemeral = True)
        else:
            embed=discord.Embed(title="회원님은 이미 가입되셨어요", description="문제가 있다면 관리자에게 연락주세요", color=0x3d56d1)
            await interaction.followup.send(embed=embed, ephemeral = True)

    async def button_callback2(interaction):
        await interaction.response.defer()
        myid, mymoney, mybk, myac = sp_find_many(ctx.author.id) 
        if myid == 0:
            embed=discord.Embed(title="회원이 아니시네요", description="회원가입을 먼저 해주세요", color=0x3d56d1)
            await interaction.followup.send(embed=embed, ephemeral = True)
        else:
            embed=discord.Embed(title="📔 회원님의 정보는 다음과 같습니다.", description="ID, 잔액, 정산여부, 계좌번호", color=0x3d56d1)
            embed.add_field(name = "ID" , value = "🤵  " + str(myid) , inline=False)
            embed.add_field(name = "잔액" , value = "🤪  " + str(mymoney) , inline=False)
            if(mybk=="0"):
                embed.add_field(name = "정산여부" , value = "❌  어라😲 저번달에 정산하신 기록이 없어요.", inline=False)
            if(mybk=="1"):
                embed.add_field(name = "정산여부" , value = "⭕ 정산 감사합니다.", inline=False)
            embed.add_field(name = "계좌번호" , value = "📲  "+str(myac) , inline=False)
            await ctx.send(embed=embed)

    async def button_callback3(interaction):
        await interaction.response.defer()
        embed=discord.Embed(title="먹은 사람은 몇명인가요?", description="자신을 포함해서 먹은 사람 수를 입력해 주세요", color=0x3d56d1)
        await ctx.send(embed=embed)
        msg1 = await bot.wait_for('message', timeout= 10.0)
        member_num = msg1.content

        embed=discord.Embed(title="먹은 금액은요?", description="얼마 계산하셨나요?", color=0x3d56d1)
        await ctx.send(embed=embed)
        msg2 = await bot.wait_for('message', timeout= 10.0)
        account_num = msg2.content

        embed=discord.Embed(title="더치페이 밥 정산을 시작합니다.", description="오늘도 :shallow_pan_of_food: 맛있게 드셨나요? \n\n 밥을 드신 분들은 내신 분을 제외하고 60초 안에 밑에 반응을 남겨 주세요.", color=0x3d56d1)
        embed.add_field(name = "먹은 사람 수" , value = member_num , inline=False)
        embed.add_field(name = "1인당 내야할 금액" , value = int(account_num)/int(member_num) , inline=False)
        msg1 = await ctx.send(embed=embed)

        human_baneng = 0
        user_arr = []
        await msg1.add_reaction("👍")
        while True:
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout = 10.0)
            except asyncio.TimeoutError:
                embed=discord.Embed(title="정산에 실패했어요.", description="다시 시도해 주세요.", color=0x3d56d1)
                await ctx.send(embed=embed)
                break
            else:
                user_arr.append(user)
                human_baneng += 1
                vartxt = ""
                if(human_baneng==int(member_num)-1):
                    embed=discord.Embed(title="정산할까요?", description="잘 읽어보고 확인 후 돈을 내신분이 10분 안에 ✅ 반응을 눌러주세요. 되돌리기 어려워요!", color=0x3d56d1)
                    for humans in user_arr:
                        vartxt += "<@"+str(humans.id)+">\n"
                        if sp_find(humans.id)==False:
                            embed=discord.Embed(title="정산에 실패했어요.", description="가입되지 않은 사람이 존재해요." + "<@"+str(ctx.author.id)+">", color=0x3d56d1)
                            await ctx.send(embed=embed)
                            break
                    embed.add_field(name = "돈 낸 사람" , value = "<@"+str(ctx.author.id)+">" , inline=False)
                    embed.add_field(name = "돈 내야할 사람들 목록" , value = vartxt , inline=False)
                    msg2 = await ctx.send(embed=embed)
                    await msg2.add_reaction("✅")
                    #나중에 주석으로 슥 수정
                    def check(reaction, user):
                        return user == ctx.author
                    try:
                        reaction, user = await bot.wait_for('reaction_add', timeout = 10.0, check = check)
                    except asyncio.TimeoutError:
                        embed=discord.Embed(title="정산에 실패했어요.", description="다시 시도해 주세요.", color=0x3d56d1)
                        await ctx.send(embed=embed)
                    else:
                        #돈 update
                        for humans in user_arr:
                            print("업데이트중...")
                            mn_update(humans.id, -int(account_num)/int(member_num))
                        print("낸사람꺼 업데이트중...")
                        mn_update(ctx.author.id, int(account_num)*(int(member_num)-1)/int(member_num))
                        embed=discord.Embed(title="정산에 성공했어요.", description="보드카페이 서버에 반영되었습니다.", color=0x3d56d1)
                        await ctx.send(embed=embed)
                    break

    async def button_callback4(interaction):
        await interaction.response.defer()
        embed=discord.Embed(title="먹은 사람은 몇명인가요?", description="자신을 포함해서 먹은 사람 수를 말해주세요", color=0x3d56d1)
        await ctx.send(embed=embed)
        msg1 = await bot.wait_for('message', timeout= 30.0)
        member_num = msg1.content
        embed=discord.Embed(title="더치페이 밥 정산을 시작합니다.", description="오늘도 :shallow_pan_of_food: 맛있게 드셨나요? \n\n 밥을 드신 분들은 내신 분을 제외하고 10분 안에 밑에 반응을 남겨 주세요.", color=0x3d56d1)
        embed.add_field(name = "먹은 사람 수" , value = member_num , inline=False)
        msg1 = await ctx.send(embed=embed)
        human_baneng = 0
        user_arr = []
        user_money_arr = []
        await msg1.add_reaction("👍")
        while True:
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout = 600.0)
            except asyncio.TimeoutError:
                embed=discord.Embed(title="정산에 실패했어요.", description="다시 시도해 주세요. 숫자가 맞지 않네요.", color=0x3d56d1)
                await ctx.send(embed=embed)
                break
            else:
                user_arr.append(user)
                human_baneng += 1
                vartxt = ""
                if(human_baneng==int(member_num)-1):
                    embed=discord.Embed(title="금액을 설정할께요", description="차례대로 본인이 먹은 음식의 가격을 답변해주세요", color=0x3d56d1)
                    await ctx.send(embed=embed)
                    for i in range (0,human_baneng):

                        if sp_find(user_arr[i].id)==False:
                            embed=discord.Embed(title="정산에 실패했어요.", description="가입되지 않은 사람이 존재해요." + "<@"+str(ctx.author.id)+">", color=0x3d56d1)
                            await ctx.send(embed=embed)
                            break
                        
                        embed=discord.Embed(title= "먹은 음식 값을 기록해 주세요", description = "<@" + str(user_arr[i].id) + ">" + "10분 안에 답변을 부탁드립니다. 타인이 적을 수 있어요.", color=0x3d56d1)
                        await ctx.send(embed=embed)
                        msg5 = await bot.wait_for('message', timeout= 600.0)
                        user_money_arr.append(int(msg5.content))
                        vartxt += "<@"+str(user_arr[i].id)+">"+" 님 "+ str(user_money_arr[i]) +"원 \n"
                    
                    embed=discord.Embed(title="다음이 맞나요?", description="돈을 내신 분이 10분 안에 ✅로 반응해 주세요", color=0x3d56d1)

                    embed.add_field(name = "돈 낸 사람 , 금액/ 본인의 것은 제외됩니다." , value = "<@" + str(ctx.author.id) + "> 님 " + str(sum(user_money_arr)) + "원" , inline=False)
                    embed.add_field(name = "돈 내야할 사람들 목록, 금액" , value = vartxt , inline=False)

                    msg2 = await ctx.send(embed=embed)
                    await msg2.add_reaction("✅")
                    #나중에 주석으로 슥 수정
                    def check(reaction, user):
                        return user == ctx.author
                    try:
                        reaction, user = await bot.wait_for('reaction_add', timeout = 600.0, check = check)
                    except asyncio.TimeoutError:
                        embed=discord.Embed(title="정산에 실패했어요.", description="다시 시도해 주세요.", color=0x3d56d1)
                        await ctx.send(embed=embed)
                    else:

                        
                        for i in range (0,human_baneng):
                            print("업데이트중...")
                            mn_update(user_arr[i].id, -user_money_arr[i])
                        print("낸사람꺼 업데이트중...")
                        mn_update(ctx.author.id, sum(user_money_arr))

                        embed=discord.Embed(title="정산에 성공했어요.", description="보드카페이 서버에 반영되었습니다.", color=0x3d56d1)
                        await ctx.send(embed=embed)
                    break


    async def button_callback5(interaction):
        embed=discord.Embed(title="계좌를 등록해 주세요", description="1분 내에 응답해 주세요", color=0x3d56d1)
        await interaction.response.send_message(embed=embed, ephemeral = True)
        msg1 = await bot.wait_for('message', timeout= 60.0)
        embed=discord.Embed(title="계좌번호가 등록 되었습니다.", description= msg1.content, color=0x3d56d1)
        ac_update(ctx.author.id, msg1.content)
        await interaction.followup.send(embed=embed, ephemeral = True)
    
    async def button_callback6(interaction):
        print("A    ")
        await interaction.response.defer()
        ranks = ranking()
        embed=discord.Embed(title="랭킹을 집계할께요", description="양수는 받아야할 돈입니다. \n 음수는 내야할 돈입니다.", color=0x3d56d1)
        i = 1
        for item in ranks:
            embed.add_field(name= str(i)+"위", value="<@"+str(item[0])+"> 님" + str(item[1]) + "원 입니다.", inline=False)
            i += 1
        await ctx.send(embed=embed)

    button1.callback = button_callback1
    button2.callback = button_callback2
    button3.callback = button_callback3
    button4.callback = button_callback4
    button5.callback = button_callback5
    button6.callback = button_callback6

    view = View(timeout=None)
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)
    view.add_item(button5)
    view.add_item(button6)
    view.add_item(button7)

    await ctx.send(embed = discord.Embed(title='보드카페이를 사용해주셔서 감사합니다',description="원하시는 버튼을 클릭해주세요. \n 보드카페이를 사용하기 전 가입은 필수입니다. \n 가입 후 계좌등록을 사용해 주세요. \n 봇에게 dm을 받을 수 있도록 서버에서 받는 dm 기능을 허용해 주세요. \n", colour=discord.Colour.blue()), view=view)

@bot.command()
#안내용 커맨드
async def helppaymon(msg):
    embed=discord.Embed(title=":book: VOPAY 사용안내서", description="보드카페이 봇의 사용 안내서입니다. \n :x: 는 관리자만 사용할 수 있는 커맨드 입니다. 사용 적발시 불이익이 있을 수 있습니다.", color=0x3d56d1)
    embed.add_field(name=":printer: joinvodkapay", value="다음을 누르면 보드카 페이에 가입 신청을 할 수 있습니다. 이미 가입된 회원일 경우 reject 됩니다. \n ", inline=False)
    embed.add_field(name=":x: acceptmember + user", value="회원가입을 허가합니다.", inline=False)
    embed.add_field(name=":pencil2: accountnumber + 은행이름 + 계좌번호", value="다음을 눌러 본인의 계좌번호를 입력할 수 있습니다.", inline=False)
    embed.add_field(name=":hamburger: samefood + 먹은 멤버 수 + 금액", value="돈을 낸 사람이 같은 금액을 내는 음식을 먹을 경우 사용하는 명령어입니다.", inline=False)
    await msg.send(embed=embed)

bot.run(TOKEN)