# Name: CPF Generator for Burp Suite
# Version: 1.0
# Author: Rafael Cintra Lopes (obonito)

from burp import IBurpExtender, ITab
from javax.swing import JPanel, JTextArea, JButton, JRadioButton, ButtonGroup
from java.awt import FlowLayout
import random
from java.awt import Dimension

class BurpExtender(IBurpExtender, ITab):
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        self.stderr = callbacks.getStderr()

        callbacks.setExtensionName("CPF Generator for Burp Suite")

        self.tab = self.createTab()
        callbacks.addSuiteTab(self)

    def createTab(self):
        panel = JPanel()
        panel.setLayout(FlowLayout(FlowLayout.LEFT, 10, 10))

        self.cpf_display = JTextArea(1, 20)
        self.cpf_display.setEditable(False)
        self.cpf_display.setPreferredSize(Dimension(180, 25))
        panel.add(self.cpf_display)

        generate_button = JButton("Generate CPF", actionPerformed=self.generateCPF)
        panel.add(generate_button)

        self.with_punctuation = JRadioButton("With punctuation", True)
        self.no_punctuation = JRadioButton("No punctuation")

        group = ButtonGroup()
        group.add(self.with_punctuation)
        group.add(self.no_punctuation)

        panel.add(self.with_punctuation)
        panel.add(self.no_punctuation)

        return panel

    def generateCPF(self, event):
        cpf = self.generateRandomCPF()
 
        if self.with_punctuation.isSelected():
            formatted_cpf = self.formatCPFWithPunctuation(cpf)
        else:
            formatted_cpf = self.formatCPFWithoutPunctuation(cpf)
        
        self.cpf_display.setText(formatted_cpf)

    def generateRandomCPF(self):
        digits = [random.randint(0, 9) for _ in range(9)]
        d1 = self.calculateVerificationDigit(digits, [10, 9, 8, 7, 6, 5, 4, 3, 2])
        d2 = self.calculateVerificationDigit(digits + [d1], [11, 10, 9, 8, 7, 6, 5, 4, 3, 2])
        cpf = ''.join(map(str, digits)) + str(d1) + str(d2)

        return cpf

    def formatCPFWithPunctuation(self, cpf):
        return "{}.{}.{}-{}".format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])

    def formatCPFWithoutPunctuation(self, cpf):
        return cpf

    def calculateVerificationDigit(self, digits, multipliers):
        total = sum(d * m for d, m in zip(digits, multipliers))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    def getTabCaption(self):
        return "CPF Generator"

    def getUiComponent(self):
        return self.tab
