from pyPdf import PdfFileWriter, PdfFileReader

def split_pdf(name, pdffile, outputfolder):
	inputpdf = PdfFileReader(open(pdffile, "rb"))

	for i in xrange(inputpdf.numPages):
	    output = PdfFileWriter()
	    output.addPage(inputpdf.getPage(i))
	    print i
	    with open(outputfolder+name+"%s.pdf" % i, "wb") as outputStream:
	        output.write(outputStream)