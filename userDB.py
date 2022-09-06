import gspread

def newmember(name, id):
    gc = gspread.service_account(filename="./vodka-payment-bd9e8321f13e.json")
    sh = gc.open("vodkapay").worksheet("시트1")

def sp_joinup(id):
    #회원가입한 회원 추가
    gc = gspread.service_account(filename="./vodka-payment-bd9e8321f13e.json")
    sh = gc.open("vodkapay").worksheet("시트1")
    i = 1
    while True:
        id_box = "A"+str(i)
        as_box = "B"+str(i)
        bk_box = "C"+str(i)
        ac_box = "D"+str(i)
        sp_id = sh.get(id_box)
        if len(sp_id) == 0:
            sh.update_acell(id_box, str(id))
            sh.update_acell(as_box, "0")
            sh.update_acell(bk_box, "0")
            sh.update_acell(ac_box, "0")
            break
        else:
            i += 1

def sp_find(id):
    #회원 찾기
    gc = gspread.service_account(filename="./vodka-payment-bd9e8321f13e.json")
    sh = gc.open("vodkapay").worksheet("시트1")
    i = 1
    while True:
        id_box = "A"+str(i)
        sp_id = sh.get(id_box)
        #print(sp_id)
        if len(sp_id) == 0:
            return False
        if sp_id[0][0] == str(id):
            return True
        else:
            i += 1

def sp_find_many(id):
    #회원 찾기/정보 return
    gc = gspread.service_account(filename="./vodka-payment-bd9e8321f13e.json")
    sh = gc.open("vodkapay").worksheet("시트1")
    i = 1
    while True:
        id_box = "A"+str(i)
        as_box = "B"+str(i)
        bk_box = "C"+str(i)
        ac_box = "D"+str(i)
        sp_id = sh.get(id_box)
        #print(sp_id)
        if len(sp_id) == 0:
            return 0, 0, 0
        if sp_id[0][0] == str(id):
            return sh.get(id_box)[0][0], sh.get(as_box)[0][0], sh.get(bk_box)[0][0], sh.get(ac_box)[0][0]
        else:
            i += 1

def ac_update(id,acc):
    #계좌번호 업데이트
    gc = gspread.service_account(filename="./vodka-payment-bd9e8321f13e.json")
    sh = gc.open("vodkapay").worksheet("시트1")
    i = 1
    while True:
        id_box = "A"+str(i)
        as_box = "B"+str(i)
        bk_box = "C"+str(i)
        ac_box = "D"+str(i)
        sp_id = sh.get(id_box)
        #print(sp_id)
        if sp_id[0][0] == str(id):
            return sh.update_acell(ac_box, acc)
        else:
            i += 1

def mn_update(id,v_money):
    #돈 업데이트
    gc = gspread.service_account(filename="./vodka-payment-bd9e8321f13e.json")
    sh = gc.open("vodkapay").worksheet("시트1")
    i = 1
    while True:
        id_box = "A"+str(i)
        as_box = "B"+str(i)
        bk_box = "C"+str(i)
        ac_box = "D"+str(i)
        sp_id = sh.get(id_box)
        #print(sp_id)
        if sp_id[0][0] == str(id):
            sp_mn = sh.get(as_box)
            n_money = int(sp_mn[0][0])+v_money
            print(sp_mn[0][0])
            print(str(v_money))
            print(str(n_money))
            sh.update_acell(as_box, str(n_money))
            print(sh.get(as_box)[0][0])
            return True
        else:
            if sp_id[0][0] == str(id):
                return False
            i += 1

def ranking():
    #돈 업데이트
    gc = gspread.service_account(filename="./vodka-payment-bd9e8321f13e.json")
    sh = gc.open("vodkapay").worksheet("시트1")
    i = 2
    ranklist = []
    while True:
        print(i)
        id_box = "A"+str(i)
        as_box = "B"+str(i)
        sp_id = sh.get(id_box)
        #print(sp_id)
        if len(sp_id)>0:
            sp_mn = sh.get(as_box)
            u_money = int(sp_mn[0][0])
            u_id = int(sp_id[0][0])
            ranklist.append([u_id,u_money])
        else:
            break
        i += 1
    ranklist.sort(key=lambda x:x[1])
    return ranklist