from asyncio import tasks
from typing import Dict, List, Tuple
import requests
from re import compile
import asyncio
from aiohttp import ClientSession
from requests.models import HTTPError
# from GetCookies import GetCookies
# Give the cookies of the user to the class 'PostRequest'.
# Give the 'date' and the 'flag' of the report url and the report method will post the selfReport.


class PostRequest:

    res_find = compile(r'F\.alert\((.+?)\);')

    def __init__(self, cookie: Dict[str, str] = None, viewstate: str = None,proxy:str = None):
        self._cookie = cookie
        self.viewstate = viewstate
        self.proxy = proxy

    def setUserInfo(self, cookie: Dict[str, str], viewstate: str):
        self._cookie = cookie
        self.viewstate = viewstate

    def setProxy(self,proxy:str):
        self.proxy = proxy

    def report(self, date: str, state: str, filelog=False):
        cookies = self._cookie

        headers = {
            'Connection': 'keep-alive',
            'Accept': 'text/plain, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'X-FineUI-Ajax': 'true',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://selfreport.shu.edu.cn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': f'https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?day={date}&t={state}',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }

        params = (
            ('day', date),
            ('t', state),
        )

        data = {
            '__EVENTTARGET': 'p1$ctl00$btnSubmit',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.viewstate,
            '__VIEWSTATEGENERATOR': 'DC4D08A3',
            'p1$ChengNuo': 'p1_ChengNuo',
            'p1$BaoSRQ': date,
            'p1$DangQSTZK': '\u826F\u597D',
            'p1$TiWen': '36',
            'p1$ZaiXiao': '\u5B9D\u5C71',
            'p1$ddlSheng$Value': '\u4E0A\u6D77',
            'p1$ddlSheng': '\u4E0A\u6D77',
            'p1$ddlShi$Value': '\u4E0A\u6D77\u5E02',
            'p1$ddlShi': '\u4E0A\u6D77\u5E02',
            'p1$ddlXian$Value': '\u5B9D\u5C71\u533A',
            'p1$ddlXian': '\u5B9D\u5C71\u533A',
            'p1$FengXDQDL': '\u5426',
            'p1$TongZWDLH': '\u5426',
            'p1$XiangXDZ': '\u65B0\u6821\u533A\u6821\u5185S2',
            'p1$QueZHZJC$Value': '\u5426',
            'p1$QueZHZJC': '\u5426',
            'p1$DangRGL': '\u5426',
            'p1$GeLDZ': '',
            'p1$CengFWH': '\u5426',
            'p1$CengFWH_RiQi': '',
            'p1$CengFWH_BeiZhu': '',
            'p1$JieChu': '\u5426',
            'p1$JieChu_RiQi': '',
            'p1$JieChu_BeiZhu': '',
            'p1$TuJWH': '\u5426',
            'p1$TuJWH_RiQi': '',
            'p1$TuJWH_BeiZhu': '',
            'p1$JiaRen_BeiZhu': '',
            'p1$SuiSM': '\u7EFF\u8272',
            'p1$LvMa14Days': '\u662F',
            'p1$Address2': '',
            'F_TARGET': 'p1_ctl00_btnSubmit',
            'p1_GeLSM_Collapsed': 'false',
            'p1_Collapsed': 'false',
            'F_STATE': 'eyJwMV9CYW9TUlEiOnsiVGV4dCI6IjIwMjAtMTItMTUifSwicDFfRGFuZ1FTVFpLIjp7IkZfSXRlbXMiOltbIuiJr+WlvSIsIuiJr+WlvSIsMV0sWyLkuI3pgIIiLCLkuI3pgIIiLDFdXSwiU2VsZWN0ZWRWYWx1ZSI6IuiJr+WlvSJ9LCJwMV9aaGVuZ1podWFuZyI6eyJIaWRkZW4iOnRydWUsIkZfSXRlbXMiOltbIuaEn+WGkiIsIuaEn+WGkiIsMV0sWyLlkrPll70iLCLlkrPll70iLDFdLFsi5Y+R54OtIiwi5Y+R54OtIiwxXV0sIlNlbGVjdGVkVmFsdWVBcnJheSI6W119LCJwMV9UaVdlbiI6eyJUZXh0IjoiMzYuMCJ9LCJwMV9aYWlYaWFvIjp7IlNlbGVjdGVkVmFsdWUiOiLlrp3lsbEiLCJGX0l0ZW1zIjpbWyLkuI3lnKjmoKEiLCLkuI3lnKjmoKEiLDFdLFsi5a6d5bGxIiwi5a6d5bGx5qCh5Yy6IiwxXSxbIuW7tumVvyIsIuW7tumVv+agoeWMuiIsMV0sWyLlmInlrpoiLCLlmInlrprmoKHljLoiLDFdLFsi5paw6Ze46LevIiwi5paw6Ze46Lev5qCh5Yy6IiwxXV19LCJwMV9kZGxTaGVuZyI6eyJGX0l0ZW1zIjpbWyItMSIsIumAieaLqeecgeS7vSIsMSwiIiwiIl0sWyLljJfkuqwiLCLljJfkuqwiLDEsIiIsIiJdLFsi5aSp5rSlIiwi5aSp5rSlIiwxLCIiLCIiXSxbIuS4iua1tyIsIuS4iua1tyIsMSwiIiwiIl0sWyLph43luoYiLCLph43luoYiLDEsIiIsIiJdLFsi5rKz5YyXIiwi5rKz5YyXIiwxLCIiLCIiXSxbIuWxseilvyIsIuWxseilvyIsMSwiIiwiIl0sWyLovr3lroEiLCLovr3lroEiLDEsIiIsIiJdLFsi5ZCJ5p6XIiwi5ZCJ5p6XIiwxLCIiLCIiXSxbIum7kem+meaxnyIsIum7kem+meaxnyIsMSwiIiwiIl0sWyLmsZ/oi48iLCLmsZ/oi48iLDEsIiIsIiJdLFsi5rWZ5rGfIiwi5rWZ5rGfIiwxLCIiLCIiXSxbIuWuieW+vSIsIuWuieW+vSIsMSwiIiwiIl0sWyLnpo/lu7oiLCLnpo/lu7oiLDEsIiIsIiJdLFsi5rGf6KW/Iiwi5rGf6KW/IiwxLCIiLCIiXSxbIuWxseS4nCIsIuWxseS4nCIsMSwiIiwiIl0sWyLmsrPljZciLCLmsrPljZciLDEsIiIsIiJdLFsi5rmW5YyXIiwi5rmW5YyXIiwxLCIiLCIiXSxbIua5luWNlyIsIua5luWNlyIsMSwiIiwiIl0sWyLlub/kuJwiLCLlub/kuJwiLDEsIiIsIiJdLFsi5rW35Y2XIiwi5rW35Y2XIiwxLCIiLCIiXSxbIuWbm+W3nSIsIuWbm+W3nSIsMSwiIiwiIl0sWyLotLXlt54iLCLotLXlt54iLDEsIiIsIiJdLFsi5LqR5Y2XIiwi5LqR5Y2XIiwxLCIiLCIiXSxbIumZleilvyIsIumZleilvyIsMSwiIiwiIl0sWyLnlJjogoMiLCLnlJjogoMiLDEsIiIsIiJdLFsi6Z2S5rW3Iiwi6Z2S5rW3IiwxLCIiLCIiXSxbIuWGheiSmeWPpCIsIuWGheiSmeWPpCIsMSwiIiwiIl0sWyLlub/opb8iLCLlub/opb8iLDEsIiIsIiJdLFsi6KW/6JePIiwi6KW/6JePIiwxLCIiLCIiXSxbIuWugeWkjyIsIuWugeWkjyIsMSwiIiwiIl0sWyLmlrDnloYiLCLmlrDnloYiLDEsIiIsIiJdLFsi6aaZ5rivIiwi6aaZ5rivIiwxLCIiLCIiXSxbIua+s+mXqCIsIua+s+mXqCIsMSwiIiwiIl0sWyLlj7Dmub4iLCLlj7Dmub4iLDEsIiIsIiJdXSwiU2VsZWN0ZWRWYWx1ZUFycmF5IjpbIuS4iua1tyJdfSwicDFfZGRsU2hpIjp7IkVuYWJsZWQiOnRydWUsIkZfSXRlbXMiOltbIi0xIiwi6YCJ5oup5biCIiwxLCIiLCIiXSxbIuS4iua1t+W4giIsIuS4iua1t+W4giIsMSwiIiwiIl1dLCJTZWxlY3RlZFZhbHVlQXJyYXkiOlsi5LiK5rW35biCIl19LCJwMV9kZGxYaWFuIjp7IkVuYWJsZWQiOnRydWUsIkZfSXRlbXMiOltbIi0xIiwi6YCJ5oup5Y6/5Yy6IiwxLCIiLCIiXSxbIum7hOa1puWMuiIsIum7hOa1puWMuiIsMSwiIiwiIl0sWyLljaLmub7ljLoiLCLljaLmub7ljLoiLDEsIiIsIiJdLFsi5b6Q5rGH5Yy6Iiwi5b6Q5rGH5Yy6IiwxLCIiLCIiXSxbIumVv+WugeWMuiIsIumVv+WugeWMuiIsMSwiIiwiIl0sWyLpnZnlronljLoiLCLpnZnlronljLoiLDEsIiIsIiJdLFsi5pmu6ZmA5Yy6Iiwi5pmu6ZmA5Yy6IiwxLCIiLCIiXSxbIuiZueWPo+WMuiIsIuiZueWPo+WMuiIsMSwiIiwiIl0sWyLmnajmtabljLoiLCLmnajmtabljLoiLDEsIiIsIiJdLFsi5a6d5bGx5Yy6Iiwi5a6d5bGx5Yy6IiwxLCIiLCIiXSxbIumXteihjOWMuiIsIumXteihjOWMuiIsMSwiIiwiIl0sWyLlmInlrprljLoiLCLlmInlrprljLoiLDEsIiIsIiJdLFsi5p2+5rGf5Yy6Iiwi5p2+5rGf5Yy6IiwxLCIiLCIiXSxbIumHkeWxseWMuiIsIumHkeWxseWMuiIsMSwiIiwiIl0sWyLpnZLmtabljLoiLCLpnZLmtabljLoiLDEsIiIsIiJdLFsi5aWJ6LSk5Yy6Iiwi5aWJ6LSk5Yy6IiwxLCIiLCIiXSxbIua1puS4nOaWsOWMuiIsIua1puS4nOaWsOWMuiIsMSwiIiwiIl0sWyLltIfmmI7ljLoiLCLltIfmmI7ljLoiLDEsIiIsIiJdXSwiU2VsZWN0ZWRWYWx1ZUFycmF5IjpbIuWuneWxseWMuiJdfSwicDFfRmVuZ1hEUURMIjp7IkxhYmVsIjoiMTLmnIgwMeaXpeiHszEy5pyIMTXml6XmmK/lkKblnKjkuK3pq5jpo47pmanlnLDljLrpgJfnlZk8c3BhbiBzdHlsZT0nY29sb3I6cmVkOyc+77yI5YaF6JKZ5Y+k5ruh5rSy6YeM5Lic5bGx6KGX6YGT44CB5YyX5Yy66KGX6YGT5Yqe5LqL5aSE77yM5omO6LWJ6K+65bCU5Yy656ys5LiJ44CB56ys5Zub44CB56ys5LqU6KGX6YGT5Yqe5LqL5aSE77yM5oiQ6YO95biC6YOr6YO95Yy66YOr562S6KGX6YGT5aSq5bmz5p2R44CB6I+g6JCd56S+5Yy65Lit6ZOB5aWl57u05bCU5LqM5pyf44CB5LiJ5pyf44CB6YOr6YO95Yy65ZSQ5piM6ZWH5rC45a6J5p2ROOe7hOOAgeaIkOWNjuWMuuW0lOWutuW6l+WNjumDveS6keaZr+WPsOWwj+WMuu+8jOm7kem+meaxn+eJoeS4ueaxn+W4guS4nOWugeW4guS4reW/g+ekvuWMuuOAgee7peiKrOays+W4gumdkuS6keWwj+WMuu+8jOaWsOeWhuWQkOmygeeVquW4gue6ouebvuWwj+WMuu+8iTwvc3Bhbj4iLCJTZWxlY3RlZFZhbHVlIjoi5ZCmIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dfSwicDFfVG9uZ1pXRExIIjp7IkxhYmVsIjoi5LiK5rW35ZCM5L2P5Lq65ZGY5piv5ZCm5pyJMTLmnIgwMeaXpeiHszEy5pyIMTXml6XmnaXoh6rkuK3pq5jpo47pmanlnLDljLrnmoTkuro8c3BhbiBzdHlsZT0nY29sb3I6cmVkOyc+77yI5YaF6JKZ5Y+k5ruh5rSy6YeM5Lic5bGx6KGX6YGT44CB5YyX5Yy66KGX6YGT5Yqe5LqL5aSE77yM5omO6LWJ6K+65bCU5Yy656ys5LiJ44CB56ys5Zub44CB56ys5LqU6KGX6YGT5Yqe5LqL5aSE77yM5oiQ6YO95biC6YOr6YO95Yy66YOr562S6KGX6YGT5aSq5bmz5p2R44CB6I+g6JCd56S+5Yy65Lit6ZOB5aWl57u05bCU5LqM5pyf44CB5LiJ5pyf44CB6YOr6YO95Yy65ZSQ5piM6ZWH5rC45a6J5p2ROOe7hOOAgeaIkOWNjuWMuuW0lOWutuW6l+WNjumDveS6keaZr+WPsOWwj+WMuu+8jOm7kem+meaxn+eJoeS4ueaxn+W4guS4nOWugeW4guS4reW/g+ekvuWMuuOAgee7peiKrOays+W4gumdkuS6keWwj+WMuu+8jOaWsOeWhuWQkOmygeeVquW4gue6ouebvuWwj+WMuu+8iTwvc3Bhbj4iLCJTZWxlY3RlZFZhbHVlIjoi5ZCmIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dfSwicDFfWGlhbmdYRFoiOnsiVGV4dCI6IuaWsOagoeWMuuagoeWGhVMyIn0sInAxX1F1ZVpIWkpDIjp7IkZfSXRlbXMiOltbIuaYryIsIuaYryIsMSwiIiwiIl0sWyLlkKYiLCLlkKYiLDEsIiIsIiJdXSwiU2VsZWN0ZWRWYWx1ZUFycmF5IjpbIuWQpiJdfSwicDFfRGFuZ1JHTCI6eyJTZWxlY3RlZFZhbHVlIjoi5ZCmIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dfSwicDFfR2VMU00iOnsiSGlkZGVuIjp0cnVlLCJJRnJhbWVBdHRyaWJ1dGVzIjp7fX0sInAxX0dlTEZTIjp7IlJlcXVpcmVkIjpmYWxzZSwiSGlkZGVuIjp0cnVlLCJGX0l0ZW1zIjpbWyLlsYXlrrbpmpTnprsiLCLlsYXlrrbpmpTnprsiLDFdLFsi6ZuG5Lit6ZqU56a7Iiwi6ZuG5Lit6ZqU56a7IiwxXV0sIlNlbGVjdGVkVmFsdWUiOm51bGx9LCJwMV9HZUxEWiI6eyJIaWRkZW4iOnRydWV9LCJwMV9DZW5nRldIIjp7IkxhYmVsIjoiMTLmnIgwMeaXpeiHszEy5pyIMTXml6XmmK/lkKblnKjkuK3pq5jpo47pmanlnLDljLrpgJfnlZnov4c8c3BhbiBzdHlsZT0nY29sb3I6cmVkOyc+77yI5YaF6JKZ5Y+k5ruh5rSy6YeM5Lic5bGx6KGX6YGT44CB5YyX5Yy66KGX6YGT5Yqe5LqL5aSE77yM5omO6LWJ6K+65bCU5Yy656ys5LiJ44CB56ys5Zub44CB56ys5LqU6KGX6YGT5Yqe5LqL5aSE77yM5oiQ6YO95biC6YOr6YO95Yy66YOr562S6KGX6YGT5aSq5bmz5p2R44CB6I+g6JCd56S+5Yy65Lit6ZOB5aWl57u05bCU5LqM5pyf44CB5LiJ5pyf44CB6YOr6YO95Yy65ZSQ5piM6ZWH5rC45a6J5p2ROOe7hOOAgeaIkOWNjuWMuuW0lOWutuW6l+WNjumDveS6keaZr+WPsOWwj+WMuu+8jOm7kem+meaxn+eJoeS4ueaxn+W4guS4nOWugeW4guS4reW/g+ekvuWMuuOAgee7peiKrOays+W4gumdkuS6keWwj+WMuu+8jOaWsOeWhuWQkOmygeeVquW4gue6ouebvuWwj+WMuu+8iTwvc3Bhbj4iLCJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8iLDFdLFsi5ZCmIiwi5ZCmIiwxXV0sIlNlbGVjdGVkVmFsdWUiOiLlkKYifSwicDFfQ2VuZ0ZXSF9SaVFpIjp7IkhpZGRlbiI6dHJ1ZX0sInAxX0NlbmdGV0hfQmVpWmh1Ijp7IkhpZGRlbiI6dHJ1ZX0sInAxX0ppZUNodSI6eyJMYWJlbCI6IjEy5pyIMDHml6Xoh7MxMuaciDE15pel5piv5ZCm5LiO5p2l6Ieq5Lit6auY6aOO6Zmp5Zyw5Yy65Y+R54Ot5Lq65ZGY5a+G5YiH5o6l6KemPHNwYW4gc3R5bGU9J2NvbG9yOnJlZDsnPu+8iOWGheiSmeWPpOa7oea0sumHjOS4nOWxseihl+mBk+OAgeWMl+WMuuihl+mBk+WKnuS6i+WkhO+8jOaJjui1ieivuuWwlOWMuuesrOS4ieOAgeesrOWbm+OAgeesrOS6lOihl+mBk+WKnuS6i+WkhO+8jOaIkOmDveW4gumDq+mDveWMuumDq+etkuihl+mBk+WkquW5s+adkeOAgeiPoOiQneekvuWMuuS4remTgeWlpee7tOWwlOS6jOacn+OAgeS4ieacn+OAgemDq+mDveWMuuWUkOaYjOmVh+awuOWuieadkTjnu4TjgIHmiJDljY7ljLrltJTlrrblupfljY7pg73kupHmma/lj7DlsI/ljLrvvIzpu5HpvpnmsZ/niaHkuLnmsZ/luILkuJzlroHluILkuK3lv4PnpL7ljLrjgIHnu6XoiqzmsrPluILpnZLkupHlsI/ljLrvvIzmlrDnloblkJDpsoHnlarluILnuqLnm77lsI/ljLrvvIk8L3NwYW4+IiwiU2VsZWN0ZWRWYWx1ZSI6IuWQpiIsIkZfSXRlbXMiOltbIuaYryIsIuaYryIsMV0sWyLlkKYiLCLlkKYiLDFdXX0sInAxX0ppZUNodV9SaVFpIjp7IkhpZGRlbiI6dHJ1ZX0sInAxX0ppZUNodV9CZWlaaHUiOnsiSGlkZGVuIjp0cnVlfSwicDFfVHVKV0giOnsiTGFiZWwiOiIxMuaciDAx5pel6IezMTLmnIgxNeaXpeaYr+WQpuS5mOWdkOWFrOWFseS6pOmAmumAlOW+hOS4remrmOmjjumZqeWcsOWMujxzcGFuIHN0eWxlPSdjb2xvcjpyZWQ7Jz7vvIjlhoXokpnlj6Tmu6HmtLLph4zkuJzlsbHooZfpgZPjgIHljJfljLrooZfpgZPlip7kuovlpITvvIzmiY7otYnor7rlsJTljLrnrKzkuInjgIHnrKzlm5vjgIHnrKzkupTooZfpgZPlip7kuovlpITvvIzmiJDpg73luILpg6vpg73ljLrpg6vnrZLooZfpgZPlpKrlubPmnZHjgIHoj6DokJ3npL7ljLrkuK3pk4HlpaXnu7TlsJTkuozmnJ/jgIHkuInmnJ/jgIHpg6vpg73ljLrllJDmmIzplYfmsLjlronmnZE457uE44CB5oiQ5Y2O5Yy65bSU5a625bqX5Y2O6YO95LqR5pmv5Y+w5bCP5Yy677yM6buR6b6Z5rGf54mh5Li55rGf5biC5Lic5a6B5biC5Lit5b+D56S+5Yy644CB57ul6Iqs5rKz5biC6Z2S5LqR5bCP5Yy677yM5paw55aG5ZCQ6bKB55Wq5biC57qi55u+5bCP5Yy677yJPC9zcGFuPiIsIlNlbGVjdGVkVmFsdWUiOiLlkKYiLCJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8iLDFdLFsi5ZCmIiwi5ZCmIiwxXV19LCJwMV9UdUpXSF9SaVFpIjp7IkhpZGRlbiI6dHJ1ZX0sInAxX1R1SldIX0JlaVpodSI6eyJIaWRkZW4iOnRydWV9LCJwMV9KaWFSZW4iOnsiTGFiZWwiOiIxMuaciDAx5pel6IezMTLmnIgxNeaXpeWutuS6uuaYr+WQpuacieWPkeeDreetieeXh+eKtiJ9LCJwMV9KaWFSZW5fQmVpWmh1Ijp7IkhpZGRlbiI6dHJ1ZX0sInAxX1N1aVNNIjp7IlNlbGVjdGVkVmFsdWUiOiLnu7/oibIiLCJGX0l0ZW1zIjpbWyLnuqLoibIiLCLnuqLoibIiLDFdLFsi6buE6ImyIiwi6buE6ImyIiwxXSxbIue7v+iJsiIsIue7v+iJsiIsMV1dfSwicDFfTHZNYTE0RGF5cyI6eyJTZWxlY3RlZFZhbHVlIjoi5pivIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dfSwicDEiOnsiVGl0bGUiOiLmr4/ml6XkuKTmiqXvvIjkuIvljYjvvIkiLCJJRnJhbWVBdHRyaWJ1dGVzIjp7fX19'
        }
        proxies = {
                "http"  : self.proxy,
                "https" : self.proxy,
        }

        response = requests.post('https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx',
                                 headers=headers, params=params, cookies=cookies, data=data,proxies=proxies)
        print('Referer:', headers['Referer'], end=f'[{response.status_code}]')
        res = self.res_find.search(response.text)
        if res and not filelog:
            print(res[1])

    async def async_report(self, session: ClientSession, date: str, state: str):
        # cookies = self._cookie
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'text/plain, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'X-FineUI-Ajax': 'true',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://selfreport.shu.edu.cn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': f'https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?day={date}&t={state}',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }

        params = (
            ('day', date),
            ('t', state),
        )

        data = {
            '__EVENTTARGET': 'p1$ctl00$btnSubmit',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.viewstate,
            '__VIEWSTATEGENERATOR': 'DC4D08A3',
            'p1$ChengNuo': 'p1_ChengNuo',
            'p1$BaoSRQ': date,
            'p1$DangQSTZK': '\u826F\u597D',
            'p1$TiWen': '36',
            'p1$ZaiXiao': '\u5B9D\u5C71',
            'p1$ddlSheng$Value': '\u4E0A\u6D77',
            'p1$ddlSheng': '\u4E0A\u6D77',
            'p1$ddlShi$Value': '\u4E0A\u6D77\u5E02',
            'p1$ddlShi': '\u4E0A\u6D77\u5E02',
            'p1$ddlXian$Value': '\u5B9D\u5C71\u533A',
            'p1$ddlXian': '\u5B9D\u5C71\u533A',
            'p1$FengXDQDL': '\u5426',
            'p1$TongZWDLH': '\u5426',
            'p1$XiangXDZ': '\u65B0\u6821\u533A\u6821\u5185S2',
            'p1$QueZHZJC$Value': '\u5426',
            'p1$QueZHZJC': '\u5426',
            'p1$DangRGL': '\u5426',
            'p1$GeLDZ': '',
            'p1$CengFWH': '\u5426',
            'p1$CengFWH_RiQi': '',
            'p1$CengFWH_BeiZhu': '',
            'p1$JieChu': '\u5426',
            'p1$JieChu_RiQi': '',
            'p1$JieChu_BeiZhu': '',
            'p1$TuJWH': '\u5426',
            'p1$TuJWH_RiQi': '',
            'p1$TuJWH_BeiZhu': '',
            'p1$JiaRen_BeiZhu': '',
            'p1$SuiSM': '\u7EFF\u8272',
            'p1$LvMa14Days': '\u662F',
            'p1$Address2': '',
            'F_TARGET': 'p1_ctl00_btnSubmit',
            'p1_GeLSM_Collapsed': 'false',
            'p1_Collapsed': 'false',
            'F_STATE': 'eyJwMV9CYW9TUlEiOnsiVGV4dCI6IjIwMjAtMTItMTUifSwicDFfRGFuZ1FTVFpLIjp7IkZfSXRlbXMiOltbIuiJr+WlvSIsIuiJr+WlvSIsMV0sWyLkuI3pgIIiLCLkuI3pgIIiLDFdXSwiU2VsZWN0ZWRWYWx1ZSI6IuiJr+WlvSJ9LCJwMV9aaGVuZ1podWFuZyI6eyJIaWRkZW4iOnRydWUsIkZfSXRlbXMiOltbIuaEn+WGkiIsIuaEn+WGkiIsMV0sWyLlkrPll70iLCLlkrPll70iLDFdLFsi5Y+R54OtIiwi5Y+R54OtIiwxXV0sIlNlbGVjdGVkVmFsdWVBcnJheSI6W119LCJwMV9UaVdlbiI6eyJUZXh0IjoiMzYuMCJ9LCJwMV9aYWlYaWFvIjp7IlNlbGVjdGVkVmFsdWUiOiLlrp3lsbEiLCJGX0l0ZW1zIjpbWyLkuI3lnKjmoKEiLCLkuI3lnKjmoKEiLDFdLFsi5a6d5bGxIiwi5a6d5bGx5qCh5Yy6IiwxXSxbIuW7tumVvyIsIuW7tumVv+agoeWMuiIsMV0sWyLlmInlrpoiLCLlmInlrprmoKHljLoiLDFdLFsi5paw6Ze46LevIiwi5paw6Ze46Lev5qCh5Yy6IiwxXV19LCJwMV9kZGxTaGVuZyI6eyJGX0l0ZW1zIjpbWyItMSIsIumAieaLqeecgeS7vSIsMSwiIiwiIl0sWyLljJfkuqwiLCLljJfkuqwiLDEsIiIsIiJdLFsi5aSp5rSlIiwi5aSp5rSlIiwxLCIiLCIiXSxbIuS4iua1tyIsIuS4iua1tyIsMSwiIiwiIl0sWyLph43luoYiLCLph43luoYiLDEsIiIsIiJdLFsi5rKz5YyXIiwi5rKz5YyXIiwxLCIiLCIiXSxbIuWxseilvyIsIuWxseilvyIsMSwiIiwiIl0sWyLovr3lroEiLCLovr3lroEiLDEsIiIsIiJdLFsi5ZCJ5p6XIiwi5ZCJ5p6XIiwxLCIiLCIiXSxbIum7kem+meaxnyIsIum7kem+meaxnyIsMSwiIiwiIl0sWyLmsZ/oi48iLCLmsZ/oi48iLDEsIiIsIiJdLFsi5rWZ5rGfIiwi5rWZ5rGfIiwxLCIiLCIiXSxbIuWuieW+vSIsIuWuieW+vSIsMSwiIiwiIl0sWyLnpo/lu7oiLCLnpo/lu7oiLDEsIiIsIiJdLFsi5rGf6KW/Iiwi5rGf6KW/IiwxLCIiLCIiXSxbIuWxseS4nCIsIuWxseS4nCIsMSwiIiwiIl0sWyLmsrPljZciLCLmsrPljZciLDEsIiIsIiJdLFsi5rmW5YyXIiwi5rmW5YyXIiwxLCIiLCIiXSxbIua5luWNlyIsIua5luWNlyIsMSwiIiwiIl0sWyLlub/kuJwiLCLlub/kuJwiLDEsIiIsIiJdLFsi5rW35Y2XIiwi5rW35Y2XIiwxLCIiLCIiXSxbIuWbm+W3nSIsIuWbm+W3nSIsMSwiIiwiIl0sWyLotLXlt54iLCLotLXlt54iLDEsIiIsIiJdLFsi5LqR5Y2XIiwi5LqR5Y2XIiwxLCIiLCIiXSxbIumZleilvyIsIumZleilvyIsMSwiIiwiIl0sWyLnlJjogoMiLCLnlJjogoMiLDEsIiIsIiJdLFsi6Z2S5rW3Iiwi6Z2S5rW3IiwxLCIiLCIiXSxbIuWGheiSmeWPpCIsIuWGheiSmeWPpCIsMSwiIiwiIl0sWyLlub/opb8iLCLlub/opb8iLDEsIiIsIiJdLFsi6KW/6JePIiwi6KW/6JePIiwxLCIiLCIiXSxbIuWugeWkjyIsIuWugeWkjyIsMSwiIiwiIl0sWyLmlrDnloYiLCLmlrDnloYiLDEsIiIsIiJdLFsi6aaZ5rivIiwi6aaZ5rivIiwxLCIiLCIiXSxbIua+s+mXqCIsIua+s+mXqCIsMSwiIiwiIl0sWyLlj7Dmub4iLCLlj7Dmub4iLDEsIiIsIiJdXSwiU2VsZWN0ZWRWYWx1ZUFycmF5IjpbIuS4iua1tyJdfSwicDFfZGRsU2hpIjp7IkVuYWJsZWQiOnRydWUsIkZfSXRlbXMiOltbIi0xIiwi6YCJ5oup5biCIiwxLCIiLCIiXSxbIuS4iua1t+W4giIsIuS4iua1t+W4giIsMSwiIiwiIl1dLCJTZWxlY3RlZFZhbHVlQXJyYXkiOlsi5LiK5rW35biCIl19LCJwMV9kZGxYaWFuIjp7IkVuYWJsZWQiOnRydWUsIkZfSXRlbXMiOltbIi0xIiwi6YCJ5oup5Y6/5Yy6IiwxLCIiLCIiXSxbIum7hOa1puWMuiIsIum7hOa1puWMuiIsMSwiIiwiIl0sWyLljaLmub7ljLoiLCLljaLmub7ljLoiLDEsIiIsIiJdLFsi5b6Q5rGH5Yy6Iiwi5b6Q5rGH5Yy6IiwxLCIiLCIiXSxbIumVv+WugeWMuiIsIumVv+WugeWMuiIsMSwiIiwiIl0sWyLpnZnlronljLoiLCLpnZnlronljLoiLDEsIiIsIiJdLFsi5pmu6ZmA5Yy6Iiwi5pmu6ZmA5Yy6IiwxLCIiLCIiXSxbIuiZueWPo+WMuiIsIuiZueWPo+WMuiIsMSwiIiwiIl0sWyLmnajmtabljLoiLCLmnajmtabljLoiLDEsIiIsIiJdLFsi5a6d5bGx5Yy6Iiwi5a6d5bGx5Yy6IiwxLCIiLCIiXSxbIumXteihjOWMuiIsIumXteihjOWMuiIsMSwiIiwiIl0sWyLlmInlrprljLoiLCLlmInlrprljLoiLDEsIiIsIiJdLFsi5p2+5rGf5Yy6Iiwi5p2+5rGf5Yy6IiwxLCIiLCIiXSxbIumHkeWxseWMuiIsIumHkeWxseWMuiIsMSwiIiwiIl0sWyLpnZLmtabljLoiLCLpnZLmtabljLoiLDEsIiIsIiJdLFsi5aWJ6LSk5Yy6Iiwi5aWJ6LSk5Yy6IiwxLCIiLCIiXSxbIua1puS4nOaWsOWMuiIsIua1puS4nOaWsOWMuiIsMSwiIiwiIl0sWyLltIfmmI7ljLoiLCLltIfmmI7ljLoiLDEsIiIsIiJdXSwiU2VsZWN0ZWRWYWx1ZUFycmF5IjpbIuWuneWxseWMuiJdfSwicDFfRmVuZ1hEUURMIjp7IkxhYmVsIjoiMTLmnIgwMeaXpeiHszEy5pyIMTXml6XmmK/lkKblnKjkuK3pq5jpo47pmanlnLDljLrpgJfnlZk8c3BhbiBzdHlsZT0nY29sb3I6cmVkOyc+77yI5YaF6JKZ5Y+k5ruh5rSy6YeM5Lic5bGx6KGX6YGT44CB5YyX5Yy66KGX6YGT5Yqe5LqL5aSE77yM5omO6LWJ6K+65bCU5Yy656ys5LiJ44CB56ys5Zub44CB56ys5LqU6KGX6YGT5Yqe5LqL5aSE77yM5oiQ6YO95biC6YOr6YO95Yy66YOr562S6KGX6YGT5aSq5bmz5p2R44CB6I+g6JCd56S+5Yy65Lit6ZOB5aWl57u05bCU5LqM5pyf44CB5LiJ5pyf44CB6YOr6YO95Yy65ZSQ5piM6ZWH5rC45a6J5p2ROOe7hOOAgeaIkOWNjuWMuuW0lOWutuW6l+WNjumDveS6keaZr+WPsOWwj+WMuu+8jOm7kem+meaxn+eJoeS4ueaxn+W4guS4nOWugeW4guS4reW/g+ekvuWMuuOAgee7peiKrOays+W4gumdkuS6keWwj+WMuu+8jOaWsOeWhuWQkOmygeeVquW4gue6ouebvuWwj+WMuu+8iTwvc3Bhbj4iLCJTZWxlY3RlZFZhbHVlIjoi5ZCmIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dfSwicDFfVG9uZ1pXRExIIjp7IkxhYmVsIjoi5LiK5rW35ZCM5L2P5Lq65ZGY5piv5ZCm5pyJMTLmnIgwMeaXpeiHszEy5pyIMTXml6XmnaXoh6rkuK3pq5jpo47pmanlnLDljLrnmoTkuro8c3BhbiBzdHlsZT0nY29sb3I6cmVkOyc+77yI5YaF6JKZ5Y+k5ruh5rSy6YeM5Lic5bGx6KGX6YGT44CB5YyX5Yy66KGX6YGT5Yqe5LqL5aSE77yM5omO6LWJ6K+65bCU5Yy656ys5LiJ44CB56ys5Zub44CB56ys5LqU6KGX6YGT5Yqe5LqL5aSE77yM5oiQ6YO95biC6YOr6YO95Yy66YOr562S6KGX6YGT5aSq5bmz5p2R44CB6I+g6JCd56S+5Yy65Lit6ZOB5aWl57u05bCU5LqM5pyf44CB5LiJ5pyf44CB6YOr6YO95Yy65ZSQ5piM6ZWH5rC45a6J5p2ROOe7hOOAgeaIkOWNjuWMuuW0lOWutuW6l+WNjumDveS6keaZr+WPsOWwj+WMuu+8jOm7kem+meaxn+eJoeS4ueaxn+W4guS4nOWugeW4guS4reW/g+ekvuWMuuOAgee7peiKrOays+W4gumdkuS6keWwj+WMuu+8jOaWsOeWhuWQkOmygeeVquW4gue6ouebvuWwj+WMuu+8iTwvc3Bhbj4iLCJTZWxlY3RlZFZhbHVlIjoi5ZCmIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dfSwicDFfWGlhbmdYRFoiOnsiVGV4dCI6IuaWsOagoeWMuuagoeWGhVMyIn0sInAxX1F1ZVpIWkpDIjp7IkZfSXRlbXMiOltbIuaYryIsIuaYryIsMSwiIiwiIl0sWyLlkKYiLCLlkKYiLDEsIiIsIiJdXSwiU2VsZWN0ZWRWYWx1ZUFycmF5IjpbIuWQpiJdfSwicDFfRGFuZ1JHTCI6eyJTZWxlY3RlZFZhbHVlIjoi5ZCmIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dfSwicDFfR2VMU00iOnsiSGlkZGVuIjp0cnVlLCJJRnJhbWVBdHRyaWJ1dGVzIjp7fX0sInAxX0dlTEZTIjp7IlJlcXVpcmVkIjpmYWxzZSwiSGlkZGVuIjp0cnVlLCJGX0l0ZW1zIjpbWyLlsYXlrrbpmpTnprsiLCLlsYXlrrbpmpTnprsiLDFdLFsi6ZuG5Lit6ZqU56a7Iiwi6ZuG5Lit6ZqU56a7IiwxXV0sIlNlbGVjdGVkVmFsdWUiOm51bGx9LCJwMV9HZUxEWiI6eyJIaWRkZW4iOnRydWV9LCJwMV9DZW5nRldIIjp7IkxhYmVsIjoiMTLmnIgwMeaXpeiHszEy5pyIMTXml6XmmK/lkKblnKjkuK3pq5jpo47pmanlnLDljLrpgJfnlZnov4c8c3BhbiBzdHlsZT0nY29sb3I6cmVkOyc+77yI5YaF6JKZ5Y+k5ruh5rSy6YeM5Lic5bGx6KGX6YGT44CB5YyX5Yy66KGX6YGT5Yqe5LqL5aSE77yM5omO6LWJ6K+65bCU5Yy656ys5LiJ44CB56ys5Zub44CB56ys5LqU6KGX6YGT5Yqe5LqL5aSE77yM5oiQ6YO95biC6YOr6YO95Yy66YOr562S6KGX6YGT5aSq5bmz5p2R44CB6I+g6JCd56S+5Yy65Lit6ZOB5aWl57u05bCU5LqM5pyf44CB5LiJ5pyf44CB6YOr6YO95Yy65ZSQ5piM6ZWH5rC45a6J5p2ROOe7hOOAgeaIkOWNjuWMuuW0lOWutuW6l+WNjumDveS6keaZr+WPsOWwj+WMuu+8jOm7kem+meaxn+eJoeS4ueaxn+W4guS4nOWugeW4guS4reW/g+ekvuWMuuOAgee7peiKrOays+W4gumdkuS6keWwj+WMuu+8jOaWsOeWhuWQkOmygeeVquW4gue6ouebvuWwj+WMuu+8iTwvc3Bhbj4iLCJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8iLDFdLFsi5ZCmIiwi5ZCmIiwxXV0sIlNlbGVjdGVkVmFsdWUiOiLlkKYifSwicDFfQ2VuZ0ZXSF9SaVFpIjp7IkhpZGRlbiI6dHJ1ZX0sInAxX0NlbmdGV0hfQmVpWmh1Ijp7IkhpZGRlbiI6dHJ1ZX0sInAxX0ppZUNodSI6eyJMYWJlbCI6IjEy5pyIMDHml6Xoh7MxMuaciDE15pel5piv5ZCm5LiO5p2l6Ieq5Lit6auY6aOO6Zmp5Zyw5Yy65Y+R54Ot5Lq65ZGY5a+G5YiH5o6l6KemPHNwYW4gc3R5bGU9J2NvbG9yOnJlZDsnPu+8iOWGheiSmeWPpOa7oea0sumHjOS4nOWxseihl+mBk+OAgeWMl+WMuuihl+mBk+WKnuS6i+WkhO+8jOaJjui1ieivuuWwlOWMuuesrOS4ieOAgeesrOWbm+OAgeesrOS6lOihl+mBk+WKnuS6i+WkhO+8jOaIkOmDveW4gumDq+mDveWMuumDq+etkuihl+mBk+WkquW5s+adkeOAgeiPoOiQneekvuWMuuS4remTgeWlpee7tOWwlOS6jOacn+OAgeS4ieacn+OAgemDq+mDveWMuuWUkOaYjOmVh+awuOWuieadkTjnu4TjgIHmiJDljY7ljLrltJTlrrblupfljY7pg73kupHmma/lj7DlsI/ljLrvvIzpu5HpvpnmsZ/niaHkuLnmsZ/luILkuJzlroHluILkuK3lv4PnpL7ljLrjgIHnu6XoiqzmsrPluILpnZLkupHlsI/ljLrvvIzmlrDnloblkJDpsoHnlarluILnuqLnm77lsI/ljLrvvIk8L3NwYW4+IiwiU2VsZWN0ZWRWYWx1ZSI6IuWQpiIsIkZfSXRlbXMiOltbIuaYryIsIuaYryIsMV0sWyLlkKYiLCLlkKYiLDFdXX0sInAxX0ppZUNodV9SaVFpIjp7IkhpZGRlbiI6dHJ1ZX0sInAxX0ppZUNodV9CZWlaaHUiOnsiSGlkZGVuIjp0cnVlfSwicDFfVHVKV0giOnsiTGFiZWwiOiIxMuaciDAx5pel6IezMTLmnIgxNeaXpeaYr+WQpuS5mOWdkOWFrOWFseS6pOmAmumAlOW+hOS4remrmOmjjumZqeWcsOWMujxzcGFuIHN0eWxlPSdjb2xvcjpyZWQ7Jz7vvIjlhoXokpnlj6Tmu6HmtLLph4zkuJzlsbHooZfpgZPjgIHljJfljLrooZfpgZPlip7kuovlpITvvIzmiY7otYnor7rlsJTljLrnrKzkuInjgIHnrKzlm5vjgIHnrKzkupTooZfpgZPlip7kuovlpITvvIzmiJDpg73luILpg6vpg73ljLrpg6vnrZLooZfpgZPlpKrlubPmnZHjgIHoj6DokJ3npL7ljLrkuK3pk4HlpaXnu7TlsJTkuozmnJ/jgIHkuInmnJ/jgIHpg6vpg73ljLrllJDmmIzplYfmsLjlronmnZE457uE44CB5oiQ5Y2O5Yy65bSU5a625bqX5Y2O6YO95LqR5pmv5Y+w5bCP5Yy677yM6buR6b6Z5rGf54mh5Li55rGf5biC5Lic5a6B5biC5Lit5b+D56S+5Yy644CB57ul6Iqs5rKz5biC6Z2S5LqR5bCP5Yy677yM5paw55aG5ZCQ6bKB55Wq5biC57qi55u+5bCP5Yy677yJPC9zcGFuPiIsIlNlbGVjdGVkVmFsdWUiOiLlkKYiLCJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8iLDFdLFsi5ZCmIiwi5ZCmIiwxXV19LCJwMV9UdUpXSF9SaVFpIjp7IkhpZGRlbiI6dHJ1ZX0sInAxX1R1SldIX0JlaVpodSI6eyJIaWRkZW4iOnRydWV9LCJwMV9KaWFSZW4iOnsiTGFiZWwiOiIxMuaciDAx5pel6IezMTLmnIgxNeaXpeWutuS6uuaYr+WQpuacieWPkeeDreetieeXh+eKtiJ9LCJwMV9KaWFSZW5fQmVpWmh1Ijp7IkhpZGRlbiI6dHJ1ZX0sInAxX1N1aVNNIjp7IlNlbGVjdGVkVmFsdWUiOiLnu7/oibIiLCJGX0l0ZW1zIjpbWyLnuqLoibIiLCLnuqLoibIiLDFdLFsi6buE6ImyIiwi6buE6ImyIiwxXSxbIue7v+iJsiIsIue7v+iJsiIsMV1dfSwicDFfTHZNYTE0RGF5cyI6eyJTZWxlY3RlZFZhbHVlIjoi5pivIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dfSwicDEiOnsiVGl0bGUiOiLmr4/ml6XkuKTmiqXvvIjkuIvljYjvvIkiLCJJRnJhbWVBdHRyaWJ1dGVzIjp7fX19'
        }

        async with session.post(url='https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx', headers=headers ,params=params, data=data,proxy=self.proxy) as response:
            html = await response.text()
            status_code = response.status  
            print('Referer:', headers['Referer'], end=f'[{status_code}]')
            # print(html)
            res = self.res_find.search(html)
            if res:
                print(res[1])
            else:
                raise HTTPError('AsyncPost Error.')

    def asyncPost(self, urls: List[Tuple[str, str]]):
        async def run():
            cookies = self._cookie
            async with ClientSession(cookies=cookies) as session:
                tasks = [asyncio.create_task(self.async_report(
                    session=session, date=url[0], state=url[1])) for url in urls]
                await asyncio.gather(*tasks)
        asyncio.run(run())


class DayReportPost(PostRequest):
    
    def report(self, date: str, state: str=None, filelog=False):
        cookies = self._cookie
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'text/plain, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'X-FineUI-Ajax': 'true',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://selfreport.shu.edu.cn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://selfreport.shu.edu.cn/DayReport.aspx',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }
        
        data = {
            '__EVENTTARGET': 'p1$ctl00$btnSubmit',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.viewstate,
            '__VIEWSTATEGENERATOR': '7AD7E509',
            'p1$ChengNuo': 'p1_ChengNuo',
            'p1$BaoSRQ': date,
            'p1$DangQSTZK': '\u826F\u597D',
            'p1$TiWen': '',
            'p1$JiuYe_ShouJHM': '',
            'p1$JiuYe_Email': '',
            'p1$JiuYe_Wechat': '',
            'p1$QiuZZT': '',
            'p1$JiuYKN': '',
            'p1$JiuYSJ': '',
            'p1$ZaiXiao': '\u4E0D\u5728\u6821',
            'p1$MingTDX': '\u4E0D\u5230\u6821',
            'p1$MingTJC': '\u5426',
            'p1$BanChe_1$Value': '0',
            'p1$BanChe_1': '\u4E0D\u9700\u8981\u4E58\u73ED\u8F66',
            'p1$BanChe_2$Value': '0',
            'p1$BanChe_2': '\u4E0D\u9700\u8981\u4E58\u73ED\u8F66',
            'p1$GuoNei': '\u56FD\u5185',
            'p1$ddlGuoJia$Value': '-1',
            'p1$ddlGuoJia': '\u9009\u62E9\u56FD\u5BB6',
            'p1$ShiFSH': '\u5426',
            'p1$ddlSheng$Value': '\u8D35\u5DDE',
            'p1$ddlSheng': '\u8D35\u5DDE',
            'p1$ddlShi$Value': '\u8D35\u9633\u5E02',
            'p1$ddlShi': '\u8D35\u9633\u5E02',
            'p1$ddlXian$Value': '\u5357\u660E\u533A',
            'p1$ddlXian': '\u5357\u660E\u533A',
            'p1$XiangXDZ': '\u82B1\u679C\u56EDr2\u533A4\u680B',
            'p1$FengXDQDL': '\u5426',
            'p1$CengFWH': '\u5426',
            'p1$CengFWH_RiQi': '',
            'p1$CengFWH_BeiZhu': '',
            'p1$JieChu': '\u5426',
            'p1$JieChu_RiQi': '',
            'p1$JieChu_BeiZhu': '',
            'p1$TuJWH': '\u5426',
            'p1$TuJWH_RiQi': '',
            'p1$TuJWH_BeiZhu': '',
            'p1$QueZHZJC$Value': '\u5426',
            'p1$QueZHZJC': '\u5426',
            'p1$DangRGL': '\u5426',
            'p1$GeLDZ': '',
            'p1$FanXRQ': '',
            'p1$WeiFHYY': '',
            'p1$ShangHJZD': '',
            'p1$DaoXQLYGJ': '\u4E2D\u56FD',
            'p1$DaoXQLYCS': '\u8D35\u9633',
            'p1$JiaRen_BeiZhu': '',
            'p1$SuiSM': '\u7EFF\u8272',
            'p1$LvMa14Days': '\u662F',
            'p1$Address2': '',
            'p1_ContentPanel1_Collapsed': 'true',
            'p1_GeLSM_Collapsed': 'false',
            'p1_Collapsed': 'false',
            'F_STATE': 'eyJwMV9CYW9TUlEiOnsiVGV4dCI6IjIwMjEtMDEtMjUifSwicDFfRGFuZ1FTVFpLIjp7IkZfSXRlbXMiOltbIuiJr+WlvSIsIuiJr+Wlve+8iOS9k+a4qeS4jemrmOS6jjM3LjPvvIkiLDFdLFsi5LiN6YCCIiwi5LiN6YCCIiwxXV0sIlNlbGVjdGVkVmFsdWUiOiLoia/lpb0ifSwicDFfWmhlbmdaaHVhbmciOnsiSGlkZGVuIjp0cnVlLCJGX0l0ZW1zIjpbWyLmhJ/lhpIiLCLmhJ/lhpIiLDFdLFsi5ZKz5Ze9Iiwi5ZKz5Ze9IiwxXSxbIuWPkeeDrSIsIuWPkeeDrSIsMV1dLCJTZWxlY3RlZFZhbHVlQXJyYXkiOltdfSwicDFfUWl1WlpUIjp7IkZfSXRlbXMiOltdLCJTZWxlY3RlZFZhbHVlQXJyYXkiOltdfSwicDFfSml1WUtOIjp7IkZfSXRlbXMiOltdLCJTZWxlY3RlZFZhbHVlQXJyYXkiOltdfSwicDFfSml1WVlYIjp7IlJlcXVpcmVkIjpmYWxzZSwiRl9JdGVtcyI6W10sIlNlbGVjdGVkVmFsdWVBcnJheSI6W119LCJwMV9KaXVZWkQiOnsiRl9JdGVtcyI6W10sIlNlbGVjdGVkVmFsdWVBcnJheSI6W119LCJwMV9KaXVZWkwiOnsiRl9JdGVtcyI6W10sIlNlbGVjdGVkVmFsdWVBcnJheSI6W119LCJwMV9aYWlYaWFvIjp7IlNlbGVjdGVkVmFsdWUiOiLkuI3lnKjmoKEiLCJGX0l0ZW1zIjpbWyLkuI3lnKjmoKEiLCLkuI3lnKjmoKEiLDFdLFsi5a6d5bGxIiwi5a6d5bGx5qCh5Yy6IiwxXSxbIuW7tumVvyIsIuW7tumVv+agoeWMuiIsMV0sWyLlmInlrpoiLCLlmInlrprmoKHljLoiLDFdLFsi5paw6Ze46LevIiwi5paw6Ze46Lev5qCh5Yy6IiwxXV19LCJwMV9NaW5nVERYIjp7IlNlbGVjdGVkVmFsdWUiOiLkuI3liLDmoKEiLCJGX0l0ZW1zIjpbWyLkuI3liLDmoKEiLCLkuI3liLDmoKEiLDFdLFsi5a6d5bGxIiwi5a6d5bGx5qCh5Yy6IiwxXSxbIuW7tumVvyIsIuW7tumVv+agoeWMuiIsMV0sWyLlmInlrpoiLCLlmInlrprmoKHljLoiLDFdLFsi5paw6Ze46LevIiwi5paw6Ze46Lev5qCh5Yy6IiwxXV19LCJwMV9NaW5nVEpDIjp7IlJlcXVpcmVkIjp0cnVlLCJTZWxlY3RlZFZhbHVlIjoi5ZCmIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dLCJIaWRkZW4iOnRydWV9LCJwMV9CYW5DaGVfMSI6eyJGX0l0ZW1zIjpbWyIwIiwi5LiN6ZyA6KaB5LmY54+t6L2mIiwxLCIiLCIiXSxbIjEiLCIx5Y+357q/77ya5ZiJ5a6a5qCh5Yy65Y2X6ZeoPT7lrp3lsbHmoKHljLoiLDEsIiIsIiJdLFsiMiIsIjLlj7fnur/vvJrlrp3lsbHmoKHljLo9PuWYieWumuagoeWMuuWNl+mXqCIsMSwiIiwiIl0sWyIzIiwiM+WPt+e6v++8muW7tumVv+agoeWMuuWMl+mXqD0+5a6d5bGx5qCh5Yy6IiwxLCIiLCIiXSxbIjQiLCI05Y+357q/77ya5a6d5bGx5qCh5Yy6PT7lu7bplb/moKHljLrljJfpl6giLDEsIiIsIiJdLFsiNSIsIjXlj7fnur/vvJrlmInlrprmoKHljLrljZfpl6g9PuW7tumVv+agoeWMuuWMl+mXqCIsMSwiIiwiIl0sWyI2IiwiNuWPt+e6v++8muW7tumVv+agoeWMuuWMl+mXqD0+5ZiJ5a6a5qCh5Yy65Y2X6ZeoIiwxLCIiLCIiXV0sIlNlbGVjdGVkVmFsdWVBcnJheSI6WyIwIl0sIkhpZGRlbiI6dHJ1ZX0sInAxX0JhbkNoZV8yIjp7IkZfSXRlbXMiOltbIjAiLCLkuI3pnIDopoHkuZjnj63ovaYiLDEsIiIsIiJdLFsiMSIsIjHlj7fnur/vvJrlmInlrprmoKHljLrljZfpl6g9PuWuneWxseagoeWMuiIsMSwiIiwiIl0sWyIyIiwiMuWPt+e6v++8muWuneWxseagoeWMuj0+5ZiJ5a6a5qCh5Yy65Y2X6ZeoIiwxLCIiLCIiXSxbIjMiLCIz5Y+357q/77ya5bu26ZW/5qCh5Yy65YyX6ZeoPT7lrp3lsbHmoKHljLoiLDEsIiIsIiJdLFsiNCIsIjTlj7fnur/vvJrlrp3lsbHmoKHljLo9PuW7tumVv+agoeWMuuWMl+mXqCIsMSwiIiwiIl0sWyI1IiwiNeWPt+e6v++8muWYieWumuagoeWMuuWNl+mXqD0+5bu26ZW/5qCh5Yy65YyX6ZeoIiwxLCIiLCIiXSxbIjYiLCI25Y+357q/77ya5bu26ZW/5qCh5Yy65YyX6ZeoPT7lmInlrprmoKHljLrljZfpl6giLDEsIiIsIiJdXSwiU2VsZWN0ZWRWYWx1ZUFycmF5IjpbIjAiXSwiSGlkZGVuIjp0cnVlfSwicDFfR3VvTmVpIjp7IkZfSXRlbXMiOltbIuWbveWGhSIsIuWbveWGhSIsMV0sWyLlm73lpJYiLCLlm73lpJYiLDFdXSwiU2VsZWN0ZWRWYWx1ZSI6IuWbveWGhSJ9LCJwMV9kZGxHdW9KaWEiOnsiRGF0YVRleHRGaWVsZCI6Ilpob25nV2VuIiwiRGF0YVZhbHVlRmllbGQiOiJaaG9uZ1dlbiIsIkZfSXRlbXMiOltbIi0xIiwi6YCJ5oup5Zu95a62IiwxLCIiLCIiXSxbIumYv+WwlOW3tOWwvOS6miIsIumYv+WwlOW3tOWwvOS6miIsMSwiIiwiIl0sWyLpmL/lsJTlj4rliKnkupoiLCLpmL/lsJTlj4rliKnkupoiLDEsIiIsIiJdLFsi6Zi/5a+M5rGXIiwi6Zi/5a+M5rGXIiwxLCIiLCIiXSxbIumYv+agueW7tyIsIumYv+agueW7tyIsMSwiIiwiIl0sWyLpmL/mi4nkvK/ogZTlkIjphYvplb/lm70iLCLpmL/mi4nkvK/ogZTlkIjphYvplb/lm70iLDEsIiIsIiJdLFsi6Zi/6bKB5be0Iiwi6Zi/6bKB5be0IiwxLCIiLCIiXSxbIumYv+abvCIsIumYv+abvCIsMSwiIiwiIl0sWyLpmL/loZ7mi5znloYiLCLpmL/loZ7mi5znloYiLDEsIiIsIiJdLFsi5Z+D5Y+KIiwi5Z+D5Y+KIiwxLCIiLCIiXSxbIuWfg+WhnuS/hOavlOS6miIsIuWfg+WhnuS/hOavlOS6miIsMSwiIiwiIl0sWyLniLHlsJTlhbAiLCLniLHlsJTlhbAiLDEsIiIsIiJdLFsi54ix5rKZ5bC85LqaIiwi54ix5rKZ5bC85LqaIiwxLCIiLCIiXSxbIuWuiemBk+WwlCIsIuWuiemBk+WwlCIsMSwiIiwiIl0sWyLlronlk6Xmi4kiLCLlronlk6Xmi4kiLDEsIiIsIiJdLFsi5a6J5Zyt5ouJIiwi5a6J5Zyt5ouJIiwxLCIiLCIiXSxbIuWuieaPkOeTnOWSjOW3tOW4g+i+viIsIuWuieaPkOeTnOWSjOW3tOW4g+i+viIsMSwiIiwiIl0sWyLlpaXlnLDliKkiLCLlpaXlnLDliKkiLDEsIiIsIiJdLFsi5aWl5YWw576k5bKbIiwi5aWl5YWw576k5bKbIiwxLCIiLCIiXSxbIua+s+Wkp+WIqeS6miIsIua+s+Wkp+WIqeS6miIsMSwiIiwiIl0sWyLlt7Tlt7TlpJrmlq8iLCLlt7Tlt7TlpJrmlq8iLDEsIiIsIiJdLFsi5be05biD5Lqa5paw5Yeg5YaF5LqaIiwi5be05biD5Lqa5paw5Yeg5YaF5LqaIiwxLCIiLCIiXSxbIuW3tOWTiOmprCIsIuW3tOWTiOmprCIsMSwiIiwiIl0sWyLlt7Tln7rmlq/lnaYiLCLlt7Tln7rmlq/lnaYiLDEsIiIsIiJdLFsi5be05YuS5pav5Z2mIiwi5be05YuS5pav5Z2mIiwxLCIiLCIiXSxbIuW3tOaelyIsIuW3tOaelyIsMSwiIiwiIl0sWyLlt7Tmi7/pqawiLCLlt7Tmi7/pqawiLDEsIiIsIiJdLFsi5be06KW/Iiwi5be06KW/IiwxLCIiLCIiXSxbIueZveS/hOe9l+aWryIsIueZveS/hOe9l+aWryIsMSwiIiwiIl0sWyLnmb7mhZXlpKciLCLnmb7mhZXlpKciLDEsIiIsIiJdLFsi5L+d5Yqg5Yip5LqaIiwi5L+d5Yqg5Yip5LqaIiwxLCIiLCIiXSxbIui0neWugSIsIui0neWugSIsMSwiIiwiIl0sWyLmr5TliKnml7YiLCLmr5TliKnml7YiLDEsIiIsIiJdLFsi5Yaw5bKbIiwi5Yaw5bKbIiwxLCIiLCIiXSxbIuazouWkmum7juWQhCIsIuazouWkmum7juWQhCIsMSwiIiwiIl0sWyLms6LlhbAiLCLms6LlhbAiLDEsIiIsIiJdLFsi5rOi5pav5bC85Lqa5ZKM6buR5aGe5ZOl57u06YKjIiwi5rOi5pav5bC85Lqa5ZKM6buR5aGe5ZOl57u06YKjIiwxLCIiLCIiXSxbIueOu+WIqee7tOS6miIsIueOu+WIqee7tOS6miIsMSwiIiwiIl0sWyLkvK/liKnlhbkiLCLkvK/liKnlhbkiLDEsIiIsIiJdLFsi5Y2a6Iyo55Om57qzIiwi5Y2a6Iyo55Om57qzIiwxLCIiLCIiXSxbIuS4jeS4uSIsIuS4jeS4uSIsMSwiIiwiIl0sWyLluIPln7rnurPms5XntKIiLCLluIPln7rnurPms5XntKIiLDEsIiIsIiJdLFsi5biD6ZqG6L+qIiwi5biD6ZqG6L+qIiwxLCIiLCIiXSxbIuW4g+e7tOWymyIsIuW4g+e7tOWymyIsMSwiIiwiIl0sWyLmnJ3pspwiLCLmnJ3pspwiLDEsIiIsIiJdLFsi6LWk6YGT5Yeg5YaF5LqaIiwi6LWk6YGT5Yeg5YaF5LqaIiwxLCIiLCIiXSxbIuS4uem6piIsIuS4uem6piIsMSwiIiwiIl0sWyLlvrflm70iLCLlvrflm70iLDEsIiIsIiJdLFsi5Lic5bid5rG2Iiwi5Lic5bid5rG2IiwxLCIiLCIiXSxbIuS4nOW4neaxtiIsIuS4nOW4neaxtiIsMSwiIiwiIl0sWyLlpJrlk6UiLCLlpJrlk6UiLDEsIiIsIiJdLFsi5aSa57Gz5bC85YqgIiwi5aSa57Gz5bC85YqgIiwxLCIiLCIiXSxbIuS/hOe9l+aWr+iBlOmCpiIsIuS/hOe9l+aWr+iBlOmCpiIsMSwiIiwiIl0sWyLljoTnk5zlpJrlsJQiLCLljoTnk5zlpJrlsJQiLDEsIiIsIiJdLFsi5Y6E56uL54m56YeM5LqaIiwi5Y6E56uL54m56YeM5LqaIiwxLCIiLCIiXSxbIuazleWbvSIsIuazleWbvSIsMSwiIiwiIl0sWyLms5Xlm73lpKfpg73kvJoiLCLms5Xlm73lpKfpg73kvJoiLDEsIiIsIiJdLFsi5rOV572X576k5bKbIiwi5rOV572X576k5bKbIiwxLCIiLCIiXSxbIuazleWxnuazouWIqeWwvOilv+S6miIsIuazleWxnuazouWIqeWwvOilv+S6miIsMSwiIiwiIl0sWyLms5XlsZ7lnK3kuprpgqMiLCLms5XlsZ7lnK3kuprpgqMiLDEsIiIsIiJdLFsi5qK16JKC5YaIIiwi5qK16JKC5YaIIiwxLCIiLCIiXSxbIuiPsuW+i+WuviIsIuiPsuW+i+WuviIsMSwiIiwiIl0sWyLmlpDmtY4iLCLmlpDmtY4iLDEsIiIsIiJdLFsi6Iqs5YWwIiwi6Iqs5YWwIiwxLCIiLCIiXSxbIuS9m+W+l+inkiIsIuS9m+W+l+inkiIsMSwiIiwiIl0sWyLlhojmr5TkupoiLCLlhojmr5TkupoiLDEsIiIsIiJdLFsi5Yia5p6cIiwi5Yia5p6cIiwxLCIiLCIiXSxbIuWImuaenO+8iOmHke+8iSIsIuWImuaenO+8iOmHke+8iSIsMSwiIiwiIl0sWyLlk6XkvKbmr5TkupoiLCLlk6XkvKbmr5TkupoiLDEsIiIsIiJdLFsi5ZOl5pav6L6+6buO5YqgIiwi5ZOl5pav6L6+6buO5YqgIiwxLCIiLCIiXSxbIuagvOael+e6s+i+viIsIuagvOael+e6s+i+viIsMSwiIiwiIl0sWyLmoLzpsoHlkInkupoiLCLmoLzpsoHlkInkupoiLDEsIiIsIiJdLFsi5qC56KW/5bKbIiwi5qC56KW/5bKbIiwxLCIiLCIiXSxbIuWPpOW3tCIsIuWPpOW3tCIsMSwiIiwiIl0sWyLnk5zlvrfnvZfmma7lspsiLCLnk5zlvrfnvZfmma7lspsiLDEsIiIsIiJdLFsi5YWz5bKbIiwi5YWz5bKbIiwxLCIiLCIiXSxbIuWcreS6mumCoyIsIuWcreS6mumCoyIsMSwiIiwiIl0sWyLlk4jokKjlhYvmlq/lnaYiLCLlk4jokKjlhYvmlq/lnaYiLDEsIiIsIiJdLFsi5rW35ZywIiwi5rW35ZywIiwxLCIiLCIiXSxbIumfqeWbvSIsIumfqeWbvSIsMSwiIiwiIl0sWyLojbflhbAiLCLojbflhbAiLDEsIiIsIiJdLFsi6buR5bGxIiwi6buR5bGxIiwxLCIiLCIiXSxbIua0qumDveaLieaWryIsIua0qumDveaLieaWryIsMSwiIiwiIl0sWyLln7rph4zlt7Tmlq8iLCLln7rph4zlt7Tmlq8iLDEsIiIsIiJdLFsi5ZCJ5biD5o+QIiwi5ZCJ5biD5o+QIiwxLCIiLCIiXSxbIuWQieWwlOWQieaWr+aWr+WdpiIsIuWQieWwlOWQieaWr+aWr+WdpiIsMSwiIiwiIl0sWyLlh6DlhoXkupoiLCLlh6DlhoXkupoiLDEsIiIsIiJdLFsi5Yeg5YaF5Lqa5q+U57uNIiwi5Yeg5YaF5Lqa5q+U57uNIiwxLCIiLCIiXSxbIuWKoOaLv+WkpyIsIuWKoOaLv+WkpyIsMSwiIiwiIl0sWyLliqDnurMiLCLliqDnurMiLDEsIiIsIiJdLFsi5Yqg6JOsIiwi5Yqg6JOsIiwxLCIiLCIiXSxbIuafrOWflOWvqCIsIuafrOWflOWvqCIsMSwiIiwiIl0sWyLmjbflhYsiLCLmjbflhYsiLDEsIiIsIiJdLFsi5rSl5be05biD6Z+mIiwi5rSl5be05biD6Z+mIiwxLCIiLCIiXSxbIuWWgOm6pumahiIsIuWWgOm6pumahiIsMSwiIiwiIl0sWyLljaHloZTlsJQiLCLljaHloZTlsJQiLDEsIiIsIiJdLFsi56eR56eR5pav77yI5Z+65p6X77yJ576k5bKbIiwi56eR56eR5pav77yI5Z+65p6X77yJ576k5bKbIiwxLCIiLCIiXSxbIuenkeaRqee9lyIsIuenkeaRqee9lyIsMSwiIiwiIl0sWyLnp5Hnibnov6rnk6YiLCLnp5Hnibnov6rnk6YiLDEsIiIsIiJdLFsi56eR5aiB54m5Iiwi56eR5aiB54m5IiwxLCIiLCIiXSxbIuWFi+e9l+WcsOS6miIsIuWFi+e9l+WcsOS6miIsMSwiIiwiIl0sWyLogq/lsLzkupoiLCLogq/lsLzkupoiLDEsIiIsIiJdLFsi5bqT5YWL576k5bKbIiwi5bqT5YWL576k5bKbIiwxLCIiLCIiXSxbIuaLieiEsee7tOS6miIsIuaLieiEsee7tOS6miIsMSwiIiwiIl0sWyLojrHntKLmiZgiLCLojrHntKLmiZgiLDEsIiIsIiJdLFsi6ICB5oydIiwi6ICB5oydIiwxLCIiLCIiXSxbIum7juW3tOWrqSIsIum7juW3tOWrqSIsMSwiIiwiIl0sWyLnq4vpmbblrpsiLCLnq4vpmbblrpsiLDEsIiIsIiJdLFsi5Yip5q+U6YeM5LqaIiwi5Yip5q+U6YeM5LqaIiwxLCIiLCIiXSxbIuWIqeavlOS6miIsIuWIqeavlOS6miIsMSwiIiwiIl0sWyLliJfmlK/mlablo6vnmbsiLCLliJfmlK/mlablo6vnmbsiLDEsIiIsIiJdLFsi55WZ5bC85rGq5bKbIiwi55WZ5bC85rGq5bKbIiwxLCIiLCIiXSxbIuWNouajruWgoSIsIuWNouajruWgoSIsMSwiIiwiIl0sWyLljaLml7rovr4iLCLljaLml7rovr4iLDEsIiIsIiJdLFsi572X6ams5bC85LqaIiwi572X6ams5bC85LqaIiwxLCIiLCIiXSxbIumprOi+vuWKoOaWr+WKoCIsIumprOi+vuWKoOaWr+WKoCIsMSwiIiwiIl0sWyLpqazmganlspsiLCLpqazmganlspsiLDEsIiIsIiJdLFsi6ams5bCU5Luj5aSrIiwi6ams5bCU5Luj5aSrIiwxLCIiLCIiXSxbIumprOiAs+S7liIsIumprOiAs+S7liIsMSwiIiwiIl0sWyLpqazmi4nnu7QiLCLpqazmi4nnu7QiLDEsIiIsIiJdLFsi6ams5p2l6KW/5LqaIiwi6ams5p2l6KW/5LqaIiwxLCIiLCIiXSxbIumprOmHjCIsIumprOmHjCIsMSwiIiwiIl0sWyLpqazlhbbpob8iLCLpqazlhbbpob8iLDEsIiIsIiJdLFsi6ams57uN5bCU576k5bKbIiwi6ams57uN5bCU576k5bKbIiwxLCIiLCIiXSxbIumprOaPkOWwvOWFi+WymyIsIumprOaPkOWwvOWFi+WymyIsMSwiIiwiIl0sWyLpqaznuqbnibkiLCLpqaznuqbnibkiLDEsIiIsIiJdLFsi5q+b6YeM5rGC5pavIiwi5q+b6YeM5rGC5pavIiwxLCIiLCIiXSxbIuavm+mHjOWhlOWwvOS6miIsIuavm+mHjOWhlOWwvOS6miIsMSwiIiwiIl0sWyLnvo7lm70iLCLnvo7lm70iLDEsIiIsIiJdLFsi576O5bGe6JCo5pGp5LqaIiwi576O5bGe6JCo5pGp5LqaIiwxLCIiLCIiXSxbIuiSmeWPpCIsIuiSmeWPpCIsMSwiIiwiIl0sWyLokpnnibnloZ7mi4nnibkiLCLokpnnibnloZ7mi4nnibkiLDEsIiIsIiJdLFsi5a2f5Yqg5ouJIiwi5a2f5Yqg5ouJIiwxLCIiLCIiXSxbIuenmOmygSIsIuenmOmygSIsMSwiIiwiIl0sWyLlr4blhYvnvZflsLzopb/kupoiLCLlr4blhYvnvZflsLzopb/kupoiLDEsIiIsIiJdLFsi57yF55S4Iiwi57yF55S4IiwxLCIiLCIiXSxbIuaRqeWwlOWkmueTpiIsIuaRqeWwlOWkmueTpiIsMSwiIiwiIl0sWyLmkanmtJvlk6UiLCLmkanmtJvlk6UiLDEsIiIsIiJdLFsi5pGp57qz5ZOlIiwi5pGp57qz5ZOlIiwxLCIiLCIiXSxbIuiOq+ahkeavlOWFiyIsIuiOq+ahkeavlOWFiyIsMSwiIiwiIl0sWyLloqjopb/lk6UiLCLloqjopb/lk6UiLDEsIiIsIiJdLFsi57qz57Gz5q+U5LqaIiwi57qz57Gz5q+U5LqaIiwxLCIiLCIiXSxbIuWNl+mdniIsIuWNl+mdniIsMSwiIiwiIl0sWyLljZfmlq/mi4nlpKsiLCLljZfmlq/mi4nlpKsiLDEsIiIsIiJdLFsi55GZ6bKBIiwi55GZ6bKBIiwxLCIiLCIiXSxbIuWwvOaziuWwlCIsIuWwvOaziuWwlCIsMSwiIiwiIl0sWyLlsLzliqDmi4nnk5wiLCLlsLzliqDmi4nnk5wiLDEsIiIsIiJdLFsi5bC85pel5bCUIiwi5bC85pel5bCUIiwxLCIiLCIiXSxbIuWwvOaXpeWIqeS6miIsIuWwvOaXpeWIqeS6miIsMSwiIiwiIl0sWyLnur3ln4MiLCLnur3ln4MiLDEsIiIsIiJdLFsi5oyq5aiBIiwi5oyq5aiBIiwxLCIiLCIiXSxbIuivuuemj+WFi+WymyIsIuivuuemj+WFi+WymyIsMSwiIiwiIl0sWyLluJXlirMiLCLluJXlirMiLDEsIiIsIiJdLFsi55qu54m55Yev5oGp576k5bKbIiwi55qu54m55Yev5oGp576k5bKbIiwxLCIiLCIiXSxbIuiRoeiQhOeJmSIsIuiRoeiQhOeJmSIsMSwiIiwiIl0sWyLml6XmnKwiLCLml6XmnKwiLDEsIiIsIiJdLFsi55Ge5YW4Iiwi55Ge5YW4IiwxLCIiLCIiXSxbIueRnuWjqyIsIueRnuWjqyIsMSwiIiwiIl0sWyLokKjlsJTnk6blpJoiLCLokKjlsJTnk6blpJoiLDEsIiIsIiJdLFsi6JCo5pGp5LqaIiwi6JCo5pGp5LqaIiwxLCIiLCIiXSxbIuWhnuWwlOe7tOS6miIsIuWhnuWwlOe7tOS6miIsMSwiIiwiIl0sWyLloZ7mi4nliKnmmIIiLCLloZ7mi4nliKnmmIIiLDEsIiIsIiJdLFsi5aGe5YaF5Yqg5bCUIiwi5aGe5YaF5Yqg5bCUIiwxLCIiLCIiXSxbIuWhnua1pui3r+aWryIsIuWhnua1pui3r+aWryIsMSwiIiwiIl0sWyLloZ7oiIzlsJQiLCLloZ7oiIzlsJQiLDEsIiIsIiJdLFsi5rKZ54m56Zi/5ouJ5LyvIiwi5rKZ54m56Zi/5ouJ5LyvIiwxLCIiLCIiXSxbIuWco+ivnuWymyIsIuWco+ivnuWymyIsMSwiIiwiIl0sWyLlnKPlpJrnvo7lkozmma7mnpfopb/mr5QiLCLlnKPlpJrnvo7lkozmma7mnpfopb/mr5QiLDEsIiIsIiJdLFsi5Zyj6LWr5YuS5ou/Iiwi5Zyj6LWr5YuS5ou/IiwxLCIiLCIiXSxbIuWco+WfuuiMqOWSjOWwvOe7tOaWryIsIuWco+WfuuiMqOWSjOWwvOe7tOaWryIsMSwiIiwiIl0sWyLlnKPljaLopb/kupoiLCLlnKPljaLopb/kupoiLDEsIiIsIiJdLFsi5Zyj6ams5Yqb6K+6Iiwi5Zyj6ams5Yqb6K+6IiwxLCIiLCIiXSxbIuWco+aWh+ajrueJueWSjOagvOael+e6s+S4geaWryIsIuWco+aWh+ajrueJueWSjOagvOael+e6s+S4geaWryIsMSwiIiwiIl0sWyLmlq/ph4zlhbDljaEiLCLmlq/ph4zlhbDljaEiLDEsIiIsIiJdLFsi5pav5rSb5LyQ5YWLIiwi5pav5rSb5LyQ5YWLIiwxLCIiLCIiXSxbIuaWr+a0m+aWh+WwvOS6miIsIuaWr+a0m+aWh+WwvOS6miIsMSwiIiwiIl0sWyLmlq/lqIHlo6vlhbAiLCLmlq/lqIHlo6vlhbAiLDEsIiIsIiJdLFsi6IuP5Li5Iiwi6IuP5Li5IiwxLCIiLCIiXSxbIuiLj+mHjOWNlyIsIuiLj+mHjOWNlyIsMSwiIiwiIl0sWyLmiYDnvZfpl6jnvqTlspsiLCLmiYDnvZfpl6jnvqTlspsiLDEsIiIsIiJdLFsi57Si6ams6YeMIiwi57Si6ams6YeMIiwxLCIiLCIiXSxbIuWhlOWQieWFi+aWr+WdpiIsIuWhlOWQieWFi+aWr+WdpiIsMSwiIiwiIl0sWyLms7Dlm70iLCLms7Dlm70iLDEsIiIsIiJdLFsi5Z2m5qGR5bC85LqaIiwi5Z2m5qGR5bC85LqaIiwxLCIiLCIiXSxbIuaxpOWKoCIsIuaxpOWKoCIsMSwiIiwiIl0sWyLnibnnq4vlsLzovr7lkozlpJrlt7Tlk6UiLCLnibnnq4vlsLzovr7lkozlpJrlt7Tlk6UiLDEsIiIsIiJdLFsi56qB5bC85pavIiwi56qB5bC85pavIiwxLCIiLCIiXSxbIuWbvueTpuWNoiIsIuWbvueTpuWNoiIsMSwiIiwiIl0sWyLlnJ/ogLPlhbYiLCLlnJ/ogLPlhbYiLDEsIiIsIiJdLFsi5Zyf5bqT5pu85pav5Z2mIiwi5Zyf5bqT5pu85pav5Z2mIiwxLCIiLCIiXSxbIuaJmOWFi+WKsyIsIuaJmOWFi+WKsyIsMSwiIiwiIl0sWyLnk6bliKnmlq/nvqTlspvlkozlr4zlm77nurPnvqTlspsiLCLnk6bliKnmlq/nvqTlspvlkozlr4zlm77nurPnvqTlspsiLDEsIiIsIiJdLFsi55Om5Yqq6Zi/5Zu+Iiwi55Om5Yqq6Zi/5Zu+IiwxLCIiLCIiXSxbIuWNseWcsOmprOaLiSIsIuWNseWcsOmprOaLiSIsMSwiIiwiIl0sWyLlp5TlhoXnkZ7mi4kiLCLlp5TlhoXnkZ7mi4kiLDEsIiIsIiJdLFsi5paH6I6xIiwi5paH6I6xIiwxLCIiLCIiXSxbIuS5jOW5sui+viIsIuS5jOW5sui+viIsMSwiIiwiIl0sWyLkuYzlhYvlhbAiLCLkuYzlhYvlhbAiLDEsIiIsIiJdLFsi5LmM5ouJ5ZytIiwi5LmM5ouJ5ZytIiwxLCIiLCIiXSxbIuS5jOWFueWIq+WFi+aWr+WdpiIsIuS5jOWFueWIq+WFi+aWr+WdpiIsMSwiIiwiIl0sWyLopb/nj63niZkiLCLopb/nj63niZkiLDEsIiIsIiJdLFsi6KW/5pKS5ZOI5ouJIiwi6KW/5pKS5ZOI5ouJIiwxLCIiLCIiXSxbIuW4jOiFiiIsIuW4jOiFiiIsMSwiIiwiIl0sWyLmlrDliqDlnaEiLCLmlrDliqDlnaEiLDEsIiIsIiJdLFsi5paw5ZaA6YeM5aSa5bC85LqaIiwi5paw5ZaA6YeM5aSa5bC85LqaIiwxLCIiLCIiXSxbIuaWsOilv+WFsCIsIuaWsOilv+WFsCIsMSwiIiwiIl0sWyLljIjniZnliKkiLCLljIjniZnliKkiLDEsIiIsIiJdLFsi5Y+Z5Yip5LqaIiwi5Y+Z5Yip5LqaIiwxLCIiLCIiXSxbIueJmeS5sOWKoCIsIueJmeS5sOWKoCIsMSwiIiwiIl0sWyLkuprnvo7lsLzkupoiLCLkuprnvo7lsLzkupoiLDEsIiIsIiJdLFsi5Lmf6ZeoIiwi5Lmf6ZeoIiwxLCIiLCIiXSxbIuS8iuaLieWFiyIsIuS8iuaLieWFiyIsMSwiIiwiIl0sWyLkvIrmnJciLCLkvIrmnJciLDEsIiIsIiJdLFsi5Lul6Imy5YiXIiwi5Lul6Imy5YiXIiwxLCIiLCIiXSxbIuaEj+Wkp+WIqSIsIuaEj+Wkp+WIqSIsMSwiIiwiIl0sWyLljbDluqYiLCLljbDluqYiLDEsIiIsIiJdLFsi5Y2w5bqm5bC86KW/5LqaIiwi5Y2w5bqm5bC86KW/5LqaIiwxLCIiLCIiXSxbIuiLseWbvSIsIuiLseWbvSIsMSwiIiwiIl0sWyLnuqbml6YiLCLnuqbml6YiLDEsIiIsIiJdLFsi6LaK5Y2XIiwi6LaK5Y2XIiwxLCIiLCIiXSxbIui1nuavlOS6miIsIui1nuavlOS6miIsMSwiIiwiIl0sWyLms73opb/lspsiLCLms73opb/lspsiLDEsIiIsIiJdLFsi5LmN5b6XIiwi5LmN5b6XIiwxLCIiLCIiXSxbIuebtOW4g+e9l+mZgCIsIuebtOW4g+e9l+mZgCIsMSwiIiwiIl0sWyLmmbrliKkiLCLmmbrliKkiLDEsIiIsIiJdLFsi5Lit6Z2eIiwi5Lit6Z2eIiwxLCIiLCIiXV0sIlNlbGVjdGVkVmFsdWVBcnJheSI6WyItMSJdfSwicDFfU2hpRlNIIjp7IlJlcXVpcmVkIjp0cnVlLCJIaWRkZW4iOmZhbHNlLCJTZWxlY3RlZFZhbHVlIjoi5ZCmIiwiRl9JdGVtcyI6W1si5pivIiwi5Zyo5LiK5rW3IiwxXSxbIuWQpiIsIuS4jeWcqOS4iua1tyIsMV1dfSwicDFfU2hpRlpYIjp7IkZfSXRlbXMiOltbIuaYryIsIuS9j+agoSIsMV0sWyLlkKYiLCLkuI3kvY/moKEiLDFdXSwiU2VsZWN0ZWRWYWx1ZSI6bnVsbH0sInAxX2RkbFNoZW5nIjp7IkhpZGRlbiI6ZmFsc2UsIkZfSXRlbXMiOltbIi0xIiwi6YCJ5oup55yB5Lu9IiwxLCIiLCIiXSxbIuWMl+S6rCIsIuWMl+S6rCIsMSwiIiwiIl0sWyLlpKnmtKUiLCLlpKnmtKUiLDEsIiIsIiJdLFsi5LiK5rW3Iiwi5LiK5rW3IiwxLCIiLCIiXSxbIumHjeW6hiIsIumHjeW6hiIsMSwiIiwiIl0sWyLmsrPljJciLCLmsrPljJciLDEsIiIsIiJdLFsi5bGx6KW/Iiwi5bGx6KW/IiwxLCIiLCIiXSxbIui+veWugSIsIui+veWugSIsMSwiIiwiIl0sWyLlkInmnpciLCLlkInmnpciLDEsIiIsIiJdLFsi6buR6b6Z5rGfIiwi6buR6b6Z5rGfIiwxLCIiLCIiXSxbIuaxn+iLjyIsIuaxn+iLjyIsMSwiIiwiIl0sWyLmtZnmsZ8iLCLmtZnmsZ8iLDEsIiIsIiJdLFsi5a6J5b69Iiwi5a6J5b69IiwxLCIiLCIiXSxbIuemj+W7uiIsIuemj+W7uiIsMSwiIiwiIl0sWyLmsZ/opb8iLCLmsZ/opb8iLDEsIiIsIiJdLFsi5bGx5LicIiwi5bGx5LicIiwxLCIiLCIiXSxbIuays+WNlyIsIuays+WNlyIsMSwiIiwiIl0sWyLmuZbljJciLCLmuZbljJciLDEsIiIsIiJdLFsi5rmW5Y2XIiwi5rmW5Y2XIiwxLCIiLCIiXSxbIuW5v+S4nCIsIuW5v+S4nCIsMSwiIiwiIl0sWyLmtbfljZciLCLmtbfljZciLDEsIiIsIiJdLFsi5Zub5bedIiwi5Zub5bedIiwxLCIiLCIiXSxbIui0teW3niIsIui0teW3niIsMSwiIiwiIl0sWyLkupHljZciLCLkupHljZciLDEsIiIsIiJdLFsi6ZmV6KW/Iiwi6ZmV6KW/IiwxLCIiLCIiXSxbIueUmOiCgyIsIueUmOiCgyIsMSwiIiwiIl0sWyLpnZLmtbciLCLpnZLmtbciLDEsIiIsIiJdLFsi5YaF6JKZ5Y+kIiwi5YaF6JKZ5Y+kIiwxLCIiLCIiXSxbIuW5v+ilvyIsIuW5v+ilvyIsMSwiIiwiIl0sWyLopb/ol48iLCLopb/ol48iLDEsIiIsIiJdLFsi5a6B5aSPIiwi5a6B5aSPIiwxLCIiLCIiXSxbIuaWsOeWhiIsIuaWsOeWhiIsMSwiIiwiIl0sWyLpppnmuK8iLCLpppnmuK8iLDEsIiIsIiJdLFsi5r6z6ZeoIiwi5r6z6ZeoIiwxLCIiLCIiXSxbIuWPsOa5viIsIuWPsOa5viIsMSwiIiwiIl1dLCJTZWxlY3RlZFZhbHVlQXJyYXkiOlsi6LS15beeIl19LCJwMV9kZGxTaGkiOnsiSGlkZGVuIjpmYWxzZSwiRW5hYmxlZCI6dHJ1ZSwiRl9JdGVtcyI6W1siLTEiLCLpgInmi6nluIIiLDEsIiIsIiJdLFsi6LS16Ziz5biCIiwi6LS16Ziz5biCIiwxLCIiLCIiXSxbIuWFreebmOawtOW4giIsIuWFreebmOawtOW4giIsMSwiIiwiIl0sWyLpgbXkuYnluIIiLCLpgbXkuYnluIIiLDEsIiIsIiJdLFsi5a6J6aG65biCIiwi5a6J6aG65biCIiwxLCIiLCIiXSxbIumTnOS7geWcsOWMuiIsIumTnOS7geWcsOWMuiIsMSwiIiwiIl0sWyLmr5XoioLlnLDljLoiLCLmr5XoioLlnLDljLoiLDEsIiIsIiJdLFsi6buU6KW/5Y2X5biD5L6d5peP6IuX5peP6Ieq5rK75beeIiwi6buU6KW/5Y2X5biD5L6d5peP6IuX5peP6Ieq5rK75beeIiwxLCIiLCIiXSxbIum7lOS4nOWNl+iLl+aXj+S+l+aXj+iHquayu+W3niIsIum7lOS4nOWNl+iLl+aXj+S+l+aXj+iHquayu+W3niIsMSwiIiwiIl0sWyLpu5TljZfluIPkvp3ml4/oi5fml4/oh6rmsrvlt54iLCLpu5TljZfluIPkvp3ml4/oi5fml4/oh6rmsrvlt54iLDEsIiIsIiJdXSwiU2VsZWN0ZWRWYWx1ZUFycmF5IjpbIui0temYs+W4giJdfSwicDFfZGRsWGlhbiI6eyJIaWRkZW4iOmZhbHNlLCJFbmFibGVkIjp0cnVlLCJGX0l0ZW1zIjpbWyItMSIsIumAieaLqeWOv+WMuiIsMSwiIiwiIl0sWyLkuYzlvZPljLoiLCLkuYzlvZPljLoiLDEsIiIsIiJdLFsi5Y2X5piO5Yy6Iiwi5Y2X5piO5Yy6IiwxLCIiLCIiXSxbIuS6keWyqeWMuiIsIuS6keWyqeWMuiIsMSwiIiwiIl0sWyLoirHmuqrljLoiLCLoirHmuqrljLoiLDEsIiIsIiJdLFsi55m95LqR5Yy6Iiwi55m95LqR5Yy6IiwxLCIiLCIiXSxbIuWwj+ays+WMuiIsIuWwj+ays+WMuiIsMSwiIiwiIl0sWyLmuIXplYfluIIiLCLmuIXplYfluIIiLDEsIiIsIiJdLFsi5byA6Ziz5Y6/Iiwi5byA6Ziz5Y6/IiwxLCIiLCIiXSxbIuaBr+eDveWOvyIsIuaBr+eDveWOvyIsMSwiIiwiIl0sWyLkv67mlofljr8iLCLkv67mlofljr8iLDEsIiIsIiJdXSwiU2VsZWN0ZWRWYWx1ZUFycmF5IjpbIuWNl+aYjuWMuiJdfSwicDFfWGlhbmdYRFoiOnsiSGlkZGVuIjpmYWxzZSwiTGFiZWwiOiLlm73lhoXor6bnu4blnLDlnYDvvIjnnIHluILljLrljr/ml6DpnIDph43lpI3loavlhpnvvIkiLCJUZXh0Ijoi6Iqx5p6c5ZutcjLljLo05qCLIn0sInAxX0NvbnRlbnRQYW5lbDFfWmhvbmdHRlhEUSI6eyJUZXh0IjoiPHNwYW4gc3R5bGU9J2NvbG9yOnJlZDsnPumrmOmjjumZqeWcsOWMuu+8mjxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guiXgeWfjuWMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guaWsOS5kOW4gjxici8+XHJcbuays+WMl+ecgemCouWPsOW4guWNl+Wuq+W4gjxici8+XHJcbum7kem+meaxn+ecgee7peWMluW4guacm+WljuWOvzxici8+XHJcbuWQieael+ecgemAmuWMluW4guS4nOaYjOWMujxici8+XHJcbuWMl+S6rOW4guWkp+WFtOWMuuWkqeWuq+mZouihl+mBk+iejeaxh+ekvuWMujxici8+XHJcbjxici8+XHJcbuS4remjjumZqeWcsOWMuu+8mjxici8+XHJcbuWMl+S6rOW4gumhuuS5ieWMuuWMl+efs+anvemVh+ilv+i1teWQhOW6hOadkTxici8+XHJcbuWMl+S6rOW4gumhuuS5ieWMuuWMl+efs+anvemVh+WMl+efs+anveadkTxici8+XHJcbuWMl+S6rOW4gumhuuS5ieWMuui1teWFqOiQpemVh+iBlOW6hOadkTxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4gumrmOaWsOWMuui1teadkeaWsOWMuuWwj+WMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4gumrmOaWsOWMuuS4u+ivreWfjuWwj+WMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guaXoOaegeWOv+S4nOWMl+i/nOadkTxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guaXoOaegeWOv+ilv+mDneW6hOadkTxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guato+WumuWOv+epuua4r+iKseWbreWwj+WMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guato+WumuWOv+WtlOadkTxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guaWsOWNjuWMuumDveW4gumYs+WFieWwj+WMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guaWsOWNjuWMuuS4vemDveays+eVlOWwj+WMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guahpeilv+WMuuW5s+WuieWwj+WMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guihjOWUkOWOv+a7qOays+Wwj+WMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guijleWNjuWMuuWkqea1t+iqieWkqeS4i+Wwj+WMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guijleWNjuWMuuaZtuW9qeiLkeWwj+WMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guijleWNjuWMuuS8l+e+juW7iuahpeWbm+Wto0HljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILoo5XljY7ljLrkuJzmlrnmmI7nj6DlsI/ljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILmoaXopb/ljLrnmb3ph5Hlhazlr5M8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILmoaXopb/ljLrljY7mtqbkuIfosaHln448YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILpub/ms4nljLrop4Lls7DlmInpgrjlsI/ljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILmraPlrprljr/lhq/lrrbluoTmnZE8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILmraPlrprljr/kuJzlubPkuZDmnZE8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILplb/lronljLrljZrpm4Xnm5vkuJblsI/ljLpF5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6ZW/5a6J5Yy65Zu96LWr57qi54+K5rm+5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6auY5paw5Yy65aSq6KGM5ZiJ6IuR5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6KOV5Y2O5Yy65Y2T5Lic5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6KOV5Y2O5Yy65paw5Y2O6IuR5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6bm/5rOJ5Yy66ZO25bGx6Iqx5Zut5paw5Yy65bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC5paw5Y2O5Yy65bCa6YeR6IuR5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6ZW/5a6J5Yy65YmN6L+b5p2RPGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6ZW/5a6J5Yy65pmu5ZKM5bCP5Yy65Y2X6ZmiPGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6ZW/5a6J5Yy65bu65piO5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6ZW/5a6J5Yy6566A562R5a625Zut5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6ZW/5a6J5Yy65L+d5Yip6Iqx5ZutQuWMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4gumVv+WuieWMuuS/neWIqeiKseWbrUTljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILplb/lronljLrog7jnp5HljLvpmaLlhazlr5PljJfljLo8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILpq5jmlrDljLrlkIznpaXln47lsI/ljLpD5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6auY5paw5Yy65ZKM5ZCI576O5a625bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6KOV5Y2O5Yy65rW35aSp6Ziz5YWJ5Zut5bCP5Yy6PGJyLz5cclxu5rKz5YyX55yB55+z5a625bqE5biC6KOV5Y2O5Yy65Y2B5LqM5YyW5bu65bCP5Yy6MTblj7fmpbw8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILoo5XljY7ljLrljYHkuozljJblu7rlsI/ljLoxN+WPt+alvDxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guijleWNjuWMuuays+WMl+WfjuW7uuWtpuagoeWutuWxnumZojxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guagvuWfjuWMuuWNk+i+vuWkqumYs+WfjuW4jOacm+S5i+a0suWwj+WMujxici8+XHJcbuays+WMl+ecgeefs+WutuW6hOW4guW5s+WxseWOv+mYsueWq+ermeWwj+WMujxici8+XHJcbuays+WMl+ecgeW7iuWdiuW4guWbuuWuieWOv+iLseWbveWuqzXmnJ88YnIvPlxyXG7msrPljJfnnIHpgqLlj7DluILpmoblsKfljr/ng5/ojYnlrrblm63vvIjng5/ojYnlhazlj7jlrrblsZ7pmaLvvIk8YnIvPlxyXG7msrPljJfnnIHnn7PlrrbluoTluILotbXljr/ku7vluoTmnZE8YnIvPlxyXG7ovr3lroHnnIHlpKfov57luILph5Hmma7mlrDljLrlhYnkuK3ooZfpgZPog5zliKnopb/npL7ljLo8YnIvPlxyXG7ovr3lroHnnIHlpKfov57luILph5Hmma7mlrDljLrmi6XmlL/ooZfpgZPlj6Tln47nlLLljLo8YnIvPlxyXG7pu5HpvpnmsZ/nnIHlpKfluobluILpvpnlh6TljLrkuJbnuqrllJDkurrkuK3lv4PlsI/ljLoy5qCLMeWNleWFgzxici8+XHJcbum7kem+meaxn+ecgem9kOm9kOWTiOWwlOW4guaYguaYgua6quWMuuWkp+S6lOemj+eOm+adkTxici8+XHJcbum7kem+meaxn+ecgeWTiOWwlOa7qOW4gummmeWdiuWMuummmeWdiuWkp+ihl+ihl+mBk+WKnuS6i+WkhOmmmeS4reekvuWMuuWPpOmmmeihlzEy5Y+3PGJyLz5cclxu6buR6b6Z5rGf55yB5ZOI5bCU5ruo5biC6aaZ5Z2K5Yy65aSn5bqG6Lev6KGX6YGT5Yqe5LqL5aSE55S15aGU5bCP5Yy6MTAx5qCLN+WNleWFgzxici8+XHJcbum7kem+meaxn+ecgeWTiOWwlOa7qOW4gummmeWdiuWMuuWSjOW5s+i3r+ihl+mBk+WKnuS6i+WkhOmjjuWNjuekvuWMuuefs+WMluWwj+WMujnmoIs25Y2V5YWDPGJyLz5cclxu6buR6b6Z5rGf55yB5ZOI5bCU5ruo5biC5ZKM5bmz6Lev6KGX6YGT5Yqe5LqL5aSE5LiK5Lic56S+5Yy65LiH6LGh5LiK5Lic5bCP5Yy6ReagizLljZXlhYM8YnIvPlxyXG7lkInmnpfnnIHplb/mmKXluILlhazkuLvlsq3luILojIPlrrblsa/plYc8YnIvPlxyXG7lkInmnpfnnIHplb/mmKXluILnu7/lm63ljLrok4nmoaXlo7nlj7dD5Yy6PGJyLz5cclxu5ZCJ5p6X55yB6ZW/5pil5biC57u/5Zut5Yy65aSn56a55Y2O6YKmQuWMujxici8+XHJcbuWQieael+ecgemVv+aYpeW4guS6jOmBk+WMuumygei+ieWbvemZheWfjuiNt+WFsOWwj+mVh+Wwj+WMujxici8+XHJcbuWQieael+ecgemAmuWMluW4guWMu+iNr+mrmOaWsOWMuuWllei+vuWwj+WMujxici8+XHJcbuWQieael+ecgeadvuWOn+W4gue7j+a1juaKgOacr+W8gOWPkeWMuuaWsOWGnOWwj+WMujflj7fmpbw8YnIvPlxyXG7kuIrmtbfluILpu4TmtabljLrmmK3pgJrot6/lsYXmsJHljLrvvIjnpo/lt57ot6/ku6XljZfljLrln5/vvIk8L3NwYW4+In0sInAxX0NvbnRlbnRQYW5lbDEiOnsiSUZyYW1lQXR0cmlidXRlcyI6e319LCJwMV9GZW5nWERRREwiOnsiTGFiZWwiOiIwMeaciDEx5pel6IezMDHmnIgyNeaXpeaYr+WQpuWcqDxzcGFuIHN0eWxlPSdjb2xvcjpyZWQ7Jz7kuK3pq5jpo47pmanlnLDljLo8L3NwYW4+6YCX55WZIiwiU2VsZWN0ZWRWYWx1ZSI6IuWQpiIsIkZfSXRlbXMiOltbIuaYryIsIuaYryIsMV0sWyLlkKYiLCLlkKYiLDFdXX0sInAxX1RvbmdaV0RMSCI6eyJSZXF1aXJlZCI6ZmFsc2UsIkhpZGRlbiI6dHJ1ZSwiTGFiZWwiOiLkuIrmtbflkIzkvY/kurrlkZjmmK/lkKbmnIkwMeaciDEx5pel6IezMDHmnIgyNeaXpeadpeiHqjxzcGFuIHN0eWxlPSdjb2xvcjpyZWQ7Jz7kuK3pq5jpo47pmanlnLDljLo8L3NwYW4+55qE5Lq6IiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dLCJTZWxlY3RlZFZhbHVlIjpudWxsfSwicDFfQ2VuZ0ZXSCI6eyJMYWJlbCI6IjAx5pyIMTHml6Xoh7MwMeaciDI15pel5piv5ZCm5ZyoPHNwYW4gc3R5bGU9J2NvbG9yOnJlZDsnPuS4remrmOmjjumZqeWcsOWMujwvc3Bhbj7pgJfnlZnov4ciLCJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8iLDFdLFsi5ZCmIiwi5ZCmIiwxXV0sIlNlbGVjdGVkVmFsdWUiOiLlkKYifSwicDFfQ2VuZ0ZXSF9SaVFpIjp7IkhpZGRlbiI6dHJ1ZX0sInAxX0NlbmdGV0hfQmVpWmh1Ijp7IkhpZGRlbiI6dHJ1ZX0sInAxX0ppZUNodSI6eyJMYWJlbCI6IjAx5pyIMTHml6Xoh7MwMeaciDI15pel5piv5ZCm5LiO5p2l6IeqPHNwYW4gc3R5bGU9J2NvbG9yOnJlZDsnPuS4remrmOmjjumZqeWcsOWMujwvc3Bhbj7lj5Hng63kurrlkZjlr4bliIfmjqXop6YiLCJTZWxlY3RlZFZhbHVlIjoi5ZCmIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dfSwicDFfSmllQ2h1X1JpUWkiOnsiSGlkZGVuIjp0cnVlfSwicDFfSmllQ2h1X0JlaVpodSI6eyJIaWRkZW4iOnRydWV9LCJwMV9UdUpXSCI6eyJMYWJlbCI6IjAx5pyIMTHml6Xoh7MwMeaciDI15pel5piv5ZCm5LmY5Z2Q5YWs5YWx5Lqk6YCa6YCU5b6EPHNwYW4gc3R5bGU9J2NvbG9yOnJlZDsnPuS4remrmOmjjumZqeWcsOWMujwvc3Bhbj4iLCJTZWxlY3RlZFZhbHVlIjoi5ZCmIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dfSwicDFfVHVKV0hfUmlRaSI6eyJIaWRkZW4iOnRydWV9LCJwMV9UdUpXSF9CZWlaaHUiOnsiSGlkZGVuIjp0cnVlfSwicDFfUXVlWkhaSkMiOnsiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxLCIiLCIiXSxbIuWQpiIsIuWQpiIsMSwiIiwiIl1dLCJTZWxlY3RlZFZhbHVlQXJyYXkiOlsi5ZCmIl19LCJwMV9EYW5nUkdMIjp7IlNlbGVjdGVkVmFsdWUiOiLlkKYiLCJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8iLDFdLFsi5ZCmIiwi5ZCmIiwxXV19LCJwMV9HZUxTTSI6eyJIaWRkZW4iOnRydWUsIklGcmFtZUF0dHJpYnV0ZXMiOnt9fSwicDFfR2VMRlMiOnsiUmVxdWlyZWQiOmZhbHNlLCJIaWRkZW4iOnRydWUsIkZfSXRlbXMiOltbIuWxheWutumalOemuyIsIuWxheWutumalOemuyIsMV0sWyLpm4bkuK3pmpTnprsiLCLpm4bkuK3pmpTnprsiLDFdXSwiU2VsZWN0ZWRWYWx1ZSI6bnVsbH0sInAxX0dlTERaIjp7IkhpZGRlbiI6dHJ1ZX0sInAxX0ZhblhSUSI6eyJIaWRkZW4iOnRydWV9LCJwMV9XZWlGSFlZIjp7IkhpZGRlbiI6dHJ1ZX0sInAxX1NoYW5nSEpaRCI6eyJIaWRkZW4iOnRydWV9LCJwMV9EYW9YUUxZR0oiOnsiVGV4dCI6IuS4reWbvSJ9LCJwMV9EYW9YUUxZQ1MiOnsiVGV4dCI6Iui0temYsyJ9LCJwMV9KaWFSZW4iOnsiTGFiZWwiOiIwMeaciDEx5pel6IezMDHmnIgyNeaXpeWutuS6uuaYr+WQpuacieWPkeeDreetieeXh+eKtiJ9LCJwMV9KaWFSZW5fQmVpWmh1Ijp7IkhpZGRlbiI6dHJ1ZX0sInAxX1N1aVNNIjp7IlJlcXVpcmVkIjp0cnVlLCJTZWxlY3RlZFZhbHVlIjoi57u/6ImyIiwiRl9JdGVtcyI6W1si57qi6ImyIiwi57qi6ImyIiwxXSxbIum7hOiJsiIsIum7hOiJsiIsMV0sWyLnu7/oibIiLCLnu7/oibIiLDFdXX0sInAxX0x2TWExNERheXMiOnsiUmVxdWlyZWQiOnRydWUsIlNlbGVjdGVkVmFsdWUiOiLmmK8iLCJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8iLDFdLFsi5ZCmIiwi5ZCmIiwxXV19LCJwMV9jdGwwMF9idG5SZXR1cm4iOnsiT25DbGllbnRDbGljayI6ImRvY3VtZW50LmxvY2F0aW9uLmhyZWY9Jy9EZWZhdWx0LmFzcHgnO3JldHVybjsifSwicDEiOnsiSUZyYW1lQXR0cmlidXRlcyI6e319fQ==',
            'F_TARGET': 'p1_ctl00_btnSubmit'
        }

        response = requests.post('https://selfreport.shu.edu.cn/DayReport.aspx', headers=headers, cookies=cookies, data=data)
        print('Referer:', headers['Referer'], end=f'[{response.status_code}]')
        res = self.res_find.search(response.text)
        if res and not filelog:
            print(res[1])



def main(): pass


if __name__ == "__main__":
    pass
    
