from unittest import TestCase

from apps.vnlp.training.alphabet import EnAlphabet
from apps.vnlp.training.raw_text_processor import RawTextProcessor


class TestRawTextProcessor(TestCase):
    def test_endings(self):
        text = RawTextProcessor.process_text(" McDonald's  trademark", EnAlphabet)
        self.assertEqual('mcdonald trademark', text)

    def test_numbers(self):
        text = RawTextProcessor.process_text("1) McDonald's  trademark ", EnAlphabet)
        self.assertEqual('', text)

        text = RawTextProcessor.process_text("1)MacDonald's  tradeermark", EnAlphabet)
        self.assertEqual('macdonald tradeermark', text)

    def test_repeated(self):
        text = RawTextProcessor.process_text("1)MacMacMacMacDonaldst's  trademarkmarkmark, nn", EnAlphabet)
        self.assertEqual('macmacmacmacdonaldst trademarkmarkmark', text)

    def test_logs(self):
        src = """
        INFO: To get higher rendering speed on JDK8 or later,
        Jun 12, 2020 3:16:20 PM org.apache.pdfbox.pdmodel.graphics.color.PDDeviceRGB suggestKCMS
        INFO:   use the option -Dsun.java2d.cmm=sun.java2d.cmm.kcms.KcmsServiceProvider
        Jun 12, 2020 3:16:20 PM org.apache.pdfbox.pdmodel.graphics.color.PDDeviceRGB suggestKCMS
        INFO:   or call System.setProperty("sun.java2d.cmm", "sun.java2d.cmm.kcms.KcmsServiceProvider")
        """
        text = RawTextProcessor.process_text(src, EnAlphabet)
        self.assertLess(len(text), len(src))
