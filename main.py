"""Hang Me Not - A hangman game"""

import wx
from random import choice
from string import ascii_uppercase
from re import finditer


class Hangman(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Hang Me Not', size=(500, 500),
                         style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.InitWords()
        self.InitUI()
        self.Reset()

    def InitWords(self):
        with open('res\\words.dat', 'r') as file:
            self.loaded_words = file.read().splitlines()

        self.words = self.loaded_words

    def InitUI(self):
        pnl = wx.Panel(self)
        bold_font = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        self.word_txt = wx.StaticText(pnl, pos=(0, 50), size=(self.GetSize()[0], -1), style=wx.ALIGN_CENTER)
        self.word_txt.SetFont(bold_font)

        self.img = wx.StaticBitmap(pnl, pos=(150, 225))

        # Play State
        start_pos_x = 90
        start_pos_y = 130
        pos_x = start_pos_x
        pos_y = start_pos_y
        chars_in_row = 0
        self.list_char_btn = []
        for char in ascii_uppercase:
            char_btn = wx.Button(pnl, label=char, pos=(pos_x, pos_y), size=(20, -1))
            char_btn.Bind(wx.EVT_BUTTON, self.OnCharPress)
            self.list_char_btn.append(char_btn)

            pos_x += 25
            chars_in_row += 1

            if chars_in_row == 13:
                pos_x = start_pos_x
                pos_y += 30
                chars_in_row = 0

        # End State
        self.end_state_txt = wx.StaticText(pnl, pos=(0, 125), size=(self.GetSize()[0], -1), style=wx.ALIGN_CENTER)
        self.end_state_txt.SetFont(bold_font)

        self.play_again_btn = wx.Button(pnl, label='Play Again', pos=(170, 175))
        self.play_again_btn.Bind(wx.EVT_BUTTON, self.OnPlayAgain)

        self.quit_btn = wx.Button(pnl, label='Quit', pos=(260, 175))
        self.quit_btn.Bind(wx.EVT_BUTTON, self.OnQuit)

        self.SetIcon(wx.Icon('icon\\hang_me_not.ico', wx.BITMAP_TYPE_ICO))
        self.Center()
        self.Show()

    def Reset(self):
        self.ChooseWord()
        self.indexes = {0, len(self.word) - 1}
        self.lives = 6

        self.UpdateWordText()
        self.UpdateImage(0)
        self.SwitchGameState(play_state=True)

    def ChooseWord(self):
        self.word = choice(self.words)
        self.words.remove(self.word)
        self.word = self.word.upper()

        if not self.words:
            self.words = self.loaded_words

    def UpdateWordText(self):
        word_txt_label = ''

        for i in range(len(self.word)):
            if i in self.indexes:
                word_txt_label += self.word[i]
            else:
                word_txt_label += '_'

            word_txt_label += ' '

        self.word_txt.SetLabel(word_txt_label[:-1])

    def UpdateImage(self, index):
        self.img.SetBitmap(wx.Bitmap(f'res\\img\\hangman_{index}.png'))

    def SwitchGameState(self, play_state):
        end_state = not play_state

        for char_btn in self.list_char_btn:
            char_btn.Show(play_state)

        self.end_state_txt.Show(end_state)
        self.play_again_btn.Show(end_state)
        self.quit_btn.Show(end_state)

    def EndGame(self, win):
        self.SwitchGameState(play_state=False)
        self.end_state_txt.SetLabel(('GAME OVER', '!!! YOU WIN !!!')[win])

        if not win:
            for i in range(1, len(self.word) - 1):
                self.indexes.add(i)
            self.UpdateWordText()

    def OnCharPress(self, e):
        btn = e.GetEventObject()
        btn_char = btn.GetLabel()
        guessed = False

        for index in (match.start() for match in finditer(btn_char, self.word)):
            if index not in self.indexes:
                self.indexes.add(index)
                guessed = True

        if guessed:
            self.UpdateWordText()

            if len(self.word) == len(self.indexes):
                self.EndGame(win=True)
        else:
            self.lives -= 1
            self.UpdateImage(6 - self.lives)

            if self.lives == 0:
                self.EndGame(win=False)

        btn.Hide()

    def OnPlayAgain(self, e):
        self.Reset()

    def OnQuit(self, e):
        self.Close()


if __name__ == '__main__':
    app = wx.App()
    Hangman()
    app.MainLoop()
