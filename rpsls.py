"""
第一个小项目：Rock-paper-scissors-lizard-Spock
作者：朱渝
日期：2020/11/18
"""
import random
def name_to_number(name):
    if name=="石头":
        num=0
    if name=="史波克":
        num=1
    if name=="布":
        num=2
    if name=="蜥蜴":
        num=3
    if name=="剪刀":
        num=4
    return num
def number_to_name(number):
    if number==0:
        Name="石头"
    if number==1:
        Name="史波克"
    if number==2:
        Name="布"
    if number==3:
        Name="蜥蜴"
    if number==4:
        Name="剪刀"
    return Name
def rpsls(player_choice):
    print("----------------")
    print("您的选择为："+player_choice)
    player_choice_number=name_to_number(player_choice)
    comp_number=random.randrange(0,5)
    comp_name=number_to_name(comp_number)
    print("计算机的选择为："+comp_name)
    if player_choice_number==0and(comp_number==(3 or 4)):
        print("您赢了")
    elif player_choice_number==1and(comp_number==(0 or 4)):
        print("您赢了")
    elif player_choice_number==2and(comp_number==(0 or 1)):
        print("您赢了")
    elif player_choice_number==3and(comp_number==(1 or 2)):
        print("您赢了")
    elif player_choice_number==4and(comp_number==(2 or 3)):
        print("您赢了")
    elif player_choice_number== comp_number:
        print("您和计算机出的一样呢")
    else:
        print("计算机赢了")

print("欢迎使用RPSLS游戏")
print("----------------")
print("请输入您的选择:")
choice_name=input()
if choice_name!=("石头" or "剪刀" or "蜥蜴" or "布" or "史波克"):
    print("Error: No Correct Name.")
else:
    rpsls(choice_name)






