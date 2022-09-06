import gspread

def newmember(name, id):
    gc = gspread.service_account(filename="./vodka-payment-bd9e8321f13e.json")
    sh = gc.open("vodkapay").worksheet("시트1")
    
