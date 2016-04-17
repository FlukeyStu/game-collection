import urllib2
import mechanize
import shutil

#TODO:
#   Get Label image instead of UGC image

def get_html(url):
    try:
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.set_handle_refresh(False)
        br.addheaders=[('User-agent','Firefox')]
        response = br.open(url)
        html = response.read()
        return html
    except:
        return None
        
def scrape(title):
    x = 0
    urltemp = 'http://www.thecoverproject.net/view.php?game_id='
    while x <= 9470:
        x += 1
        print 'Trying id ' + str(x) + '...'
        url = urltemp + str(x)
        html = get_html(url)
        if not html == None:
            print 'Found HTML!'
            title = title.upper()
            with open('fullhtml.txt','w') as file:
                file.write(html)
            with open('fullhtml.txt','rb') as rawFile:
                print 'Searching HTML...'
                found_url = find_title(title, rawFile)
                #print found_url
        else: 
            print "Can't get HTML. Continuing..."
            continue
        if not found_url == None:
            print 'Found Title!'
            with open('fullhtml.txt','rb') as rawFile:
                for line in rawFile:
                    if 'href="/download_cover.php?' in line:
                        for elem in line.split('"'):
                            if 'download_cover.php' in elem:
                                suff = elem
                        print 'Finding Image Link...'
                        fileurl = urlpre + suff
                        req = urllib2.urlopen(fileurl)
                        file_name = "BOXART_" + title.replace(":","") + '.jpg'
                        print 'Saving File ' + file_name
                        with open(file_name, 'wb') as fp:
                            shutil.copyfileobj(req, fp)
                            return file_name
    
def find_title(title,file):
    a = None
    for line in file:
        line = line.upper()
        if '<H2>'in line:
            if title in line:
                a = '999'
    return a

if __name__ == '__main__':
    urlpre = 'http://www.thecoverproject.net'
    print scrape("Starfox 64")
