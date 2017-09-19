import pdfsplitter
import urllib


def quran_downloader():
	pdffile = urllib.URLopener()
	for i in range(1, 31):
		url = 'http://www.islamicnet.com/online_quran_pdf/Holy-Quran-Para-'+str(i)+'.pdf'
		pdffile.retrieve(url, "../web/static/resources/quran/paras/para-"+str(i)+".pdf")


def split_quran():
	for i in range(1, 31):
		name = "para"+str(i)+"-page"
		pdffile = "../web/static/resources/quran/paras/para-"+str(i)+".pdf"
		outputfolder = "../web/static/resources/quran/"

		pdfsplitter.split_pdf(name, pdffile, outputfolder)


split_quran()