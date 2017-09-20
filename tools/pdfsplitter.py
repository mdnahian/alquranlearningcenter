from pyPdf import PdfFileWriter, PdfFileReader

def split_pdf(name, pdffile, outputfolder, count):
	inputpdf = PdfFileReader(open(pdffile, "rb"))

	for i in xrange(inputpdf.numPages):
	    output = PdfFileWriter()
	    output.addPage(inputpdf.getPage(i))
	    print i
	    with open(outputfolder+name+"%s.pdf" % count, "wb") as outputStream:
	        output.write(outputStream)
	    count += 1
	return count
