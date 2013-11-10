#!/usr/bin/python3
# Written by David Lareau on September 2012
# Generated a resume from xml to different output format (text, html, fodt [Flat ODT])
#
# Usage: ./resume2.py resume.xml 0 text > out_en.txt  (english, txt)
# Usage: ./resume2.py resume.xml 1 html > out_fr.html (french, html)
# Usage: ./resume2.py resume.xml 0 fodt > out_en.fodt (english, fodt)
# You can convert to pdf the fodt using: unoconv -f pdf mydocument.odt OR libreoffice --headless --invisible --convert-to pdf *.odt
#
# The language function splits each xml text on the pipe character, if there isn't anything at that language index it defaults to 0 (so phone number don't have to be repeated for each language)
# Example: <what>Developer|D&#233;veloppeur</what>
#
# About the code:
# Its a bit of mess where new lines are inserted, I've left it in an imperfect state.
# The fodt styles were mostly copy pasted from a libreoffice saveas fodt file. I did not attempt at compressing it much, nor have I tested if its all necessary.

import sys
import codecs
import locale
from lxml import objectify
#import xml.etree.ElementTree as etree
import getopt

# params
resumeFile = sys.argv[1]
languageIndex = int(sys.argv[2])
outputFormat = sys.argv[3]
web = sys.argv[4] == "True"
outputFileEncoding = sys.argv[5] # e.g. 'utf-8'

# Language spliter (splits on pipes '|', default to 0 if specified index isn't there)
def lang(o, index):
	s = str(o)
	parts = s.split('|')
	if index < len(parts):
		return parts[index]
	return parts[0]

# utils
def l(s):
	return lang(s, languageIndex)

def line():
	pln("")

def escape(s):
	s = s.replace("é", "&eacute;")
	s = s.replace("é", "&eacute;")
	s = s.replace("é", "&eacute;")
	s = s.replace("é", "&eacute;")
	s = s.replace("é", "&eacute;")
	s = s.replace("é", "&eacute;")
	s = s.replace("é", "&eacute;")
	s = s.replace("é", "&eacute;")
	s = s.replace("é", "&eacute;")
	s = s.replace("À", "&Agrave;")
	s = s.replace("Á", "&Aacute;")
	s = s.replace("Â", "&Acirc;")
	s = s.replace("Ã", "&Atilde;")
	s = s.replace("Ä", "&Auml;")
	s = s.replace("Å", "&Aring;")
	s = s.replace("Æ", "&AElig;")
	s = s.replace("Ç", "&Ccedil;")
	s = s.replace("È", "&Egrave;")
	s = s.replace("É", "&Eacute;")
	s = s.replace("Ê", "&Ecirc;")
	s = s.replace("Ë", "&Euml;")
	s = s.replace("Ì", "&Igrave;")
	s = s.replace("Í", "&Iacute;")
	s = s.replace("Î", "&Icirc;")
	s = s.replace("Ï", "&Iuml;")
	s = s.replace("Ð", "&ETH;")
	s = s.replace("Ñ", "&Ntilde;")
	s = s.replace("Ò", "&Ograve;")
	s = s.replace("Ó", "&Oacute;")
	s = s.replace("Ô", "&Ocirc;")
	s = s.replace("Õ", "&Otilde;")
	s = s.replace("Ö", "&Ouml;")
	s = s.replace("Ø", "&Oslash;")
	s = s.replace("Ù", "&Ugrave;")
	s = s.replace("Ú", "&Uacute;")
	s = s.replace("Û", "&Ucirc;")
	s = s.replace("Ü", "&Uuml;")
	s = s.replace("Ý", "&Yacute;")
	s = s.replace("Þ", "&THORN;")
	s = s.replace("ß", "&szlig;")
	s = s.replace("à", "&agrave;")
	s = s.replace("á", "&aacute;")
	s = s.replace("â", "&acirc;")
	s = s.replace("ã", "&atilde;")
	s = s.replace("ä", "&auml;")
	s = s.replace("å", "&aring;")
	s = s.replace("æ", "&aelig;")
	s = s.replace("ç", "&ccedil;")
	s = s.replace("è", "&egrave;")
	s = s.replace("é", "&eacute;")
	s = s.replace("ê", "&ecirc;")
	s = s.replace("ë", "&euml;")
	s = s.replace("ì", "&igrave;")
	s = s.replace("í", "&iacute;")
	s = s.replace("î", "&icirc;")
	s = s.replace("ï", "&iuml;")
	s = s.replace("ð", "&eth;")
	s = s.replace("ñ", "&ntilde;")
	s = s.replace("ò", "&ograve;")
	s = s.replace("ó", "&oacute;")
	s = s.replace("ô", "&ocirc;")
	s = s.replace("õ", "&otilde;")
	s = s.replace("ö", "&ouml;")
	s = s.replace("ø", "&oslash;")
	s = s.replace("ù", "&ugrave;")
	s = s.replace("ú", "&uacute;")
	s = s.replace("û", "&ucirc;")
	s = s.replace("ü", "&uuml;")
	s = s.replace("ý", "&yacute;")
	s = s.replace("þ", "&thorn;")
	s = s.replace("ÿ", "&yuml;")
	# bold
	s = s.replace("{BB}", "<b>")
	s = s.replace("{EB}", "</b>")
	return s

def escapeXML(s):
	s = s.replace("&", "&amp;")
	# bold
	s = s.replace("{BB}", '<text:span text:style-name="T9">')
	s = s.replace("{EB}", '</text:span>')
	return s

def escapeText(s):
	# absorb bold
	s = s.replace("{BB}", "")
	s = s.replace("{EB}", "")
	return s
	
def p(s):
	if outputFormat == 'text':
		s = escapeText(s)
	if outputFormat == 'html':
		s = escape(s)
	if outputFormat == 'fodt':
		s = escapeXML(s)
	#sys.stdout.write(s) # The default encoding used is different on Windows and Linux!! Lame.
	bytes = s.encode(outputFileEncoding)
	sys.stdout.buffer.write(bytes)

def pln(s):
	p(s + "\n")

tabCount = 0

def tinc():
	global tabCount
	tabCount += 1

def tdec():
	global tabCount
	tabCount -= 1

def tp(s):
	for i in range(0, tabCount):
		s = "\t" + s
	p(s)

def tpln(s, tdelta = 0):
	if tdelta < 0:
		tdec()
	for i in range(0, tabCount):
		s = "\t" + s
	pln(s)
	if tdelta > 0:
		tinc()

# formating
def dline(s = ""):
	if outputFormat == 'html':
		s += "<br/>"
	if outputFormat == 'fodt':
		s = '<text:p text:style-name="headerLine">' + s + '</text:p>'
	tpln(s)

def preResume(title):
	if outputFormat == 'html':
		tpln('<html>')
		tpln('<head>', 1)
		tpln('<title>' + title + '</title>')
		tpln('<style>')
		#p.italic {font-style:italic}
		#p.thick {font-weight:bold;}
		#font-size: medium, large, x-large, xx-large, small, x-small, xx-small
		#font-family: "serif", "sans-serif", "cursive", "fantasy", "monospace"
		tpln('body {')
		tpln(' font-family: "Times New Roman", serif;')
		tpln(' font-size: medium;')
		tpln(' font-style: normal;')
		tpln(' font-weight: normal;')
		tpln('}')
		tpln('.header {')
		tpln('}')
		tpln('.headerName {')
		tpln(' font-size: x-large;')
		tpln('}')
		tpln('.sectionTitle {')
		tpln(' font-size: large;')
		tpln(' text-decoration: underline;')
		tpln(' font-weight: bold;')
		tpln('}')
		tpln('.section {')
		tpln('}')
		tpln('.first {')
		tpln(' font-weight: bold;')
		tpln('}')
		tpln('.second {')
		tpln(' font-style: italic;')
		tpln('}')
		tpln('ul {')
		#tpln(' margin-top: 0;')    # There seems to be a bug, at least in chrome, where the first ul of a section still has a top margin
		#tpln(' margin-bottom: 0;')
		tpln('}')
		tpln('li {')
		tpln('}')
		tpln('</style>')
		tpln('</head>', -1)
		tpln('<body>', 1)
	if outputFormat == 'fodt':
		# I simply saved a mostly empty fodt with open office and copied all the junk it generates
		tpln('<?xml version="1.0" encoding="UTF-8"?>')
		tpln('')
		tpln('<office:document xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0" xmlns:ooo="http://openoffice.org/2004/office" xmlns:ooow="http://openoffice.org/2004/writer" xmlns:oooc="http://openoffice.org/2004/calc" xmlns:dom="http://www.w3.org/2001/xml-events" xmlns:xforms="http://www.w3.org/2002/xforms" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:rpt="http://openoffice.org/2005/report" xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:grddl="http://www.w3.org/2003/g/data-view#" xmlns:tableooo="http://openoffice.org/2009/table" xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0" xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0" xmlns:css3t="http://www.w3.org/TR/css3-text/" office:version="1.2" office:mimetype="application/vnd.oasis.opendocument.text">')
		tpln(' <office:meta><meta:creation-date>2012-09-20T12:40:38</meta:creation-date><meta:document-statistic meta:table-count="0" meta:image-count="0" meta:object-count="0" meta:page-count="1" meta:paragraph-count="2" meta:word-count="2" meta:character-count="8" meta:non-whitespace-character-count="8"/><dc:date>2012-09-20T12:41:09</dc:date><meta:editing-duration>P0D</meta:editing-duration><meta:editing-cycles>1</meta:editing-cycles><meta:generator>LibreOffice/3.5$Linux_X86_64 LibreOffice_project/350m1$Build-2</meta:generator></office:meta>')
		tpln(' <office:settings>')
		tpln('  <config:config-item-set config:name="ooo:view-settings">')
		tpln('   <config:config-item config:name="ViewAreaTop" config:type="long">0</config:config-item>')
		tpln('   <config:config-item config:name="ViewAreaLeft" config:type="long">0</config:config-item>')
		tpln('   <config:config-item config:name="ViewAreaWidth" config:type="long">18404</config:config-item>')
		tpln('   <config:config-item config:name="ViewAreaHeight" config:type="long">20122</config:config-item>')
		tpln('   <config:config-item config:name="ShowRedlineChanges" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="InBrowseMode" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item-map-indexed config:name="Views">')
		tpln('    <config:config-item-map-entry>')
		tpln('     <config:config-item config:name="ViewId" config:type="string">view2</config:config-item>')
		tpln('     <config:config-item config:name="ViewLeft" config:type="long">3002</config:config-item>')
		tpln('     <config:config-item config:name="ViewTop" config:type="long">3976</config:config-item>')
		tpln('     <config:config-item config:name="VisibleLeft" config:type="long">0</config:config-item>')
		tpln('     <config:config-item config:name="VisibleTop" config:type="long">0</config:config-item>')
		tpln('     <config:config-item config:name="VisibleRight" config:type="long">18403</config:config-item>')
		tpln('     <config:config-item config:name="VisibleBottom" config:type="long">20121</config:config-item>')
		tpln('     <config:config-item config:name="ZoomType" config:type="short">0</config:config-item>')
		tpln('     <config:config-item config:name="ViewLayoutColumns" config:type="short">0</config:config-item>')
		tpln('     <config:config-item config:name="ViewLayoutBookMode" config:type="boolean">false</config:config-item>')
		tpln('     <config:config-item config:name="ZoomFactor" config:type="short">100</config:config-item>')
		tpln('     <config:config-item config:name="IsSelectedFrame" config:type="boolean">false</config:config-item>')
		tpln('    </config:config-item-map-entry>')
		tpln('   </config:config-item-map-indexed>')
		tpln('  </config:config-item-set>')
		tpln('  <config:config-item-set config:name="ooo:configuration-settings">')
		tpln('   <config:config-item config:name="PrintTables" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="AddParaTableSpacingAtStart" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="ChartAutoUpdate" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="IsLabelDocument" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="MathBaselineAlignment" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="OutlineLevelYieldsNumbering" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="PrintLeftPages" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="AlignTabStopPosition" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="DoNotJustifyLinesWithManualBreak" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="PrintTextPlaceholder" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="UseOldNumbering" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="PrintProspectRTL" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="ProtectForm" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="CurrentDatabaseCommand" config:type="string"/>')
		tpln('   <config:config-item config:name="PrintBlackFonts" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="SmallCapsPercentage66" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="CharacterCompressionType" config:type="short">0</config:config-item>')
		tpln('   <config:config-item config:name="PrintControls" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="PrintHiddenText" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="IsKernAsianPunctuation" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="UseFormerTextWrapping" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="PrintProspect" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="PrintEmptyPages" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="UnbreakableNumberings" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="UseFormerObjectPositioning" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="PrintReversed" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="TabsRelativeToIndent" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="TableRowKeep" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="ConsiderTextWrapOnObjPos" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="PrintRightPages" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="PrintPaperFromSetup" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="AddFrameOffsets" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="UpdateFromTemplate" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="AddParaSpacingToTableCells" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="PrintSingleJobs" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="AddExternalLeading" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="PrinterIndependentLayout" config:type="string">high-resolution</config:config-item>')
		tpln('   <config:config-item config:name="LinkUpdateMode" config:type="short">1</config:config-item>')
		tpln('   <config:config-item config:name="PrintAnnotationMode" config:type="short">0</config:config-item>')
		tpln('   <config:config-item config:name="UseOldPrinterMetrics" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="RedlineProtectionKey" config:type="base64Binary"/>')
		tpln('   <config:config-item config:name="PrinterName" config:type="string"/>')
		tpln('   <config:config-item config:name="CollapseEmptyCellPara" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="PrinterSetup" config:type="base64Binary"/>')
		tpln('   <config:config-item config:name="IgnoreFirstLineIndentInNumbering" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="InvertBorderSpacing" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="PrintPageBackground" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="DoNotCaptureDrawObjsOnPage" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="TabOverflow" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="ApplyUserData" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="TabAtLeftIndentForParagraphsInList" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="UnxForceZeroExtLeading" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="SaveVersionOnClose" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="PrintFaxName" config:type="string"/>')
		tpln('   <config:config-item config:name="PrintDrawings" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="AddParaTableSpacing" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="LoadReadonly" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="PrintGraphics" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="FieldAutoUpdate" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="AllowPrintJobCancel" config:type="boolean">true</config:config-item>')
		tpln('   <config:config-item config:name="SaveGlobalDocumentLinks" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="CurrentDatabaseDataSource" config:type="string"/>')
		tpln('   <config:config-item config:name="UseFormerLineSpacing" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="IgnoreTabsAndBlanksForLineCalculation" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="CurrentDatabaseCommandType" config:type="int">0</config:config-item>')
		tpln('   <config:config-item config:name="DoNotResetParaAttrsForNumFont" config:type="boolean">false</config:config-item>')
		tpln('   <config:config-item config:name="ClipAsCharacterAnchoredWriterFlyFrames" config:type="boolean">false</config:config-item>')
		tpln('  </config:config-item-set>')
		tpln(' </office:settings>')
		tpln(' <office:scripts>')
		tpln('  <office:script script:language="ooo:Basic">')
		tpln('   <ooo:libraries xmlns:ooo="http://openoffice.org/2004/office" xmlns:xlink="http://www.w3.org/1999/xlink"/>')
		tpln('  </office:script>')
		tpln(' </office:scripts>')
		tpln(' <office:font-face-decls>')
		tpln('  <style:font-face style:name="FreeSans1" svg:font-family="FreeSans" style:font-family-generic="swiss"/>')
		tpln('  <style:font-face style:name="Times New Roman" svg:font-family="Times New Roman" style:font-family-generic="roman" style:font-pitch="variable"/>')
		tpln('  <style:font-face style:name="Arial" svg:font-family="Arial" style:font-family-generic="swiss" style:font-pitch="variable"/>')
		tpln('  <style:font-face style:name="Droid Sans" svg:font-family="Droid Sans" style:font-family-generic="system" style:font-pitch="variable"/>')
		tpln('  <style:font-face style:name="FreeSans" svg:font-family="FreeSans" style:font-family-generic="system" style:font-pitch="variable"/>')
		tpln(' </office:font-face-decls>')
		tpln(' <office:styles>')
		tpln('  <style:default-style style:family="graphic">')
		tpln('   <style:graphic-properties svg:stroke-color="#808080" draw:fill-color="#cfe7f5" fo:wrap-option="no-wrap" draw:shadow-offset-x="0.3cm" draw:shadow-offset-y="0.3cm" draw:start-line-spacing-horizontal="0.283cm" draw:start-line-spacing-vertical="0.283cm" draw:end-line-spacing-horizontal="0.283cm" draw:end-line-spacing-vertical="0.283cm" style:flow-with-text="false"/>')
		tpln('   <style:paragraph-properties style:text-autospace="ideograph-alpha" style:line-break="strict" style:writing-mode="lr-tb" style:font-independent-line-spacing="false">')
		tpln('    <style:tab-stops/>')
		tpln('   </style:paragraph-properties>')
		tpln('   <style:text-properties style:use-window-font-color="true" fo:font-size="12pt" fo:language="en" fo:country="CA" style:letter-kerning="true" style:font-size-asian="10.5pt" style:language-asian="zh" style:country-asian="CN" style:font-size-complex="12pt" style:language-complex="hi" style:country-complex="IN"/>')
		tpln('  </style:default-style>')
		tpln('  <style:default-style style:family="paragraph">')
		tpln('   <style:paragraph-properties fo:hyphenation-ladder-count="no-limit" style:text-autospace="ideograph-alpha" style:punctuation-wrap="hanging" style:line-break="strict" style:tab-stop-distance="1.251cm" style:writing-mode="page"/>')
		tpln('   <style:text-properties style:use-window-font-color="true" style:font-name="Times New Roman" fo:font-size="12pt" fo:language="en" fo:country="CA" style:letter-kerning="true" style:font-name-asian="Droid Sans" style:font-size-asian="10.5pt" style:language-asian="zh" style:country-asian="CN" style:font-name-complex="FreeSans" style:font-size-complex="12pt" style:language-complex="hi" style:country-complex="IN" fo:hyphenate="false" fo:hyphenation-remain-char-count="2" fo:hyphenation-push-char-count="2"/>')
		tpln('  </style:default-style>')
		tpln('  <style:default-style style:family="table">')
		tpln('   <style:table-properties table:border-model="collapsing"/>')
		tpln('  </style:default-style>')
		tpln('  <style:default-style style:family="table-row">')
		tpln('   <style:table-row-properties fo:keep-together="auto"/>')
		tpln('  </style:default-style>')
		tpln('  <style:style style:name="Standard" style:family="paragraph" style:class="text"/>')
		tpln('  <style:style style:name="Heading" style:family="paragraph" style:parent-style-name="Standard" style:next-style-name="Text_20_body" style:class="text">')
		tpln('   <style:paragraph-properties fo:margin-top="0.423cm" fo:margin-bottom="0.212cm" fo:keep-with-next="always"/>')
		tpln('   <style:text-properties style:font-name="Arial" fo:font-size="14pt" style:font-name-asian="Droid Sans" style:font-size-asian="14pt" style:font-name-complex="FreeSans" style:font-size-complex="14pt"/>')
		tpln('  </style:style>')
		tpln('  <style:style style:name="Text_20_body" style:display-name="Text body" style:family="paragraph" style:parent-style-name="Standard" style:class="text">')
		tpln('   <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0.212cm"/>')
		tpln('  </style:style>')

		tpln('    <style:style style:name="Table_20_Contents" style:display-name="Table Contents" style:family="paragraph" style:parent-style-name="Standard" style:class="extra">')
		tpln('     <style:paragraph-properties text:number-lines="false" text:line-number="0"/>')
		tpln('    </style:style>')

		tpln('  <style:style style:name="List" style:family="paragraph" style:parent-style-name="Text_20_body" style:class="list">')
		tpln('   <style:text-properties style:font-size-asian="12pt" style:font-name-complex="FreeSans1"/>')
		tpln('  </style:style>')
		tpln('  <style:style style:name="Caption" style:family="paragraph" style:parent-style-name="Standard" style:class="extra">')
		tpln('   <style:paragraph-properties fo:margin-top="0.212cm" fo:margin-bottom="0.212cm" text:number-lines="false" text:line-number="0"/>')
		tpln('   <style:text-properties fo:font-size="12pt" fo:font-style="italic" style:font-size-asian="12pt" style:font-style-asian="italic" style:font-name-complex="FreeSans1" style:font-size-complex="12pt" style:font-style-complex="italic"/>')
		tpln('  </style:style>')
		tpln('  <style:style style:name="Index" style:family="paragraph" style:parent-style-name="Standard" style:class="index">')
		tpln('   <style:paragraph-properties text:number-lines="false" text:line-number="0"/>')
		tpln('   <style:text-properties style:font-size-asian="12pt" style:font-name-complex="FreeSans1"/>')
		tpln('  </style:style>')
		tpln('  <text:outline-style style:name="Outline">')
		tpln('   <text:outline-level-style text:level="1" style:num-format="">')
		tpln('    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">')
		tpln('     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="0.762cm" fo:text-indent="-0.762cm" fo:margin-left="0.762cm"/>')
		tpln('    </style:list-level-properties>')
		tpln('   </text:outline-level-style>')
		tpln('   <text:outline-level-style text:level="2" style:num-format="">')
		tpln('    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">')
		tpln('     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="1.016cm" fo:text-indent="-1.016cm" fo:margin-left="1.016cm"/>')
		tpln('    </style:list-level-properties>')
		tpln('   </text:outline-level-style>')
		tpln('   <text:outline-level-style text:level="3" style:num-format="">')
		tpln('    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">')
		tpln('     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="1.27cm" fo:text-indent="-1.27cm" fo:margin-left="1.27cm"/>')
		tpln('    </style:list-level-properties>')
		tpln('   </text:outline-level-style>')
		tpln('   <text:outline-level-style text:level="4" style:num-format="">')
		tpln('    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">')
		tpln('     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="1.524cm" fo:text-indent="-1.524cm" fo:margin-left="1.524cm"/>')
		tpln('    </style:list-level-properties>')
		tpln('   </text:outline-level-style>')
		tpln('   <text:outline-level-style text:level="5" style:num-format="">')
		tpln('    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">')
		tpln('     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="1.778cm" fo:text-indent="-1.778cm" fo:margin-left="1.778cm"/>')
		tpln('    </style:list-level-properties>')
		tpln('   </text:outline-level-style>')
		tpln('   <text:outline-level-style text:level="6" style:num-format="">')
		tpln('    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">')
		tpln('     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="2.032cm" fo:text-indent="-2.032cm" fo:margin-left="2.032cm"/>')
		tpln('    </style:list-level-properties>')
		tpln('   </text:outline-level-style>')
		tpln('   <text:outline-level-style text:level="7" style:num-format="">')
		tpln('    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">')
		tpln('     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="2.286cm" fo:text-indent="-2.286cm" fo:margin-left="2.286cm"/>')
		tpln('    </style:list-level-properties>')
		tpln('   </text:outline-level-style>')
		tpln('   <text:outline-level-style text:level="8" style:num-format="">')
		tpln('    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">')
		tpln('     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="2.54cm" fo:text-indent="-2.54cm" fo:margin-left="2.54cm"/>')
		tpln('    </style:list-level-properties>')
		tpln('   </text:outline-level-style>')
		tpln('   <text:outline-level-style text:level="9" style:num-format="">')
		tpln('    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">')
		tpln('     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="2.794cm" fo:text-indent="-2.794cm" fo:margin-left="2.794cm"/>')
		tpln('    </style:list-level-properties>')
		tpln('   </text:outline-level-style>')
		tpln('   <text:outline-level-style text:level="10" style:num-format="">')
		tpln('    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">')
		tpln('     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="3.048cm" fo:text-indent="-3.048cm" fo:margin-left="3.048cm"/>')
		tpln('    </style:list-level-properties>')
		tpln('   </text:outline-level-style>')
		tpln('  </text:outline-style>')
		tpln('  <text:notes-configuration text:note-class="footnote" style:num-format="1" text:start-value="0" text:footnotes-position="page" text:start-numbering-at="document"/>')
		tpln('  <text:notes-configuration text:note-class="endnote" style:num-format="i" text:start-value="0"/>')
		tpln('  <text:linenumbering-configuration text:number-lines="false" text:offset="0.499cm" style:num-format="1" text:number-position="left" text:increment="5"/>')
		tpln(' </office:styles>')
		tpln(' <office:automatic-styles>')

		# Styles
		tpln('  <style:style style:name="headerName" style:family="paragraph" style:parent-style-name="Standard" style:master-page-name="">')
		tpln('   <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0cm" fo:line-height="100%" fo:text-align="center" style:justify-single-word="false" style:page-number="auto" fo:background-color="transparent" style:writing-mode="lr-tb">')
		tpln('    <style:background-image/>')
		tpln('   </style:paragraph-properties>')
		tpln('   <style:text-properties style:font-name="Times New Roman" fo:font-size="16pt" fo:language="fr" fo:country="CA" fo:font-style="normal" fo:font-weight="normal" fo:background-color="transparent" style:language-asian="zxx" style:country-asian="none" style:font-name-complex="Times New Roman" style:font-size-complex="16pt"/>')
		tpln('  </style:style>')
		tpln('  <style:style style:name="headerLine" style:family="paragraph" style:parent-style-name="Standard">')
		tpln('   <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0cm" fo:line-height="100%" fo:text-align="center" style:justify-single-word="false" fo:background-color="transparent" style:writing-mode="lr-tb">')
		tpln('    <style:background-image/>')
		tpln('   </style:paragraph-properties>')
		tpln('   <style:text-properties style:font-name="Times New Roman" fo:language="fr" fo:country="CA" fo:font-style="normal" fo:font-weight="normal" fo:background-color="transparent" style:language-asian="zxx" style:country-asian="none" style:font-name-complex="Times New Roman"/>')
		tpln('  </style:style>')
		tpln('  <style:style style:name="section" style:family="paragraph" style:parent-style-name="Standard">')
		tpln('   <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0.212cm" style:writing-mode="lr-tb"/>')
		tpln('   <style:text-properties style:font-name="Times New Roman" fo:font-size="14pt" fo:language="fr" fo:country="CA" style:text-underline-style="solid" style:text-underline-width="auto" style:text-underline-color="font-color" fo:font-weight="bold" style:language-asian="zxx" style:country-asian="none" style:font-name-complex="Times New Roman" style:font-size-complex="14pt" style:font-weight-complex="bold"/>')
		tpln('  </style:style>')
		tpln('  <style:style style:name="first" style:family="paragraph" style:parent-style-name="Standard">')
		tpln('   <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0.212cm" style:writing-mode="lr-tb"/>')
		tpln('   <style:text-properties style:font-name="Times New Roman" fo:language="fr" fo:country="CA" fo:font-weight="bold" style:language-asian="zxx" style:country-asian="none" style:font-name-complex="Times New Roman" style:font-weight-complex="bold"/>')
		tpln('  </style:style>')
		tpln('  <style:style style:name="second" style:family="paragraph" style:parent-style-name="Standard">')
		tpln('   <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0.212cm" style:writing-mode="lr-tb"/>')
		tpln('   <style:text-properties style:font-name="Times New Roman" fo:language="fr" fo:country="CA" fo:font-style="italic" style:language-asian="zxx" style:country-asian="none" style:font-name-complex="Times New Roman" style:font-style-complex="italic"/>')
		tpln('  </style:style>')
		tpln('  <style:style style:name="listItem" style:family="paragraph" style:parent-style-name="Standard">')
		tpln('   <style:paragraph-properties fo:margin-left="1.247cm" fo:margin-right="0cm" fo:text-indent="-0.499cm" style:auto-text-indent="false" style:writing-mode="lr-tb">')
		tpln('    <style:tab-stops/>')
		tpln('   </style:paragraph-properties>')
		tpln('   <style:text-properties style:font-name="Times New Roman" fo:language="fr" fo:country="CA" style:language-asian="zxx" style:country-asian="none" style:font-name-complex="Times New Roman"/>')
		tpln('  </style:style>')
		tpln('  <style:style style:name="T8" style:family="text">')
		tpln('   <style:text-properties fo:font-style="italic" style:font-style-complex="italic"/>')
		tpln('  </style:style>')
		tpln('  <style:style style:name="T82" style:family="paragraph" style:parent-style-name="Standard">')
		tpln('   <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0.212cm" style:writing-mode="lr-tb"/>')
		tpln('   <style:text-properties style:font-name="Times New Roman" fo:language="fr" fo:country="CA" style:language-asian="zxx" style:country-asian="none" style:font-name-complex="Times New Roman" fo:font-style="italic" style:font-style-complex="italic"/>')
		tpln('  </style:style>')
		tpln('  <style:style style:name="T9" style:family="text">')
		tpln('   <style:text-properties fo:font-weight="bold" style:font-weight-complex="bold"/>')
		tpln('  </style:style>')
		tpln('  <style:style style:name="P19" style:family="paragraph" style:parent-style-name="Standard">')
		tpln('   <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0.212cm" style:writing-mode="lr-tb"/>')
		tpln('   <style:text-properties style:font-name="Times New Roman" fo:font-size="10pt" fo:language="fr" fo:country="CA" style:font-size-asian="10pt" style:language-asian="zxx" style:country-asian="none" style:font-name-complex="Times New Roman" style:font-size-complex="10pt"/>')
		tpln('  </style:style>')
		tpln('  <style:style style:name="P6" style:family="paragraph" style:parent-style-name="Standard">')
		tpln('   <style:paragraph-properties fo:margin-left="1.247cm" fo:margin-right="0cm" fo:text-indent="-0.499cm" style:auto-text-indent="false" style:writing-mode="lr-tb">')
		tpln('    <style:tab-stops/>')
		tpln('   </style:paragraph-properties>')
		tpln('   <style:text-properties style:font-name="Times New Roman" fo:font-size="10pt" fo:language="fr" fo:country="CA" style:font-size-asian="10pt" style:language-asian="zxx" style:country-asian="none" style:font-name-complex="Times New Roman" style:font-size-complex="10pt"/>')
		tpln('  </style:style>')

		# Page break style
		tpln('  <style:style style:name="Table1" style:family="table">')
		tpln('   <style:table-properties style:width="17.59cm" fo:break-before="page" table:align="margins" style:writing-mode="lr-tb"/>')
		tpln('  </style:style>')
		tpln('  <style:style style:name="Table1.A" style:family="table-column">')
		tpln('   <style:table-column-properties style:column-width="8.793cm" style:rel-column-width="32760*"/>')
		tpln('  </style:style>')
		tpln('  <style:style style:name="Table1.B" style:family="table-column">')
		tpln('   <style:table-column-properties style:column-width="8.797cm" style:rel-column-width="32775*"/>')
		tpln('  </style:style>')
		tpln('    <style:style style:name="P3" style:family="paragraph" style:parent-style-name="Standard">')
		tpln('     <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0cm" fo:line-height="100%" fo:text-align="end" style:justify-single-word="false" fo:background-color="transparent" style:writing-mode="lr-tb">')
		tpln('      <style:background-image/>')
		tpln('     </style:paragraph-properties>')
		tpln('     <style:text-properties style:font-name="Times New Roman" fo:language="fr" fo:country="CA" fo:font-style="normal" fo:font-weight="normal" fo:background-color="transparent" style:language-asian="zxx" style:country-asian="none" style:font-name-complex="Times New Roman"/>')
		tpln('    </style:style>')

		tpln('  <style:page-layout style:name="pm1">')
		tpln('   <style:page-layout-properties fo:page-width="21.59cm" fo:page-height="27.94cm" style:num-format="1" style:print-orientation="portrait" fo:margin="2cm" fo:margin-top="2cm" fo:margin-bottom="2cm" fo:margin-left="2cm" fo:margin-right="2cm" style:writing-mode="lr-tb" style:footnote-max-height="0cm">')
		tpln('    <style:footnote-sep style:width="0.018cm" style:distance-before-sep="0.101cm" style:distance-after-sep="0.101cm" style:line-style="solid" style:adjustment="left" style:rel-width="25%" style:color="#000000"/>')
		tpln('   </style:page-layout-properties>')
		tpln('   <style:header-style/>')
		tpln('   <style:footer-style/>')
		tpln('  </style:page-layout>')
		tpln(' </office:automatic-styles>')
		tpln(' <office:master-styles>')
		tpln('  <style:master-page style:name="Standard" style:page-layout-name="pm1"/>')
		tpln(' </office:master-styles>')
		tpln(' <office:body>')
		tpln('  <office:text>')
		tpln('   <text:sequence-decls>')
		tpln('    <text:sequence-decl text:display-outline-level="0" text:name="Illustration"/>')
		tpln('    <text:sequence-decl text:display-outline-level="0" text:name="Table"/>')
		tpln('    <text:sequence-decl text:display-outline-level="0" text:name="Text"/>')
		tpln('    <text:sequence-decl text:display-outline-level="0" text:name="Drawing"/>')
		tpln('   </text:sequence-decls>')

def postResume():
	if outputFormat == 'html':
		tpln('</body>', -1)
		tpln('</html>')
	if outputFormat == 'fodt':
		tpln('  </office:text>')
		tpln(' </office:body>')
		tpln('</office:document>')

def preHeader():
	if outputFormat == 'html':
		tpln('<p class="header">', 1)

def headerName(name):
	if outputFormat == 'text':
		tpln(name)
	if outputFormat == 'html':
		tpln('<span class="headerName">' + name + '</span><br/>')
	if outputFormat == 'fodt':
		tpln('<text:p text:style-name="headerName">' + name + '</text:p>')

def postHeader():
	if outputFormat == 'text':
		line()
	if outputFormat == 'html':
		tpln('</p>', -1)
		line()
	if outputFormat == 'fodt':
		tpln('<text:p text:style-name="Standard"/>')

def preSection(title):
	if outputFormat == 'text':
		tpln(title)
	if outputFormat == 'html':
		tpln('<p class="sectionTitle">' + title + '</p>')
		tpln('<p class="section">', 1)
	if outputFormat == 'fodt':
		tpln('<text:p text:style-name="section">' + title + '</text:p>')

def postSection():
	if outputFormat == 'text':
		line()
	if outputFormat == 'html':
		tpln('</p>', -1)
		line()
	#if outputFormat == 'fodt':
	#	tpln('<text:p text:style-name="Standard"/>')

def preListSection(title):
	if outputFormat == 'text':
		tpln(title)
		line()
	if outputFormat == 'html':
		tpln('<p class="sectionTitle">' + title + '</p>')
		tpln('<p class="section">', 1)
	if outputFormat == 'fodt':
		tpln('<text:p text:style-name="section">' + title + '</text:p>')

def postListSection():
	if outputFormat == 'text':
		line()
	if outputFormat == 'html':
		tpln('</p>', -1)
		line()
	#if outputFormat == 'fodt':
	#	tpln('<text:p text:style-name="Standard"/>')

def preList():
	if outputFormat == 'html':
		tpln('<ul>', 1)

def postList():
	if outputFormat == 'html':
		tpln('</ul>', -1)
	if outputFormat == 'fodt':
		tpln('<text:p text:style-name="Standard"/>')

def listItem(item, minor):
	if outputFormat == 'text':
		tpln('- ' + item)
	if outputFormat == 'html':
		tpln('<li>' + item + '</li>')
	if outputFormat == 'fodt':
		if minor:
			tpln('<text:p text:style-name="P6">•<text:tab/>' + item + '</text:p>')
		else:
			tpln('<text:p text:style-name="listItem">•<text:tab/>' + item + '</text:p>')

def first(s, minor, image=None):
	if outputFormat == 'text':
		tpln(s)
	if outputFormat == 'html':
		if image != None:
			tpln('<img src="logo/' + image + '" height="37" align="left" />')
		tpln('<span class="first">' + s + '</span><br/>')
	if outputFormat == 'fodt':
		if minor:
			tpln('<text:p text:style-name="P19"><text:span text:style-name="T9">' + s + ' </text:span>')
		else:
			tpln('<text:p text:style-name="first">' + s + '</text:p>')

def second(s, minor, sameLine=False, image=None):
	if outputFormat == 'text':
		tpln(s)
	if outputFormat == 'html':
		tp('<span class="second">' + s + '</span>')
		if image != None:
			tpln('<br clear="left"/>')
		else:
			tpln('<br/>')
	if outputFormat == 'fodt':
		if minor:
			if sameLine:
				tpln('<text:span text:style-name="T8">' + s + '</text:span></text:p>')
			else:
				tpln('<text:span text:style-name="T8"><text:line-break/>' + s + '</text:span></text:p>')
			#tpln('</text:p><text:p text:style-name="T82">' + s + '</text:p>')
		else:
			tpln('<text:p text:style-name="second">' + s + '</text:p>')

def preSectionItem():
	if outputFormat == 'text':
		line()

def postSectionItem():
	#if outputFormat == 'text':
	#	line()
	#if outputFormat == 'fodt':
	#	tpln('<text:p text:style-name="Standard"/>')
	return None

def pageBreak(name, phone):
	if outputFormat == 'fodt':
		if phone == None: phone = ""
		tpln('   <table:table table:name="Table1" table:style-name="Table1">')
		tpln('    <table:table-column table:style-name="Table1.A"/>')
		tpln('    <table:table-column table:style-name="Table1.B"/>')
		tpln('    <table:table-row>')
		tpln('     <table:table-cell office:value-type="string">')
		tpln('      <text:p text:style-name="Table_20_Contents">' + name + '</text:p>')
		tpln('     </table:table-cell>')
		tpln('     <table:table-cell office:value-type="string">')
		tpln('      <text:p text:style-name="P3">' + phone + '</text:p>')
		tpln('     </table:table-cell>')
		tpln('    </table:table-row>')
		tpln('   </table:table>')
		tpln('<text:p text:style-name="Standard"/>')

f = open(resumeFile, 'r')
tree = objectify.parse(f)
resume = tree.getroot()

preResume(l(resume.attrib["title"] + " - " + l(resume.id.name)))

# Header
preHeader()
headerName(l(resume.id.name))
if not web: dline(l(resume.id.address.street))
if not web: dline(l(resume.id.address.city) + " (" + l(resume.id.address.province) + ")  " + l(resume.id.address.postal))
if web: dline(l(resume.id.address.city) + " (" + l(resume.id.address.province) + ")")
dline(l(resume.id.email))
if not web: dline(l(resume.id.phone))
postHeader()

# Education
preSection(l(resume.education.attrib["title"]))
for degree in resume.education.degree:
	preSectionItem()
	first(l(degree.name), False)
	second(l(degree.where) + ", " + l(degree.to) + " (" + l(degree.duration) + ")", False)
	preList()
	for note in degree.note:
		listItem(l(note), False)
	postList()
	postSectionItem()
postSection()

# Lists (Skills, Personal Interests)
for items in resume.list:
	preListSection(l(items.attrib["title"]))
	preList()
	for item in items.item:
		listItem(l(item), False)
	postList()
	postListSection()

# Page Break
pageBreak(l(resume.id.name), None if web else l(resume.id.phone))

# Work Experience
preSection(l(resume.experience.attrib["title"]))
for work in resume.experience.work:
	preSectionItem()
	minor = hasattr(work, 'minor')
	sameLine = hasattr(work, 'sameLine')
	first(l(work.name) + ", " + l(work.where), minor, work.image if hasattr(work, 'image') else None)
	second(l(work.what) + ", " + l(work.when), minor, sameLine, work.image if hasattr(work, 'image') else None)
	preList()
	for exp in work.exp:
		listItem(l(exp), minor)
	postList()
	# Note: no support for minor with more lists
	if hasattr(work, 'more'):
		for more in work.more:
			second(l(more.what) + ", " + l(more.when), False) 
			preList()
			for exp in more.exp:
				listItem(l(exp), False)
			postList()
	postSectionItem()
postSection()

postResume()

f.close()


