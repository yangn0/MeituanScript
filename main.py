import requests
import json,time,traceback
import datetime

print("作者qq：792301982")

submit_url = "https://health.meituan.com/api/sghospital/doctor/workShift/submitApply?yodaReady=h5"
info_url = "https://health.meituan.com/api/sghospital/doctor/workShift/getTableInfo?startTime=%s&endTime=%s&yodaReady=h5"

# headers转换
def trans(s):
    d = dict()
    s = s.split("\n")
    for i in s:
        if(i == ''):
            continue
        if(i[0] == ":"):
            i = i[1:]
        d[i.split(': ')[0]] = i.split(': ')[1]
    return d


headers = '''Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7
Cache-Control: no-cache
Connection: keep-alive
Host: health.meituan.com
M-APPKEY: fe_com.sankuai.medicine.fe.selfinquiry
M-TRACEID: 9000862326025147867
Pragma: no-cache
Referer: https://health.meituan.com/selfInquiry
sec-ch-ua: "Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
token: pGBJla7R_0NAdtzqQn3V-m9hNweCHsRD8fM3ot0JTHO4AmwVOQoWKLbaQuJvO1Ty96d2JkgbUVt29tZ9K3JMVA
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36
'''
cookie="_lxsdk_cuid=18645353081c8-08933fc4e72e4a-26021051-384000-18645353081c8; _lxsdk=18645353081c8-08933fc4e72e4a-26021051-384000-18645353081c8; e_b_id_352126=a2b85b6dd5c63b8d8649ebdfa2ac7065; WEBDFPID=0z0vvz2025005x11zyu5940879809zy8813546399v5979585z0wzwy4-1991558412669-1676198412669GASYSOCfd79fef3d01d5e9aadc18ccd4d0c95073864; token=_oYUS_bFdTei6BozV-lwtPfd8hqox6WDdGPXxFlsRiTKbQ1SRqyouZ4pkur9gK-3EcpexMWjdHYngjnCCLpVvw; bizType=2; accountId=137049837; name=HJH1427101411; hospitalName=%25E9%259D%2592%25E5%25B2%259B%25E7%2599%25BE%25E5%25AF%25BF%25E4%25BA%2592%25E8%2581%2594%25E7%25BD%2591%25E5%258C%25BB%25E9%2599%25A2; accountType=2; acctId=10103; logan_session_token=6gd6ayudqos6rxwzt21w; _lxsdk_s=18654457767-15b-e48-e5f%7C%7C9"
token="_oYUS_bFdTei6BozV-lwtPfd8hqox6WDdGPXxFlsRiTKbQ1SRqyouZ4pkur9gK-3EcpexMWjdHYngjnCCLpVvw"
headers = trans(headers)
headers["Cookie"]=cookie
headers['token']=token

def get_info(starttime="",endtime=""):
    d=dict()
    try:
        r=requests.get(info_url%(starttime,endtime),headers=headers)
        d=json.loads(r.text)
    except:
        d['success']="error"
        traceback.print_exc()
    return d

def submit(workShiftIds):
    d=dict()
    try:
        submit_form = {"workShiftIds": workShiftIds, "applyType": 1}
        r = requests.post(submit_url, headers=headers, json=submit_form)
        d=json.loads(r.text)
    except:
        d['success']="error"
        d['msg']=""
        traceback.print_exc()
    return d

def baoli():
    d=get_info()
    workShiftIds=list()
    sheet_list=list()
    sheet_list.append(d['data']['workShiftTableInfo'][0])
    sheet_list+=d['data']['workShiftTableInfo'][7:]
    for i in sheet_list:
        for u in i['workShiftCells']:
            if u['status']['expired']==False:
                workShiftIds.append(u['workShiftId'])
    while(1):
        # 选班上限40-个班次
        submit_rtn=submit(workShiftIds[-30:])
        print(time.asctime( time.localtime(time.time()) ),submit_rtn['success'],submit_rtn['msg'])

def simple():
    while(1):
        while(1):
            d=get_info()
            try:
                if d['success']=="error":
                    print(time.asctime( time.localtime(time.time()) ),"get_info",d['success'])
                    continue
            except:
                print(d)
                continue
            #print(time.asctime( time.localtime(time.time()) ),"get_info",d["success"])
            endDate=d['data']['weekSelectionInfo']['endDate']
            endDate=datetime.datetime.strptime(endDate, "%Y-%m-%d")
            nextweek_startdate=(endDate + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            nextweek_enddate=(endDate + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
            d_nextweek=get_info(nextweek_startdate,nextweek_enddate)
            try:
                if d_nextweek['success']=="error":
                    print(time.asctime( time.localtime(time.time()) ),"get_info",d_nextweek['success'])
                    continue
            except:
                print(d_nextweek)
                continue
            workShiftIds=list()
            sheet_list=list()
            sheet_list.append(d['data']['workShiftTableInfo'][0])
            sheet_list+=d['data']['workShiftTableInfo'][7:]
            for i in sheet_list:
                for u in i['workShiftCells']:
                    if u['status']['expired']==False and u['status']['workShiftStatus']!=1 and u['status']['applyStatus']!=1:
                        workShiftIds.append(u['workShiftId'])
            #nextweek
            if(len(d_nextweek['data']['workShiftTableInfo'])!=0):
                sheet_list.append(d_nextweek['data']['workShiftTableInfo'][0])
                sheet_list+=d_nextweek['data']['workShiftTableInfo'][7:]
                for i in sheet_list:
                    for u in i['workShiftCells']:
                        if u['status']['expired']==False and u['status']['workShiftStatus']!=1 and u['status']['applyStatus']!=1:
                            workShiftIds.append(u['workShiftId'])
            if len(workShiftIds)!=0:
                break
            
        submit_rtn=submit(workShiftIds[-30:])
        if submit_rtn['success']=="error":
            print(time.asctime( time.localtime(time.time()) ),"submit",submit_rtn)
            continue
        print(time.asctime( time.localtime(time.time()) ),"submit",submit_rtn,"len(workShiftIds):%s"%len(workShiftIds))
        
if __name__ =="__main__":
    simple()