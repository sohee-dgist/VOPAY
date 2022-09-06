import discord, asyncio
from discord.ext import commands
from userDB import *

bot = commands.Bot(command_prefix="!", intents= discord.Intents.all())
TOKEN = "MTAxNjY0MTY0NDI5ODI0MDA3MA.GcPkHr.m4bwqcOP3_7CoyTZTvS1G8w4OEOlMmLB_pcOTE"

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready.")

@bot.command()
#안내용 커맨드
async def helppaymon(msg):
    embed=discord.Embed(title=":book: VOPAY 사용안내서", description="보드카페이 봇의 사용 안내서입니다. \n :x: 는 관리자만 사용할 수 있는 커맨드 입니다. 사용 적발시 불이익이 있을 수 있습니다.", color=0x3d56d1)
    embed.add_field(name=":printer: joinvodkapay", value="다음을 누르면 보드카 페이에 가입 신청을 할 수 있습니다. 이미 가입된 회원일 경우 reject 됩니다. \n ", inline=False)
    embed.add_field(name=":x: acceptmember + user", value="회원가입을 허가합니다.", inline=False)
    embed.add_field(name=":pencil2: accountnumber + 은행이름 + 계좌번호", value="다음을 눌러 본인의 계좌번호를 입력할 수 있습니다.", inline=False)
    embed.add_field(name=":hamburger: samefood + 먹은 멤버 수 + 금액", value="돈을 낸 사람이 같은 금액을 내는 음식을 먹을 경우 사용하는 명령어입니다.", inline=False)
    await msg.send(embed=embed)

@bot.command()
#가입용 커맨드입니다.
async def joinvodkapay(msg):
    embed=discord.Embed(title="보드카페이 회원가입 안내", description="회원가입이 승낙되려면 예치금 1만원을 넣어주세요 :money_with_wings:", color=0x3d56d1)
    embed.add_field(name="송금 계좌번호", value="대구은행 1002-459-614260", inline=False)
    embed.add_field(name="이름", value=msg.author.name, inline=False)
    embed.add_field(name="ID", value=msg.author.id, inline=False)
    await msg.send(embed=embed)

@bot.command()
#예치금 넣고 승인해주세요.
async def acceptmember(msg, user: discord.User):
    embed=discord.Embed(title= user.name +" 회원님의 회원가입이 승낙 되셨습니다. :white_check_mark: ", description = "보드카페이 요금은 매월 28일 정산합니다. 정산을 위해 accountnumber 명령어를 사용해서 계좌번호를 등록해 주세요. \n 그 전에 요금을 받으시려면 별도로 관리자에게 연락해주세요", color=0x3d56d1)
    embed.add_field(name= user.name, value= user.id, inline=False)
    await msg.send(embed=embed)

@bot.command()
#계좌번호 등록해주세요.
async def accountnumber(msg, bankname , accnumber):
    embed=discord.Embed(title="계좌번호가 등록 되었습니다.", description="", color=0x3d56d1)
    embed.add_field(name=bankname, value=accnumber, inline=False)
    await msg.send(embed=embed)

@bot.command()
#더치페이 밥 정산하기/ 내는 사람이 해주세요~
async def samefood(msg, member_num , account_num):
    embed=discord.Embed(title="더치페이 밥 정산을 시작합니다.", description="오늘도 :shallow_pan_of_food: 맛있게 드셨나요? \n\n 밥을 드신 분들은 내신 분을 제외하고 60초 안에 밑에 반응을 남겨 주세요.", color=0x3d56d1)
    embed.add_field(name = "먹은 사람 수" , value = member_num , inline=False)
    embed.add_field(name = "1인당 내야할 금액" , value = int(account_num)/int(member_num) , inline=False)
    msg1 = await msg.send(embed=embed)
    human_baneng = 0
    user_arr = []
    await msg1.add_reaction("👍")
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout = 10.0)
        except asyncio.TimeoutError:
            embed=discord.Embed(title="정산에 실패했어요.", description="다시 시도해 주세요.", color=0x3d56d1)
            await msg.send(embed=embed)
            break
        else:
            user_arr.append(user)
            human_baneng += 1
            vartxt = ""
            if(human_baneng==int(member_num)-1):
                embed=discord.Embed(title="정산할까요?", description="잘 읽어보고 확인 후 돈을 내신분이 3분 안에 ✅ 반응을 눌러주세요. 되돌리기 어려워요!", color=0x3d56d1)
                for humans in user_arr:
                    vartxt += "<@"+str(humans.id)+">\n"
                embed.add_field(name = "돈 낸 사람" , value = "<@"+str(msg.author.id)+">" , inline=False)
                embed.add_field(name = "돈 내야할 사람들 목록" , value = vartxt , inline=False)
                msg2 = await msg.send(embed=embed)
                await msg2.add_reaction("✅")
                #나중에 주석으로 슥 수정
                def check(reaction, user):
                    return user == msg.author
                try:
                    reaction, user = await bot.wait_for('reaction_add', timeout = 10.0, check = check)
                except asyncio.TimeoutError:
                    embed=discord.Embed(title="정산에 실패했어요.", description="다시 시도해 주세요.", color=0x3d56d1)
                    await msg.send(embed=embed)
                else:
                    embed=discord.Embed(title="정산에 성공했어요.", description="보드카페이 서버에 반영되었습니다.", color=0x3d56d1)
                    await msg.send(embed=embed)
                break

@bot.command()
#다른음식 밥 정산하기/ 내는 사람이 해주세요~
async def differentfood(msg, member_num):
    embed=discord.Embed(title="더치페이 밥 정산을 시작합니다.", description="오늘도 :shallow_pan_of_food: 맛있게 드셨나요? \n\n 밥을 드신 분들은 내신 분을 제외하고 60초 안에 밑에 반응을 남겨 주세요.", color=0x3d56d1)
    embed.add_field(name = "먹은 사람 수" , value = member_num , inline=False)
    msg1 = await msg.send(embed=embed)
    human_baneng = 0
    user_arr = []
    user_money_arr = []
    await msg1.add_reaction("👍")
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout = 10.0)
        except asyncio.TimeoutError:
            embed=discord.Embed(title="정산에 실패했어요.", description="다시 시도해 주세요. 숫자가 맞지 않네요.", color=0x3d56d1)
            await msg.send(embed=embed)
            break
        else:
            user_arr.append(user)
            human_baneng += 1
            vartxt = ""
            if(human_baneng==int(member_num)-1):
                embed=discord.Embed(title="금액을 설정할께요", description="차례대로 본인이 먹은 음식의 가격을 답변해주세요", color=0x3d56d1)
                await msg.send(embed=embed)
                for i in range (0,human_baneng):
                    embed=discord.Embed(title= "먹은 음식 값을 기록해 주세요", description = "<@" + str(user_arr[i].id) + ">" + "60초 안에 답변을 부탁드립니다.", color=0x3d56d1)
                    await msg.send(embed=embed)
                    msg5 = await bot.wait_for('message', timeout= 10.0)
                    user_money_arr.append(int(msg5.content))
                    vartxt += "<@"+str(user_arr[i].id)+">"+" 님 "+ str(user_money_arr[i]) +"원 \n"
                
                embed=discord.Embed(title="다음이 맞나요?", description="돈을 내신 분이 ✅로 반응해 주세요", color=0x3d56d1)

                embed.add_field(name = "돈 낸 사람 , 금액/ 본인의 것은 제외됩니다." , value = "<@" + str(msg.author.id) + "> 님 " + str(sum(user_money_arr)) + "원" , inline=False)
                embed.add_field(name = "돈 내야할 사람들 목록, 금액" , value = vartxt , inline=False)

                msg2 = await msg.send(embed=embed)
                await msg2.add_reaction("✅")
                #나중에 주석으로 슥 수정
                def check(reaction, user):
                    return user == msg.author
                try:
                    reaction, user = await bot.wait_for('reaction_add', timeout = 10.0, check = check)
                except asyncio.TimeoutError:
                    embed=discord.Embed(title="정산에 실패했어요.", description="다시 시도해 주세요.", color=0x3d56d1)
                    await msg.send(embed=embed)
                else:
                    embed=discord.Embed(title="정산에 성공했어요.", description="보드카페이 서버에 반영되었습니다.", color=0x3d56d1)
                    await msg.send(embed=embed)
                break







bot.run(TOKEN)