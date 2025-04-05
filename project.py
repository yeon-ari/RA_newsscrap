#cmd  작업: pip install lxml
from email.base64mime import header_length
import requests
from bs4 import BeautifulSoup
import csv

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

filename="'풍력발전소 반대' 네이버 기사 스크래핑 2010.csv"
f=open(filename,"w",encoding="utf-8-sig",newline="")
writer=csv.writer(f)

title="기사 제목na신문사na발행 날짜na본문 내용".split("na") 
writer.writerow(title)

#해결: res.status_code 404 오류, 한글 깨짐, connection 거부, requests.exceptions.SSLError: HTTPSConnectionPool(host='www.vop.co.kr', port=443): Max retries exceeded with url: /A00001439221.html (Caused by SSLError dh key too small (_ssl.c:997)'))), 코드 미완성 출력 해결
def calling_text(url):
    global context
    global headline_n
    global news_url

    res=requests.get(url,headers=headers,verify=False)
    soup=BeautifulSoup(res.text,"lxml")

    if res.status_code!=requests.codes.ok:
        context="해당 기사는 관련자에 의해 삭제되었습니다."
    else:
        print(res.status_code)  
        print (news_url)
        if ("kjmbc" in url)|("tjmbc" in url)|("busanmbc" in url)|("ysmbc" in url)|("usmbc" in url)|("jejumbc" in url): #대전mbc,부산mbc, 여수mbc,울산mbc-두번째 기사 연결 오류,제주mbc,광주mbc
            if "풍력발전 갈등 곳곳에" in headline_n:
                context="본 기사는 삭제되었습니다."
            else:
                context=soup.select_one("#journal_article_wrap").get_text()
        if "dgmbc" in url: #대구 mbc
            context=soup.find("div",attrs={"class":"single-content"}).get_text()
        elif "kyeongin" in url: #경인일보
            context="html 불일치"
        elif "kookje" in url: #국제신문-글자깨짐-해결
            html=res.content.decode('euc-kr','replace')
            soup=BeautifulSoup(html,"lxml")
            context=soup.find("div",attrs={"class":"news_article"}).get_text()
        elif "kmib" in url: #국민일보-글자깨짐-해결
            html=res.content.decode('euc-kr','replace')
            soup=BeautifulSoup(html,"lxml")
            context=soup.find("div",attrs={"class":"tx"}).get_text()
        elif "e-platform" in url:
            context=soup.find("div",attrs={"class":"ad-template"}).get_text()
        elif "smartfn" in url: #스마트에프엔
            context=soup.find("div",attrs={"class":"vc_con articleContent detailCont"}).get_text()
        elif "tfmedia" in url: #조세금융신문
            context=soup.select_one("#news_body_area").get_text()
        elif ("naeil" in url)|("tf" in url)|("dailian" in url)|("skyedaily" in url): #내일신문,더팩트,데일리안-삭제된 기사 홈페이지로 넘어가는 거 해결해야, 스카이데일리-글자깨짐-해결
            if "skyedaily" in url:
                html=res.content.decode('euc-kr','replace')
                soup=BeautifulSoup(html,"lxml")
            elif ("중국 패권에 굴종하는" in headline_n)|('위기의 태양광 산업' in headline_n)|('<storyK 칼럼>원전 반대?' in headline_n)|('"목숨 값 싼 나라" 안철수' in headline_n):
                context="본 기사는 삭제되었습니다."
            else:
                context=soup.find("div",attrs={"class":"article"}).get_text()
        elif "munhwa" in url: #문화일보-글자깨짐-해결했는데 connection aborted-더미 헤더 정보 넘겨줌으로써 해결
            html=res.content.decode('euc-kr','replace')
            soup=BeautifulSoup(html,"lxml")
            context=soup.select_one("#NewsAdContent").get_text()
        elif "seoul." in url: #서울신문 태그 오류...이게 왜 돌아가..?
            context="html 불일치"
        elif "segye" in url: #세계일보
            context=soup.find("article",attrs={"class":"viewBox2"}).get_text()
        elif "asiatoday" in url: #아시아투데이
            context=soup.find("div",attrs={"class":"news_bm"}).get_text()
        elif "joongang" in url: #중앙일보,코리아중앙데일리
            if '포토타임' in headline_n: #키워드 본문만 뜨도록 고쳐야
                con=soup.find_all("div",attrs={"class":"chat_box"})  #find_all 은 리스트 형식이라 .get_text() 가 고대로 사용 안됨 for 문 써야
                for context in con:
                    print(context.get_text())
            else:
                context=soup.select_one("#article_body").get_text()
        elif "sunday" in url: #중앙 sunday-코드 미완성 뜸-해결 (href 속성값과 url이 다름)
            context=soup.select_one("#article_body").get_text()
        elif ("h21.hani" in url)|("w.hani" in url) | ("seouland" in url)|("shindonga" in url): #한겨레,신동아,한겨레21-raise ConnectionError(err, request=request)requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))-해결
            if "중국 시위주민 발포" in headline_n:
                html=res.content.decode('euc-kr','replace')
                soup=BeautifulSoup(html,"lxml")
                context=soup.find("div",attrs={"class":"news_text01"}).get_text()
            else:
                context=soup.find("div",attrs={"class":"text"}).get_text()
        elif ("hani" in url) & ("2korea" in url): #투코리아-한겨레 하위신문사... ^^;
            context=soup.find("div",attrs={"class":"xe_content"}).get_text()
        elif "hankookilbo" in url: #한국일보
            context=soup.find("div",attrs={"class":"end-body"}).get_text()
        elif ("cpbc" in url)|("pressian" in url): #가톨릭평화방송,평화신문,프레시안-requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))-해결
            context=soup.find("div",attrs={"class":"article_body"}).get_text()
        elif "news1" in url: #뉴스1-글자깨짐-해결
            html=res.content.decode('utf-8','replace')
            soup=BeautifulSoup(html,"lxml")
            if "photos" in url:
                context=soup.find("p",attrs={"class":"photo_view_content"}).get_text()
            else:
                context=soup.find("div",attrs={"class":"detail sa_area"}).get_text()
        elif "newspim" in url: #뉴스핌
            if ('유니슨과 손잡은 금호석화' in headline_n)|("[투자활성화] 정부, 1단계" in headline_n)|("흔들리는 탄소배출권 시장" in headline_n)|("삼성重, 스코틀랜드에 해상" in headline_n):
                context="본 기사는 삭제되었습니다."
            else:
                context=soup.select_one("#news-contents").get_text()
        elif "newsis" in url: #뉴시스-2페이지부터 raise HTTPError (기사 삭제)-해결
            context=soup.find("div",attrs={"class":"viewer"}).get_text()
        elif "andongmbc" in url: #안동mbc
            context=soup.find("div",attrs={"class":"news_cont"}).get_text()
        elif "sentv" in url: #서울경제tv
            context=soup.select_one("#newsView").get_text()
        elif "yonhapnews" in url: #연합뉴스-첫 번째 기사 인식을 못하는데 머고 (href 속성값과 url..)
            if "PYH" in url:
                context=soup.find("div",attrs={"class":"article-txt"}).get_text()
            elif "tv" in url:
                context=soup.select_one("#articleBody").get_text()
            else:
                context=soup.find("article",attrs={"class":"story-news article"}).get_text()
        elif ("mediapen" in url)|("jejuilbo" in url)|("hg-times" in url)|("yonhapnewstv" in url)|("ajunews" in url): #연합뉴스tv,아주경제,한강타임즈,뉴제주일보,주간조선,
            if ('영암 풍력발전단지 조성사업' in headline_n)|('풍력발전업계, RPS' in headline_n):
                context="본 기사는 삭제되었습니다."
            else:
                context=soup.select_one("#articleBody").get_text()
        elif "weekly.chosun" in url:
            context=soup.select_one("#article-view-content-div").get_text()
        elif "pub.chosun" in url: #조선펍
            context=soup.find("div",attrs={"class":"article-body"}).get_text()
        elif ("mediafine" in url)|("dailysportshankook" in url)|("iusm" in url): #미디어파인,단비뉴스,데일리스포츠한국,울산매일신문-글자깨짐-해결
            html=res.content.decode('euc-kr','replace')
            soup=BeautifulSoup(html,"lxml")
            context=soup.select_one("#articleBody").get_text()
        elif "ichannela" in url: #채널A
            context=soup.select_one("#articleSection").get_text()
        elif "wowtv" in url: #한국경제tv
            context=soup.select_one("#divNewsContent").get_text()
        elif ("jtbc" in url)|("busan.com" in url)|("jnilbo" in url): #jtbc,부산일보,전남일보
            if "전남에 몰리는 태양광… 환경훼손.주민 갈등 그림자" in headline_n:
                context="해당 기사는 관련자에 의해 삭제되었습니다."
            else:
                context=soup.find("div",attrs={"class":"article_content"}).get_text()
        elif "kbsm" in url: #경북신문
            context="html 불일치"
        elif "kbs" in url: #kbs
            if '그린벨트 푼 곳에 쇼핑몰· 호텔 허용 외' in headline_n:
                context="해당 기사는 관련자에 의해 삭제되었습니다."
            else:
                context=soup.find("div",attrs={"class":"detail-body font-size"}).get_text()
        elif "lghellovision" in url: #lg헬로비전
            context=soup.find("div",attrs={"class":"bbs-contents"}).get_text()
        elif "imbc" in url: #mbc
            if ("아직도 원전이 우선?‥거꾸로" in headline_n)|("부산저축은행 임직원 친인척들" in headline_n)|("독일, 2022년까지" in headline_n)|('"2030년까지 발전소 탄소 배출량 30% 감축"' in headline_n)|('풍력발전 반대? 백두대간' in headline_n)|("풍력발전 '환경파괴' 논란" in headline_n):
                context="본 기사는 삭제되었습니다."
            else:
                context=soup.find("div",attrs={"class":"news_txt"}).get_text()
        elif "mbn" in url: #mbn-글자깨짐-해결
            html=res.content.decode('utf-8','replace')
            soup=BeautifulSoup(html,"lxml")
            if "money" in url: #매일경제
                context=soup.find("div",attrs={"class":"news_contents"}).get_text()
            else:
                context=soup.find("div",attrs={"class":"detail"}).get_text()
        elif "sbs" in url: #sbs
            if "cnbc" in url:
                context="html 불일치"
            elif "biz" in url:
                context="html 불일치"
            else:
                context=soup.find("div",attrs={"class":"text_area"}).get_text()
        elif "mk" in url: #매경이코노미-글자깨짐-다 해결
            html=res.content.decode('utf-8','replace')
            soup=BeautifulSoup(html,"lxml")
            try:
                if "economy" in url:
                    context=soup.find("div",attrs={"class":"article_body"}).get_text()
                elif "premium" in url:
                    context=soup.find("div",attrs={"class":"view_txt"}).get_text()
                else:
                    html=res.content.decode('euc-kr','replace')
                    soup=BeautifulSoup(html,"lxml")
                    category=soup.find("a",attrs={"class":"mkservicelogo"}).get_text()
                    print(category)
                    if "오피니언" in category:
                        context=soup.find("div",attrs={"class":"view_txt"}).get_text() 
                    else:
                        context=soup.find("div",attrs={"class":"art_txt"}).get_text()
            except:
                url="https://www.mk.co.kr/economy/view/2017/"+news_url[-6:]
                calling_text(url)
        elif "dtnews" in url: #디트뉴스
            if "서천-군산 大戰의 원인과 해법" in headline_n:
                context="본 기사는 삭제되었습니다."
            else:
                context=soup.select_one("#article-view-content-div").get_text()
        elif "mdtoday" in url: #메디컬투데이
            context=soup.select_one("#articleBody").get_text()
        elif "dt" in url: #디지털타임스-글자깨짐, 두번째기사 connection aborted,
            html=res.content.decode('euc-kr','replace')
            soup=BeautifulSoup(html,"lxml")
            context=soup.find("div",attrs={"class":"art_txt"}).get_text()      
        elif "viva100" in url: #브릿지경제
            context=soup.find("div",attrs={"class":"left_text_box"}).get_text()
        elif "businesspost" in url: #비즈니스포스트
            if ("[Who Is ?] 정지택 두산중공업 부회장"in headline_n)|("조환익, 한전 최장수 CEO 관록" in headline_n):
                context="html 불일치"
            else:
                try: 
                    context=soup.find("div",attrs={"class":"rns_text"}).get_text()
                except:
                    context=soup.find("div",attrs={"class":"tab_container"}).get_text()
        elif ("sedaily" in url)|("heraldcorp" in url)|("joseilbo" in url)|("honam" in url): #서울경제,헤럴드경제,무등일보-본문 코드 미완성 뜸-해결
            if '"칠산 앞바다 해상풍력 발전 반대"' in headline_n:
                context="본 기사는 삭제되었습니다." 
            else:
                context=soup.find("div",attrs={"class":"article_view"}).get_text()
        elif "바람 잘날 없는" in headline_n:
            context="본 기사는 삭제되었습니다."
        elif "asiae" in url: #아시아경제
            context=soup.find("div",attrs={"class":"article fb-quotable"}).get_text()
        elif "ekn" in url: #에너지경제
            context=soup.find("div",attrs={"class":"view-text"}).get_text()
        elif "etoday" in url: #이투데이
            context=soup.find("div",attrs={"class":"articleView"}).get_text()
        elif "fnnews" in url: #파이낸셜뉴스
            context=soup.find("div",attrs={"class":"cont_art"}).get_text()
        elif ("newsprime" in url)|("theguru" in url)|("m-economynews" in url): #프라임경제,더구루,m이코노미
            context=soup.select_one("#news_body_area").get_text()
        elif "autotimes" in url: #오토타임즈
            context=soup.find("div",attrs={"class":"view_report"}).get_text()
        elif "hankyung" in url: #한국경제
            try:
                if "magazine" in url: #매거진한경
                    context=soup.select_one("#magazineView").get_text()
                else:
                    context=soup.select_one("#articletxt").get_text()
            except:
                context=soup.find("div",attrs={"class":"view-cont-area"}).get_text()
        elif "ppss" in url: #ㅍㅍㅅㅅ
            context=soup.find("div",attrs={"class":"entry-content"}).get_text()
        elif "nocutnews" in url: #노컷뉴스
            context=soup.select_one("#pnlContent").get_text()
        elif "newdaily" in url: #뉴데일리
            context=soup.find("section",attrs={"class":"nd-center"}).get_text()
        elif "newsway" in url: #뉴스웨이
            context=soup.find("div",attrs={"class":"view_text"}).get_text()
        elif "ddanzi" in url: #딴지뉴스
            context=soup.find("div",attrs={"class":"read_content"}).get_text()
        elif "mtn" in url:
            context=soup.find("div",attrs={"class":"news-article-wrapper"}).get_text()
        elif ("greendaily" in url)|("econonews" in url)|("kado" in url): #그린데일리,이코노뉴스,bbs news,강원도민일보
            context=soup.find("div",attrs={"class":"article-body"}).get_text()
        elif "dailyhankooki" in url: #?
            context="html 불일치"
        elif "g-enews" in url: #글로벌이코노믹
            context=soup.find("div",attrs={"class":"vtxt detailCont"}).get_text()
        elif "newstomato" in url: #뉴스토마토-AttributeError: 'NoneType' object has no attribute 'get_text'
            #context=soup.find("div",attrs={"class":"rns_text"}).get_text()
            context="html 불일치"
        elif "globalepic" in url: #글로벌에픽
            context=soup.find("div",attrs={"class":"vtext"}).get_text()
        elif "zdnet" in url: #zdnet korea-Connection aborted.'-해결
            context=soup.select_one("#articleBody").get_text()
        elif "megaeconomy" in url: #메가경제
            context=soup.find("div",attrs={"class":"viewConts"}).get_text()
        elif "vop" in url: #민중의소리-requests.exceptions.SSLError: HTTPSConnectionPool(host='www.vop.co.kr', port=443): Max retries exceeded with url: /A00001439221.html (Caused by SSLError(SSLError(1, '[SSL: DH_KEY_TOO_SMALL] dh key too small (_ssl.c:997)')))-verify 변수 추가, 7,8줄 코드로 해결
            html=res.content.decode('utf-8','replace')
            soup=BeautifulSoup(html,"lxml")
            if "태양광에 내밀린 농민들" in headline_n:
                context=soup.find("div",attrs={"class":"article-body"}).get_text()
            context="html 불일치"
        elif "slownews" in url: #슬로우뉴스
            context=soup.select_one("#article_content").get_text()
        elif "theasian" in url: #아시아엔
            context=soup.find("div",attrs={"class":"entry-content clearfix"}).get_text()
        elif "ohmynews" in url: #오마이뉴스
            if "2792529" in url: #star 인식을 못함 계속
                context=soup.find("div",attrs={"class":"atc-text"}).get_text()
            elif ("2719423" in url)|("A0002825345" in url)|("A0002276812" in url):
                context=soup.find("div",attrs={"class":"content_box type2"}).get_text()
            elif ("A0002436520" in url):
                context=soup.find("div",attrs={"class":"text"}).get_text()
            elif ("A0002794171" in url):
                context=soup.find("article",attrs={"class":"article_body at_contents article_view"}).get_text()
            elif "연전연패 독일 여당" in headline_n:
                context=soup.find("div",attrs={"class":"article_view"}).get_text()
            else:  
                context=soup.find("div",attrs={"class":"at_contents"}).get_text()
        elif "huffingtonpost" in url: #허프포스트코리아
            context=soup.find("div",attrs={"class":"content-list-component text"}).get_text() 
        elif "upinews" in url: #UPI 뉴스
            context=soup.select_one("#article").get_text()
        elif "topstarnews" in url: #톱스타뉴스
            context=soup.find("div",attrs={"class":"article-view-page"}).get_text() 
        elif "news.naver.com" in url: #헤럴드pop,더불어민주당,민생당,정의당,쿠키뉴스 다-requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))-해결
            context=soup.select_one("#dic_area").get_text()
        elif "redian" in url: #sbs golf
            context=soup.find("div",attrs={"class":"pf-content"}).get_text() 
        elif "kwnews" in url: #강원일보
            context=soup.select_one("#kwnews_body").get_text()
        elif "knnews" in url: #경남신문
            context=soup.select_one("#content_li").get_text()
        elif "ksmnews" in url: #경상매일신문-문제 있음-해결?
            context="html 불일치"
        elif "kjdaily" in url: #광주매일신문,한국기독공보-태그 인식 오류
            context=soup.select_one("#content").get_text()
        elif "pckworld" in url:
            context="html 불일치"
            #context=soup.select_one("#head_wrap").get_text()
        elif "idaegu.com" in url: #대구일보
            context=soup.select_one("#body_wrap").get_text()
        elif "daejonilbo" in url: #대전일보-글자깨짐-해결
            html=res.content.decode('utf-8','replace')
            soup=BeautifulSoup(html,"lxml")
            context=soup.select_one("#article-view-content-div").get_text()
        elif "imaeil" in url: #매일신문
            if "[자연과 인간문화의 융복합도시 영양]" in headline_n:
                context="본 기사는 삭제되었습니다."
            else:
                context=soup.select_one("#articlebody").get_text()
        elif ("koreadaily" in url)|("dongascience" in url): #미주중앙일보,동아사이언스
            context=soup.select_one("#article_body").get_text()
        elif "sjbnews" in url: #새전북신문
            if "포커스" in headline_n: #페이지 뜨지 않아 이 코드는 임시방편
                context="존재하지 않습니다."
            else:
                context=soup.find("div",attrs={"class":"p-b-70"}).get_text()
        elif "yeongnam" in url: #영남일보-태그 인식 오류-해결?
            context=soup.find("div",attrs={"class":"article-news-box"}).get_text()
        elif "jjan" in url: #전북일보
            context=soup.find("div",attrs={"class":"article_txt_container"}).get_text()
        elif "joongdo" in url: #중도일보
            context=soup.select_one("#font").get_text()
        elif "voakorea" in url: #voa
            context=soup.find("div",attrs={"class":"wsw"}).get_text()
        elif "lady.khan" in url: #레이디경향
            context=soup.select_one("#_article").get_text()
        elif "khan" in url: #경향신문 http://www.khan.co.kr/kh_news/art_view.html?artid=201205111346001&code=910303
            try:
                context=soup.find("div",attrs={"class":"art_body"}).get_text()
            except:
                context=soup.find("div",attrs={"class":"article_txt"}).get_text()
        elif "esquirekorea" in url: #에스콰이어
            context=soup.find("div",attrs={"class":"article_wrap"}).get_text()
        elif "economychosun" in url: #이코노미조선
            context=soup.find("div",attrs={"class":"conts"}).get_text()
        elif "ildaro" in url: #일다
            context=soup.select_one("#textinput").get_text()
        elif "monthly.chosun" in url: #월간조선
            context=soup.select_one("#articleBody").get_text()
        elif ("chosun" in url)|("biz.chosun" in url): #조선일보,조선비즈 둘다 태그 맞게 찾았는데 왜 get_text 함수 못 쓴다고 하는지
            contexy=''
            cons=soup.find_all("p",attrs={"class":" article-body__content article-body__content-text | text--black text font--size-sm-18 font--size-md-18 font--primary"})
            for con in cons:
                cont=con.get_text()
                contexy+=cont
            context=contexy
        elif "jmagazine" in url: #월간중앙-글자 깨짐-해결
            html=res.content.decode('utf-8','replace')
            soup=BeautifulSoup(html,"lxml")
            context=soup.find("div",attrs={"class":"con_area"}).get_text()
        elif "bbsi" in url:
            context="html 불일치"
        elif  ("legaltimes" in url)|("danbinews" in url)|("civicnews" in url)|("dailyimpact" in url)|("codingworldnews" in url)|("ngetnews" in url): #데일리한국-태그 오류,코딩월드뉴스,뉴스저널리즘, 리걸타임즈
            context=soup.select_one("#article-view-content-div").get_text()
        elif "dnews" in url: #e대한경제-코드 미완성 뜸-해결
            context=soup.find("div",attrs={"class":"newsCont"}).get_text()
        elif "paxnetnews" in url: #팍스넷뉴스
            context=soup.find("div",attrs={"class":"read-news-main-contents"}).get_text()
        elif ("news.donga.com" in url)|("etnews.com" in url)|("weekly.khan" in url): #동아일보,전자신문,주간경향-requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))-해결
            context=soup.find("div",attrs={"class":"article_txt"}).get_text()
        elif "jeollailbo" in url:
            context=soup.find("div",attrs={"class":"content"}).get_text()
        elif ("hellodd" in url)|("gnnews" in url)|("jbnews" in url)|("newswatch" in url)|("idaegu.co." in url)|("gokorea" in url)|("smedaily" in url)|("nongaek" in url)|("leaders" in url)|("whitepaper" in url)|("hdhy" in url)|("ikpnews" in url)|("kbiznews" in url)|("electimes" in url)|("e-platform" in url)|("suhyupnews" in url)|("safetimes" in url)|("ibuan" in url)|("beopbo" in url)|("thedailypost" in url)|("the-pr" in url)|("ikld" in url)|("fortunekorea" in url)|("laborplus" in url)|("outdoornews" in url)|("sisain" in url)|("ilemonde" in url)|("ccdailynews" in url)|("jejusori" in url)|("domin" in url)|("jeonmin" in url)|("incheontoday" in url)|("incheonilbo" in url)|("siminsori" in url)|("namdonews" in url)|("gimhaenews" in url)|("ksilbo" in url)|("kyongbuk" in url)|("kbmaeil" in url)|("idomin" in url)|("gndomin" in url)|("incheonnews" in url)|("incheonin" in url)|("sisafocus" in url)|("sisajournal" in url)|("jeonmae" in url)|("newscj" in url)|("m-i" in url)|("gukje" in url)|("greenpostkorea" in url)|("paxetv" in url)|("obsnews" in url)|("joongboo" in url)|("enewstoday" in url)|("e2news" in url)|("todayenergy" in url)|("newsquest" in url)|("newstof" in url)|("mediatoday" in url)|("seoulfn" in url)|("newsfreezone" in url)|("dandinews" in url)|("straightnews" in url): #전국매일신문,천지일보,매일일보,국제뉴스,그린포스트,팍스경제tv,obs,대한금융신문,이뉴스투데이,이투뉴스,투데이에너지,뉴스퀘스트,뉴스톱,미디어오늘,서울파이낸스,뉴스프리존,단디뉴스,스트레이트뉴스,시빅뉴스,시사저널,시사포커스,인천in,인천뉴스,경남도민신문,(경남도민일보,경북도민일보),경북매일신문,경북일보,경상일보,김해뉴스,남도일보,시민의 소리,인천일보,인천투데이,전민일보,전북도민일보,제주도민일보,제주의소리,중부일보,시사in,이코노믹리뷰,참여와혁신,국토일보,더피알,부산제일경제-코드미완성 출력-해결,중소기업신문,공감뉴스
        #헬로디디,경남일보,중부매일,뉴스워치,대구신문,오피니언타임즈-코드 미완성 출력-해결, 충청일보-삭제된 기사 존재raise HTTPError(http_error_msg, response=self)requests.exceptions.HTTPError: 404 Client Error: Not Found for url-해결,르몽드,아웃도어뉴스,포춘코리아,데일리포스트,법보신문,부안독립신문,세이프타임즈,어업in수산,에너지플랫폼뉴스,오피니언뉴스,전기신문,중소기업뉴스,한국농정신문,현대해양,화이트페이퍼,
            try:
                context=soup.select_one("#article-view-content-div").get_text()
            except:
                url="https://www.electimes.com/news/articleView.html?idxno="+news_url[-9:-3]
                res=requests.get(url,headers=headers,verify=False)
                soup=BeautifulSoup(res.text,"lxml")
                context=soup.select_one("#article-view-content-div").get_text()
        elif ("econovill" in url):
            if ("핵 폐기시설 없는 원자력발전은" in headline_n)|('에너지의 역사를 알면' in headline_n):
                context="본 기사는 삭제되었습니다."
            else:
                context=soup.select_one("#article-view-content-div").get_text()
        elif ("moneys" in url)|("mt" in url): #머니s,머니투데이
            context=soup.select_one("#textBody").get_text()
        elif "ceoscoredaily" in url: #ceo스코어데일리
            context="html 불일치"
        elif "edaily.co" in url: #이데일리
            context=soup.find("div",attrs={"class":"newscontainer"}).get_text()
        elif "getnews" in url: #글로벌경제
            context="html 불일치"
        elif "korea.kr" in url: #정책브리핑-삭제된 기사 존재하는데 404 안 뜨고 홈으로
            if ('오바마 대통령의' in headline_n)|('“원자력 산업은 이미 사양길”' in headline_n):
                context="해당 기사는 관련자에 의해 삭제되었습니다."
            else:
                context=soup.find("div",attrs={"class":"view-cont"}).get_text()         
        print(context)
    
num=1

def windmill(url):
    global num
    global headline_n
    global news_url

    res=requests.get(url)
    res.raise_for_status()
    soup=BeautifulSoup(res.text,"lxml")

    print(num,"페이지")
    articles=soup.find_all("div",attrs={"class":"news_area"})
    for article in articles:
        headline=article.find("a",attrs={"class":"news_tit"})
        headline_n=headline.get_text()
        if ("[신·재생E 산업]안전한 미래" in headline_n)|("정부·지자체 일방통행 ‘반환경’ 자충수" in headline_n)|("[공기업 올해 실적 우등생은 누구?]" in headline_n)|("[건설 R&D 기술 끝없는 진화①]상식을 깼다" in headline_n)|("‘죽음의 시화호’" in headline_n)|("(대전)해상풍력 大戰" in headline_n)|("[데스크 칼럼] 4차산업-5G 중요한데" in headline_n)|("'지역콘텐츠, 글로컬 시대 이끈다'" in headline_n)|("인건비, 왜 이렇게 비싸!" in headline_n):
            continue
        headline_n=headline_n+"nayeon"
        print("기사 제목 : ", headline_n)
        
        info=article.find("a",attrs={"class":"info press"}).get_text()
        if "언론사 선정" in info:
            info=info.strip('언론사 선정')
        if "SK브로드밴드"==info:
            continue
        info=info+"nayeon"
        print("신문사 : ", info)

        date=article.find_all("span",attrs={"class":"info"})
        for dates in date:
            date=dates.get_text()+"nayeon"
            if "면" in date:
                continue
            else:
                print("날짜 : ",date)

        news_url=headline["href"]
        calling_text(news_url)

        l=headline_n+info+date+context
        l=l.split("nayeon")
        writer.writerow(l)
       

    nums=soup.find("a",attrs={"class":"btn_next"})
    next=nums["aria-disabled"]

    if next == "true":
        print("기사자료 추출 끝")
    if next == "false":
        num=num+1
        url="https://search.naver.com/search.naver"+nums["href"]
        windmill(url)

key=input("검색할 검색어를 입력하시오 : ")
start=input("스크래핑할 뉴스의 시작 일을 xxxx.xx.xx 형식으로 입력하시오 : ")
end=input("스크래핑할 뉴스의 마지막 일을 xxxx.xx.xx 형식으로 입력하시오 : ")
pg=input("스크래핑을 시작할 뉴스 웹페이지 시작 번호를 입력하시오 : ")
url_format="https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=0&photo=0&field=0&pd=3&ds={}&de={}&cluster_rank=37&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from{}to{},a:all&start={}".format(key,start,end,start,end,pg)
#url_format="https://search.naver.com/search.naver?where=news&query=%ED%92%8D%EB%A0%A5%EB%B0%9C%EC%A0%84%EC%86%8C%20%EB%B0%98%EB%8C%80&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds=2017.01.01&de=2017.12.31&docid=&related=0&mynews=1&office_type=2&office_section_code=6&news_office_checked=2374&nso=so%3Ar%2Cp%3Afrom20170101to20171231&is_sug_officeid=0"
windmill(url_format)



