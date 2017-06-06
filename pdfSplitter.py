from pyPdf import PdfFileWriter, PdfFileReader

inputpdf = PdfFileReader(open("web/static/resources/textbook.pdf", "rb"))

for i in xrange(inputpdf.numPages):
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    print i
    with open("web/static/resources/textbook/textbook%s.pdf" % i, "wb") as outputStream:
        output.write(outputStream)