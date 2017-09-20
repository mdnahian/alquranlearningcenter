import pdfsplitter
import urllib


def quran_downloader():
	pdffile = urllib.URLopener()
	for i in range(1, 31):
		url = 'http://www.islamicnet.com/online_quran_pdf/Holy-Quran-Para-'+str(i)+'.pdf'
		pdffile.retrieve(url, "../web/static/resources/quran/paras/para-"+str(i)+".pdf")


def split_quran():
	count = 0
	for i in range(1, 31):
		name = "page"
		pdffile = "../web/static/resources/quran/paras/para-"+str(i)+".pdf"
		outputfolder = "../web/static/resources/quran/"

		count = pdfsplitter.split_pdf(name, pdffile, outputfolder, count)


split_quran()
