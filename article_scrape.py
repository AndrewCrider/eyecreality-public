
from bs4 import BeautifulSoup
import urllib3
import certifi
import pdfkit
import weasyprint

def pdf2HTML(fileName, sourceHTML):
    try:
        pdfkit.from_string("<html>"+sourceHTML+"</html>", fileName)
    except:
        print("an error with " + fileName)


urls2 = []
cnnUrls = ['https://www.cnn.com/2021/04/15/us/derek-chauvin-trial-george-floyd-day-14/index.html']
voxUrls = ['https://www.vox.com/22385716/russia-sanctions-biden-cyber-ukraine']
req = urllib3.PoolManager(ca_certs=certifi.where())



for u in urls2:
    fileName = u.split('/')[-1]
    pdfName = fileName.split('.')[0]+".pdf"

    resp = req.request('GET', u)
    soup = BeautifulSoup(resp.data, 'html.parser')
    firstLevel = soup.find(class_='post-wrap')
    secondLevel = firstLevel.find_all('article')
    print(fileName + " " + pdfName)
    pdf2HTML(pdfName, str(secondLevel[0]))

    
for c in cnnUrls:
    fileName = c.split('/')[-2]+".html"
    pdfName = c.split('/')[-2] +".pdf"
    print(fileName + " " + pdfName)
    resp = req.request('GET', c)
    soup = BeautifulSoup(resp.data, 'html.parser')
    firstLevel = soup.find(class_='l-container')
    secondLevel = firstLevel.find_all(class_='zn-body__paragraph')
    print(secondLevel)
    htmlSource = "<html>"
    for s in secondLevel:
        print(type(s))
        htmlSource = htmlSource + str(s)
        
    htmlSource = htmlSource +"</html>"
    pdf2HTML(pdfName, htmlSource)

for v in voxUrls:
    fileName = v.split('/')[-1] + ".html"
    pdfName = v.split('/')[-1]  + ".pdf"
    print(fileName + " " + pdfName)
    resp = req.request('GET', v)
    soup = BeautifulSoup(resp.data, 'html.parser')
    firstLevel = soup.find(class_='c-entry-content')
    secondLevel = firstLevel.find_all('p')
    print(secondLevel)
    htmlSource = "<html>"
    for s in secondLevel:
        print(type(s))
        htmlSource = htmlSource + str(s)
        
    htmlSource = htmlSource +"</html>"
    pdf2HTML(pdfName, htmlSource)
    
    #xhtml2pdf
"""     pdfFile = open(pdfName, "w+b")
    pisa_create = pisa.CreatePDF(str(secondLevel[0]), 
                    dest=pdfName)
    pdfFile.close()  """
    
    #WeasyPrint
    #HTML(filename=fileName).write_pdf(pdfName)

    
    


