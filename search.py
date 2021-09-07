import requests
from urllib import request
from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from PIL import Image
import pickle
import os


global imagephoto,imagephoto2
global txt_detalie, client_secret, HEADERS, origin, data_location, image_location
global stathash


stathash = []

data_location = './data/'
image_location = './image/'

client_secret = "428d72e8d59140d89a4d9e4ee234e10f"
HEADERS = {"X-API-Key": client_secret}
origin = 'https://www.bungie.net'

#폴더랑 기본파일 확인용, ddd.json 확인....

root = Tk()
root.title("데스티니 2")
root.geometry("500x500+100+100")
#프레임/윈도우/창 크기 조절 허용 여부
root.resizable(False, True)
root.iconbitmap(data_location+"destiny-2.ico")

def btndef():
    global names
    print(entr1.get())
    names = findhash()

    #txt_detalie.insert(END,find_hash)
    #name.clear()
    return

def findhash():
    gettxt = entr1.get()
    list1.delete(0,END)
    ss = '/Platform/Destiny2/Armory/Search/DestinyInventoryItemDefinition/'+gettxt+'?lc=ko'
    r = requests.get(origin + ss, headers=HEADERS);
    print(r.json())
    touch = r.json()

    with open('./data/touch.pickle','wb') as fw:
        pickle.dump(touch, fw)

    totalResult = touch.get("Response").get("results").get("totalResults")
    name = [0] * totalResult
    for i in range(totalResult):
        name[i] = touch.get("Response").get("results").get("results")[i].get("displayProperties").get("name")
    print(name)

    #리스트 목록에 검색된 것들
    for ii in range(totalResult):
        list1.insert(ii,name[ii])
    return name

def findinformation():
    global anchor_str, item_response, getyou_num,item_response_eng
    label2.delete("1.0", "end")
    #선택된 리스트의 이름을 가져온다...인데 이름말고 순서를 들고 와야함
    anchor_str = list1.get(ANCHOR)
    #튜플 형태로 선택된 위치를 준다. [0]사용으로 번호 뽑기
    in_to = list1.curselection()

    print(anchor_str)
    with open('./data/touch.pickle','rb') as f:
        data = pickle.load(f)

    getyou_num = data.get("Response").get("results").get("results")[in_to[0]].get("hash")
    print(getyou_num)
    item_response = Checking_file_DestinyInventoryItemDefinition(getyou_num)
    item_response_eng = Checking_file_DestinyInventoryItemDefinition_eng(getyou_num)
    print(item_response)
    print(item_response_eng)
    image_upload = item_response.get("Response").get("displayProperties").get("icon")
    phtoimage_down(image_upload)
    image_screenshot = item_response.get("Response").get("screenshot")
    screenshot_image_down(image_screenshot)
    phtoimage_setup()
    More_information()
    item_display_tierTypeName = item_response.get("Response").get("inventory").get("tierTypeName")
    socketEntries_Legendary()

def item_stats_search(stats_hash):
    lili = []

    telme = {"3555269338":"확대/축소",
             "2961396640":"충전 시간",
             "4043523819":"충격",
             "1240592695":"사거리",
             "155624089":"안정성",
             "3871231066":"탄창",
             "4188031367":"재장전 속도",
             "1931675084": "소지품 크기",
             "943549884": "조작성",
             "1345609583": "조준 지원",
             "2715839340": "반동 방향",
             "4284893193": "분당 발사 수",
             "1591432999": "정확도",
             "447667954": "발사 시간",
             "3614673599": "폭발 반경",
             "2523465841": "투사체 속도",
             "2837207746": "스윙 속도",
             "3022301683": "충전 속도",
             "925767036": "탄약 수용량",
             "209426660": "막기 저항",
             }
    for A in range(len(stats_hash)):
        try:
            lili.append(telme[stats_hash[A]])
            lili.append(item_response.get("Response").get("stats").get("stats").get(stats_hash[A]).get("value"))
        except:
            pass

    return lili

def More_information():
    global item_display_name, item_stats, item_display_tierTypeName, item_flavorText, item_display_typename, collection_data,item_display_name_eng
    paste = []
    item_display_name = item_response.get("Response").get("displayProperties").get("name")
    item_display_name_eng = item_response_eng.get("Response").get("displayProperties").get("name")
    item_display_tierTypeName = item_response.get("Response").get("inventory").get("tierTypeName")
    item_display_typename = item_response.get("Response").get("itemTypeDisplayName")
    item_flavorText = item_response.get("Response").get("flavorText")
    stathash = list(item_response.get("Response").get("stats").get("stats").keys())
    item_stats = item_stats_search(stathash)

    tiertyprhash = item_response.get("Response").get("inventory").get("tierTypeHash")

    collectibleHash = item_response.get("Response").get("collectibleHash")
    #콜렉션 정보를 다운받는 구간
    collection_data = Checkinig_file_DestinyCollectibleDefinition(collectibleHash)

    paste.extend([item_display_name,item_display_tierTypeName,item_display_typename,item_flavorText])

    label2.insert(1.0, "\n".join(paste))
    AA1 = 0
    AA2 = 1
    label2.insert(END, "\n")
    for A2 in range(len(item_stats)):
        try:
            label2.insert(END, item_stats[AA1]+str(item_stats[AA2]))
            label2.insert(END, "\n")
            AA1 += 2
            AA2 += 2
        except:
            pass

def phtoimage_down(urldown):
    #os.system("curl " + origin +urldown + " > "+data_location+"icons2.jpg")
    if not os.path.isfile("./image/"+anchor_str+'.jpg'):
        request.urlretrieve(origin+urldown,image_location+anchor_str+'.jpg')
        print("phtoimage 다운 완료")
    return
def screenshot_image_down(urldown):
    #os.system("curl " + origin +urldown + " > "+data_location+"icons2.jpg")
    if not os.path.isfile("./image/"+anchor_str+'_screenshot.jpg'):
        request.urlretrieve(origin+urldown,image_location+anchor_str+'_screenshot.jpg')
        print("screenshot 다운 완료")
    return


def jsondata_down(touch,name):
    with open('./data/'+ str(name) +'.pickle', 'wb') as Handle:
        pickle.dump(touch,Handle, protocol=pickle.HIGHEST_PROTOCOL)

def jsondata_open(name):
    with open('./data/'+ str(name) +'.pickle','rb') as Handle:
        data = pickle.load(Handle)
    return data

def phtoimage_setup():
    image_change = ImageTk.PhotoImage(Image.open(image_location+anchor_str+".jpg"))
    label1.config(image=image_change)
    label1.image = image_change

def Checking_file_DestinyPlugSetDefinition(rprint):
    #랜덤 소켓의 정보를 가져오는 함수, 해당 파일의 체크와 불러오기 담당
    if not os.path.isfile("./data/" + str(rprint) + ".pickle"):
        ss = "/Platform/Destiny2/Manifest/DestinyPlugSetDefinition/"+str(rprint)+"/"
        r = requests.get(origin + ss, headers=HEADERS);
        reusablePlugItems = r.json()
        jsondata_down(reusablePlugItems,rprint)
    else :
        reusablePlugItems  = jsondata_open(rprint)
    return reusablePlugItems

def Checking_file_DestinyInventoryItemDefinition(getyou_hash):
    #퍽의 자세한 정보를 들고오는 함수...
    if not os.path.isfile("./data/" + str(getyou_hash) + ".pickle"):
        ss = '/Platform/Destiny2/Manifest/DestinyInventoryItemDefinition/' + str(getyou_hash) + '?lc=ko'
        r = requests.get(origin + ss, headers=HEADERS);
        displayProperties = r.json()
        jsondata_down(displayProperties, getyou_hash)
    else:
        displayProperties = jsondata_open(getyou_hash)
    return displayProperties

def Checking_file_DestinyInventoryItemDefinition_eng(getyou_hash):
    #퍽의 자세한 정보를 들고오는 함수...
    str_plus = str(getyou_hash)+'eng'
    if not os.path.isfile("./data/" + str(getyou_hash) + "eng.pickle"):
        ss = '/Platform/Destiny2/Manifest/DestinyInventoryItemDefinition/' + str(getyou_hash)
        r = requests.get(origin + ss, headers=HEADERS);
        displayProperties = r.json()
        jsondata_down(displayProperties, str_plus)
    else:
        displayProperties = jsondata_open(str_plus)
    return displayProperties

def Checkinig_file_DestinyStatDefinition(stathash):
    for i in range(len(stathash)):
        rprint = item_response.get("Response").get("stats").get("stats").get(stathash[i]).get("value")
        if not os.path.isfile("./data/" + str(stathash[i]) + ".pickle"):
            ss = "/Platform/Destiny2/Manifest/DestinyStatDefinition/" + str(stathash[i]) + "?lc=ko"
            r = requests.get(origin + ss, headers=HEADERS);
            weapon_stat_data = r.json()
            jsondata_down(weapon_stat_data,stathash[i])
        else:
            weapon_stat_data = jsondata_open(stathash[i])
    return weapon_stat_data

def Checkinig_file_DestinyCollectibleDefinition(getyou_hash):
    # 퍽의 자세한 정보를 들고오는 함수...
    if not os.path.isfile("./data/" + str(getyou_hash) + ".pickle"):
        ss = '/Platform/Destiny2/Manifest/DestinyCollectibleDefinition/' + str(getyou_hash) + '?lc=ko'
        r = requests.get(origin + ss, headers=HEADERS);
        displayProperties = r.json()
        jsondata_down(displayProperties, getyou_hash)
    else:
        displayProperties = jsondata_open(getyou_hash)
    return displayProperties

def elemental(select_elemental):
    print(select_elemental)
    if select_elemental == '3373582085':
        selecting = 'destiny_element_kinetic.png' #물리 속성
    elif select_elemental == '1847026933':
        selecting = 'destiny_element_thermal.png' #태양 속성
    elif select_elemental == '2303181850':
        selecting = 'destiny_element_arc.png' #전기 속성
    elif select_elemental == '3454344768':
        selecting = 'destiny_element_void.png' #공허 속성
    elif select_elemental == '151347233':
        selecting = 'DestinyDamageTypeDefinition_530c4c3e7981dc2aefd24fd3293482bf.png' #시공 속성
    else:
        selecting = 'error'

    return selecting

def ammunition(select_ammunition):
    if select_ammunition == '1':
        selecting = 'destiny_ammunition_primary.png' #흰탄
    elif select_ammunition == '2':
        selecting = 'destiny_ammunition_special.png' #특탄
    elif select_ammunition == '3':
        selecting = 'destiny_ammunition_heavy.png' #중탄
    else:
        selecting = 'error'
    return selecting

def Type_data(item_type_data):
    global namu_stat_list
    namu_stat_list = []
    namu_stat_list.clear()
    if item_type_data == '자동 소총' or item_type_data =='기관단총' or item_type_data =='정찰 소총' or item_type_data =='파동 소총' or item_type_data =='보조 무기' or item_type_data =='핸드 캐논' or item_type_data =='저격총' or item_type_data =='산탄총' or item_type_data =='추적 소총':
        selecting = 's1=충격, s2=사거리, s3=안정성, s4=조작성, s5=재장전 속도, s6=분당 발사 수, s7=탄창'#기본
        namu_stat_list = ['충격','사거리','안정성','조작성','재장전 속도','분당 발사 수','탄창']
    elif item_type_data == '유탄 발사기' or item_type_data =='로켓 발사기':
        selecting = 's1=폭발 반경, s2=투사체 속도, s3=안정성, s4=조작성, s5=재장전 속도, s6=분당 발사 수, s7=탄창'#유탄, 로케쇼
        namu_stat_list = ['폭발 반경', '투사체 속도', '안정성', '조작성', '재장전 속도', '분당 발사 수', '탄창']
    elif item_type_data == '전투 활':
        selecting = 's1=충격, s2=정확도, s3=안정성, s4=조작성, s5=재장전 속도, s6=충전 시간, s7=발사 시간'#활
        namu_stat_list = ['충격', '정확도', '안정성', '조작성', '재장전 속도', '충전 시간', '발사 시간']
    elif item_type_data == '융합 소총' or item_type_data =='선형 융합 소총':
        selecting = 's1=충격, s2=사거리, s3=안정성, s4=조작성, s5=재장전 속도, s6=충전 시간, s7=탄창'#융합
        namu_stat_list = ['충격', '사거리', '안정성', '조작성', '재장전 속도', '충전 시간', '탄창']
    elif item_type_data == '검':
        selecting = 's1=충격, s2=스윙 속도, s3=충전 속도, s4=막기 저항, s5=막기 효율, s6=막기 지속, s7=탄약 수용량, s8=충전 시간'#검
        namu_stat_list = ['충격', '스윙 속도', '충전 속도', '탄약 수용량']
    return selecting

def stat_image_namu(socket_data):
    list_example = []
    for i in range(len(socket_data)):
        list_example.append('[[파일:데스티니가디언즈_'+socket_data[i].replace(' ','')+'.png|width=40px]][br]{{{#FFF '+socket_data[i]+'}}}')
    return list_example

def stat_image_random_namu(socket_dat):
    text1.insert(END, '\n')
    make_text = '||'+stat_option + socket_dat[0] + ' ||'
    text1.insert(END, make_text)
    for y in range(len(socket_dat)):
        yy = y+1
        if yy == len(socket_dat)-1 :
            break
        text1.insert(END, '\n')
        text1.insert(END, '|| '+socket_dat[yy]+' ||')
    text1.insert(END, '\n')
    make_text = '|| ' + socket_dat[len(socket_dat)-1].replace("\n","") + ' ||' + stat_option3
    text1.insert(END, make_text)

def make_dim_wishlist():
    global stat_option, stat_option3, stat_option2
    text1.delete("1.0", "end")
    fdata_scope = scope_socket_data[0]
    fdata_magazine = magazine_socket_data[0]
    fdata_trait1 = trait1_socket_data[0]
    fdata_trait2 = trait2_socket_data[0]

    item_element = elemental(str(item_response.get('Response').get('defaultDamageTypeHash')))
    item_ammunition = ammunition(str(item_response.get('Response').get('equippingBlock').get('ammoType')))
    item_collection = collection_data.get('Response').get('sourceString')

    item_type = Type_data(str(item_display_typename))
    try:
        v1 = item_stats.index(namu_stat_list[0]) + 1
        v2 = item_stats.index(namu_stat_list[1]) + 1
        v3 = item_stats.index(namu_stat_list[2]) + 1
        v4 = item_stats.index(namu_stat_list[3]) + 1
        v5 = item_stats.index(namu_stat_list[4]) + 1
        v6 = item_stats.index(namu_stat_list[5]) + 1
        v7 = item_stats.index(namu_stat_list[6]) + 1
    except:
        v5 = 0
        v6 = 0
        v7 = 0

    namu1 = "||<table width=400px><table bgcolor=#222><-2><(>{{{#FFF '''{{{+1 "+ item_display_name +"}}},,,("+item_display_name_eng+"),,,'''[br]"+ item_display_typename +"}}}[br]{{{-2 {{{#DDD "+item_flavorText+"}}}}}}||"
    namu2 = "||<width=50%><)>[[파일:"+item_element+"]]||<(>[[파일:"+item_ammunition+"]]||"
    namu3 = '||<-2><(>\'\'{{{-2 {{{#DDD '+item_collection+'}}}}}}\'\'||'
    namu4 = '[include(틀:데스티니 가디언즈/무기 정보, '+item_type+', v1='+str(item_stats[v1])+', v2='+str(item_stats[v2])+', v3='+str(item_stats[v3])+', v4='+str(item_stats[v4])+', v5='+str(item_stats[v5])+', v6='+str(item_stats[v6])+', v7='+str(item_stats[v7])+', )]'

    top="||<table width=500px><rowbgcolor=#222> '''{{{#FFF 총열}}}''' || '''{{{#FFF 탄창}}}''' || '''{{{#FFF 속성 1}}}''' || '''{{{#FFF 속성 2}}}''' ||\n||<-4> '''고정 특성''' ||"
    stat_top = "||<rowbgcolor=#444> [[파일:데스티니가디언즈_"+fdata_scope.replace(" ","")+".png|width=40px]][br]{{{#FFF "+fdata_scope+"}}} || [[파일:데스티니가디언즈_"+fdata_magazine.replace(" ","")+".png|width=40px]][br]{{{#FFF "+fdata_magazine+"}}} || [[파일:데스티니가디언즈_"+fdata_trait1.replace(" ","")+".png|width=40px]][br]{{{#FFF "+fdata_trait1+"}}} || [[파일:데스티니가디언즈_"+fdata_trait2.replace(" ","")+".png|width=40px]][br]{{{#FFF "+fdata_trait2+"}}} ||"
    random_perk = "||<-4> '''무작위 특성''' ||"
    patton = '{{{#!folding [ 펼치기 · 접기 ]\n{{{#!wiki style="margin:-5px -1px -15px"'
    stat_option = "<width=25%><colbgcolor=#444> "
    stat_option2 = " {{{#!wiki style=\"margin:0 -10px\""
    stat_option3 = '}}}}}}}}} ||'

    scope_list = stat_image_namu(scope_socket_data)
    magazine_list = stat_image_namu(magazine_socket_data)
    trait1_list = stat_image_namu(trait1_socket_data)
    trait2_list = stat_image_namu(trait2_socket_data)


    text1.insert(1.0, namu1)
    text1.insert(END, '\n')
    text1.insert(END, namu2)
    text1.insert(END, '\n')
    text1.insert(END, namu3)
    text1.insert(END, '\n')
    text1.insert(END, namu4)
    text1.insert(END, '\n')
    text1.insert(END, top)
    text1.insert(END, '\n')
    text1.insert(END, stat_top)
    text1.insert(END, '\n')
    text1.insert(END, random_perk)
    text1.insert(END, '\n')
    stat_option2_ = "||"+stat_option2
    text1.insert(END, stat_option2_)
    text1.insert(END, '\n')
    text1.insert(END, patton)

    del scope_list[0]
    stat_image_random_namu(scope_list)

    text1.insert(END, stat_option2)
    text1.insert(END, '\n')
    text1.insert(END, patton)

    del magazine_list[0]
    stat_image_random_namu(magazine_list)

    text1.insert(END, stat_option2)
    text1.insert(END, '\n')
    text1.insert(END, patton)

    del trait1_list[0]
    stat_image_random_namu(trait1_list)

    text1.insert(END, stat_option2)
    text1.insert(END, '\n')
    text1.insert(END, patton)

    del trait2_list[0]
    stat_image_random_namu(trait2_list)


def scope_socket():
    global reusablePlugItems1
    global scope_socket_data
    scope_socket_data = []
    fprint = []
    list_names = []
    list_donw1.delete("1.0","end")

    rprint = item_response.get("Response").get("sockets").get("socketEntries")[1].get("randomizedPlugSetHash")
    reusablePlugItems1 = Checking_file_DestinyPlugSetDefinition(rprint)
    list_len = reusablePlugItems1.get("Response").get("reusablePlugItems")
    fprint.append(item_response.get("Response").get("sockets").get("socketEntries")[1].get("singleInitialItemHash"))
    list_len_plus = len(list_len)+1
    for i in range(len(list_len)):
        fprint.append(reusablePlugItems1.get("Response").get("reusablePlugItems")[i].get("plugItemHash"))
    for i in range(list_len_plus):
        getyou_hash = fprint[i]
        displayProperties = Checking_file_DestinyInventoryItemDefinition(getyou_hash)
        item_name = displayProperties.get("Response").get("displayProperties").get("name")
        list_names.append(item_name+ '\n')
    list_donw1.insert(1.0, "".join(list_names))

    for A1 in range(list_len_plus):
        #scope_socket_data.append('[br]')
        scope_socket_data.append(list_names[A1].replace("\n",""))
    #del scope_socket_data[0]

def magazine_socket():
    global reusablePlugItems2
    global magazine_socket_data
    magazine_socket_data = []
    fprint = []
    list_names = []
    list_donw2.delete("1.0","end")
    rprint2 = item_response.get("Response").get("sockets").get("socketEntries")[2].get("randomizedPlugSetHash")

    reusablePlugItems2 = Checking_file_DestinyPlugSetDefinition(rprint2)

    list_len = reusablePlugItems2.get("Response").get("reusablePlugItems")
    fprint.append(item_response.get("Response").get("sockets").get("socketEntries")[2].get("singleInitialItemHash"))
    list_len_plus = len(list_len) + 1
    for i in range(len(list_len)):
        fprint.append(reusablePlugItems2.get("Response").get("reusablePlugItems")[i].get("plugItemHash"))
    for i in range(list_len_plus):
        getyou_hash = fprint[i]
        displayProperties = Checking_file_DestinyInventoryItemDefinition(getyou_hash)
        item_name = displayProperties.get("Response").get("displayProperties").get("name")
        list_names.append(item_name + '\n')
    list_donw2.insert(1.0, "".join(list_names))

    for A1 in range(len(list_names)):
        #magazine_socket_data.append('[br]')
        magazine_socket_data.append(list_names[A1].replace("\n",""))
    #del magazine_socket_data[0]

def trait1_socket():
    global reusablePlugItems3
    global trait1_socket_data
    trait1_socket_data = []
    fprint = []
    list_names = []
    list_donw3.delete("1.0","end")
    rprint3 = item_response.get("Response").get("sockets").get("socketEntries")[3].get("randomizedPlugSetHash")

    reusablePlugItems3 = Checking_file_DestinyPlugSetDefinition(rprint3)

    list_len = reusablePlugItems3.get("Response").get("reusablePlugItems")
    fprint.append(item_response.get("Response").get("sockets").get("socketEntries")[3].get("singleInitialItemHash"))
    list_len_plus = len(list_len) + 1
    for i in range(len(list_len)):
        fprint.append(reusablePlugItems3.get("Response").get("reusablePlugItems")[i].get("plugItemHash"))
    for i in range(list_len_plus):
        getyou_hash = fprint[i]
        displayProperties = Checking_file_DestinyInventoryItemDefinition(getyou_hash)
        item_name = displayProperties.get("Response").get("displayProperties").get("name")
        list_names.append(item_name + '\n')
    list_donw3.insert(1.0, "".join(list_names))

    for A1 in range(len(list_names)):
        #trait1_socket_data.append('[br]')
        trait1_socket_data.append(list_names[A1].replace("\n",""))
    #del trait1_socket_data[0]

def trait2_socket():
    global reusablePlugItems4
    global trait2_socket_data
    trait2_socket_data = []
    fprint = []
    list_names = []
    list_donw4.delete("1.0","end")
    rprint4 = item_response.get("Response").get("sockets").get("socketEntries")[4].get("randomizedPlugSetHash")

    reusablePlugItems4 = Checking_file_DestinyPlugSetDefinition(rprint4)

    list_len = reusablePlugItems4.get("Response").get("reusablePlugItems")
    fprint.append(item_response.get("Response").get("sockets").get("socketEntries")[4].get("singleInitialItemHash"))
    list_len_plus = len(list_len) + 1
    for i in range(len(list_len)):
        fprint.append(reusablePlugItems4.get("Response").get("reusablePlugItems")[i].get("plugItemHash"))
    for i in range(list_len_plus):
        getyou_hash = fprint[i]
        displayProperties = Checking_file_DestinyInventoryItemDefinition(getyou_hash)
        item_name = displayProperties.get("Response").get("displayProperties").get("name")
        list_names.append(item_name + '\n')
    list_donw4.insert(1.0, "".join(list_names))

    for A1 in range(len(list_names)):
        #trait2_socket_data.append('[br]')
        trait2_socket_data.append(list_names[A1].replace("\n",""))
    #del trait2_socket_data[0]

def socketEntries_Legendary():
    scope_socket()
    magazine_socket()
    trait1_socket()
    trait2_socket()
    #label2.config(text=name_sum)


def specificity():
    global frame_down1,frame_down2,frame_down3,frame_down4, main_frame2
    global list_donw1,list_donw2,list_donw3,list_donw4
    global btns1, btns2, btns3, btns4
    global labels1, labels2, labels3, labels4
    main_frame2 = Frame(root, bg='#FFF38A', bd=20)
    frame_down1 = Frame(main_frame2)
    frame_down2 = Frame(main_frame2, bg='#BDFFE3')
    frame_down3 = Frame(main_frame2)
    #frame_down4 = Frame(main_frame2)
    list_donw1 = Text(frame_down2,width=15,height=10)
    list_donw2 = Text(frame_down2,width=15,height=10)
    list_donw3 = Text(frame_down2,width=15,height=10)
    list_donw4 = Text(frame_down2,width=15,height=10)

    labels1 = Label(frame_down3,text="--------",width=14,height=0)
    labels2 = Label(frame_down3,text="--------",width=14,height=0)
    labels3 = Label(frame_down3,text="--------",width=14,height=0)
    labels4 = Label(frame_down3,text="--------",width=14,height=0)

    main_frame2.pack()
    frame_down1.pack(side=TOP,anchor=N)
    frame_down2.pack(side=TOP,anchor=S)
    frame_down3.pack(side=BOTTOM,anchor=N)
    #frame_down3.pack(side=LEFT,anchor=N)
    #frame_down4.pack(side=LEFT,anchor=N)

    list_donw1.pack(side=LEFT, anchor=N)
    list_donw2.pack(side=LEFT, anchor=N)
    list_donw3.pack(side=LEFT, anchor=N)
    list_donw4.pack(side=LEFT, anchor=N)

    labels1.pack(side=LEFT, anchor=N)
    labels2.pack(side=LEFT, anchor=N)
    labels3.pack(side=LEFT, anchor=N)
    labels4.pack(side=LEFT, anchor=N)

def seting():
    global imagephoto,label1, btn1, list1, combo1, btn2, scroll1, frame1, frame2, main_frame, frame3
    global frame1_left,frame1_right, scroll1, label2, entr1
    main_frame = Frame(root, bg='light blue', bd=10 )
    frame1 = Frame(main_frame,bd=6,bg='white')
    frame2 = Frame(main_frame, bg='red')
    frame3 = Frame(main_frame,bg='light green',relief="solid")
    frame1_left = Frame(frame1)
    frame1_right = Frame(frame1)

    imagephoto = ImageTk.PhotoImage(Image.open(data_location+"main.jpg"))
    label1 = Label(frame2, image=imagephoto)
    entr1 = Entry(frame1_left, width=20)
    entr1.insert(END, "용자리")
    btn1 = Button(frame1_left, text="상세 검색", command=findinformation)

    scroll1 = Scrollbar(frame1_right,orient="vertical")
    list1 = Listbox(frame1_right, selectmode='extended',height=0, yscrollcommand=scroll1.set)
    combo1 = ttk.Combobox(frame1, width=20,textvariable=str)
    btn2 = Button(frame1_left, text="아이템 검색", command=btndef)
    label2 = Text(frame3,width=25,height=5)

def seting_ui():
    main_frame.pack()
    frame1.pack(side=TOP)
    frame1_left.pack(side=LEFT)
    frame1_right.pack(side=RIGHT)
    frame2.pack(side=LEFT)
    frame3.pack(side=RIGHT)
    entr1.pack(side=TOP)
    btn1.pack(side=BOTTOM, fill=X)
    btn2.pack(side=BOTTOM, fill=X, anchor=S)
    #txt_detalie.pack()
    list1.pack(side=LEFT)
    scroll1.pack(side=RIGHT,fill=Y)
    #combo1.grid(row=1,column=0)
    label1.pack()
    label2.pack()
    specificity()

def text_gui():
    global main_frame3,text1,btni1

    main_frame3 = Frame(root, bg='#C3E873', bd=10)
    text1 = Text(main_frame3,width=30,height=5)
    btni1 = Button(main_frame3,text="MAKE",width=10,height=0,command=make_dim_wishlist)

    main_frame3.pack()
    btni1.pack(side=LEFT, anchor=N)
    text1.pack(side=RIGHT, anchor=N)

if __name__ == "__main__":
    seting()
    seting_ui()
    text_gui()
    root.mainloop()