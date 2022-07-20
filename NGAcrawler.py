from bs4 import BeautifulSoup
import urllib3
import tkinter as tk
import webbrowser

#Soup_outputfile='C:/Users/user/Desktop/NGAcrawler_soup.txt'
#wholePage_file='C:/Users/user/Desktop/wholeNGApage.txt'

NGA_HOMEPAGE_URL='https://bbs.nga.cn/thread.php?fid=650'
NEXT_PAGE_APPEND_URL='&page='
TOPIC_WEBSITE_URL='bbs.nga.cn'
BLOCK_STRING_1='[版面活动]'
BLOCK_STRING_2='[签到活动]'
BLOCK_STRING_3='[ROLL贴]'
commentCount=30
http=urllib3.PoolManager()
headers=urllib3.make_headers(keep_alive=True,user_agent='Googlebot/2.1')

urls=[]
topics=[]
window=tk.Tk()
contentFrame=tk.Frame(window)

def getNGApageHTML():
    global commentCount
    #global Soup_outputfile
    global urls
    global topics
    global http
    global headers

    urls=[]
    topics=[]

    
    first_loop=True
    url=NGA_HOMEPAGE_URL
    pageNum=2
    while(pageNum<=3):
        # if first_loop:
        #     open(Soup_outputfile,'w').close() #每一次執行程式，都清空輸出檔
        #     #open(wholePage_file,'w').close()
        
        #soup_file=open(Soup_outputfile,'a',encoding='UTF-8')
        #wholepage_file=open(wholePage_file,'a',encoding='UTF-8')
        
        #獲得目標頁面html
        NGA_homepage=http.request('GET',url,headers=headers)
        print(NGA_homepage.status) 
        soup=BeautifulSoup(NGA_homepage.data,'html.parser')
        
        #print(soup.prettify(),file=wholepage_file)
        #print('-----------',file=wholepage_file)

        #獲取回復數大於等於指定數的討論帖
        for reply_count  in soup.findAll('a',{'class':'replies'}):
            if int(reply_count.contents[0])>=commentCount:
                topic_id=str(reply_count.get('id')).replace('rc','tt')
                topic=soup.find('a',{'id':''+str(topic_id)+''})
                #print(topic.get('id'),file=soup_file)
                if not BLOCK_STRING_1 in topic.contents[0] and not BLOCK_STRING_2 in topic.contents[0] and not BLOCK_STRING_3 in topic.contents[0]:
                    # print(TOPIC_WEBSITE_URL+topic.get('href'),file=soup_file)
                    # print(topic.contents[0],file=soup_file)
                    #print(reply_count.get('id'),file=soup_file)
                    urls.append(TOPIC_WEBSITE_URL+topic.get('href'))
                    topics.append(topic.contents[0])
        
        #print(urls)
        #print(topics)

        if first_loop:
            first_loop=False
        else:
            pageNum+=1
        url=NGA_HOMEPAGE_URL+NEXT_PAGE_APPEND_URL+str(pageNum)

        #soup_file.close()
        #wholepage_file.close()

def getTopics():
    global urls
    global topics
    global window
    global contentFrame

    
    print('click button')

    contentFrame.pack_forget()
    contentFrame.destroy()

    contentFrame=tk.Frame(window)
    contentFrame.pack()
    
    getNGApageHTML()
    for i in range(len(urls)) :
        webLink=tk.Label(contentFrame,text=topics[i], cursor="hand2")
        webLink.pack()
        webLink.bind('<Button-1>',lambda e,url=urls[i]:webbrowser.open_new_tab(url))

def display():

    global window

    window.title('NGA crawler')
    window.geometry('600x400') #widthxheight

    contentFrame.pack()

    searchButton=tk.Button(window,text='search',command=getTopics)
    searchButton.pack()

    window.mainloop()

if __name__=='__main__':
    display()

