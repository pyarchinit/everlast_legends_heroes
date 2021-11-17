#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
/***************************************************************************
    Heroquest Legends Solo by Mandor the Druid
                             -------------------
    begin                : 2021-01-02
    copyright            : (C) 2021 by Luca Mandolesi
    email                : mandoluca at gmail.com
    version              : 0.91 ALPHA
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import locale
import sys, os
import random
import json
from datetime import datetime
from PyQt5 import QtWidgets, uic, QtCore

#codeadded
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QLabel

#codeadde d/
from heroquest_solo_function import Heroquest_solo


from adventure_panel_settings_main import AdventurePanelSettings
from hql_map_viewer import HQL_MAP


from pygame import mixer  # Load the popular external library


class Ui(QtWidgets.QMainWindow):
    #TODO aggiungere come posizione il mostro davanti alla porta fuori o dentro la stanza
    #TODO aggiungere oltre che davanti, davanti ed adiacente a te.
    #TODO aggiungere opzione per circondare l'eroe
    #TODO messaggio con punto di partenza
    #TODO aggiungere segnalatore di fine avventura scale trovate
    #TODO se il mostro prima attacca poi si sposta per lasciare spazio ad un altro mostro se è nella stanza

    CONFIG = ""
    local_language = locale.getdefaultlocale()
    #file_name = 'en_EN.txt'
    if local_language[0] == 'it_IT':
        CONFIG = open('./languages/IT_it.txt', "rb+")
    else:
        CONFIG = open('./languages/EN_en.txt', "rb+")
    data_config = CONFIG.read()
    CONFIG_DICT = eval(data_config)
    CONFIG.close()
    HQ_SOLO = ""

    CURRENT_ROUND = 1

    MONSTER_LIST = ''

    TREASURES_FINDS = 0

    CHRONICLE = ""

    def __init__(self):
        super(Ui, self).__init__()

        self.acceptDrops()
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

        uic.loadUi(os.path.join(os.path.dirname(__file__),'heroquest_legends.ui'), self)

        self.HQ_SOLO = Heroquest_solo(self.CONFIG_DICT)
        self.pushButton_close.clicked.connect(self.close)

        bg_img_path = './background.png'
        oImage = QImage(bg_img_path)
        sImage = oImage.scaled(QSize(800, 768))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))

        self.setPalette(palette )
        self.charge_list()
        the_missions_dict = self.CONFIG_DICT['missions_dict']
        key_list = []
        for k in the_missions_dict.keys():
            key_list.append(str(k))

        self.comboBox_choose_adventure.addItems(key_list)

        self.show()

    def on_pushButton_map_pressed(self):
        map = HQL_MAP(self)
        map.exec_()
        #map.show()

    def on_pushButton_settings_pressed(self):
        dlg = AdventurePanelSettings(self)
        dlg.DICT = self.CONFIG_DICT
        dlg.insertItems()

        dlg.exec_()
        the_missions_dict = self.CONFIG_DICT['missions_dict']
        key_list = []
        for k in the_missions_dict.keys():
            key_list.append(str(k))

        self.comboBox_choose_adventure.clear()
        self.comboBox_choose_adventure.addItems(key_list)

        local_language = locale.getdefaultlocale()
        # file_name = 'en_EN.txt'
        if local_language[0] == 'it_IT':
            convert_file = open('./languages/IT_it.txt', 'w')
            convert_file.write(str(self.CONFIG_DICT))
            convert_file.close()
            self.pushButton_the_mission.setEnabled(True)
        else:
            self.CONFIG = open('./languages/EN_en.txt', 'w')
            convert_file.write(str(self.CONFIG_DICT))
            convert_file.close()
            self.pushButton_the_mission.setEnabled(True)

    def charge_list(self):
        #CHARGE DB MONSTERS CATEGORY
        db_monsters_charged = self.HQ_SOLO.MONSTERS_CATEGORY

        self.MONSTER_LIST = []

        for value in db_monsters_charged.values():

            self.MONSTER_LIST.append(self.CONFIG_DICT['monster_name_conversion_dict'][value])

        self.comboBox_monster_attack.clear()

        self.comboBox_monster_attack.addItems(self.MONSTER_LIST)

        ############# CHARGE FORNITURES LIST ##############
        fornitures_list = self.CONFIG_DICT['forniture_name_reconversion_dict']
        self.comboBox_fornitures.addItems([*fornitures_list])

        ###########CHARGE DUNGEON POV ############

        self.POV_LIST =self.HQ_SOLO.charge_point_of_views()

        self.comboBox_pov.clear()
        self.comboBox_pov.addItems(self.POV_LIST)

        ###########CHARGE ROOM NUMBERS ############

        self.ROOMS_NUMBERS_LIST =self.HQ_SOLO.charge_rooms_numbers()

        self.comboBox_room_n.clear()
        self.comboBox_room_n.addItems(self.ROOMS_NUMBERS_LIST)


    def on_pushButton_the_mission_pressed(self):
        mission_choosed = self.comboBox_choose_adventure.currentText()

        if mission_choosed =="":
            rng_base = random.SystemRandom()
            mission_number_rand = rng_base.randint(1,4)
        else:
            mission_number_rand = int(mission_choosed)

        self.HQ_SOLO.special_data_mission_charged(mission_number_rand)

        the_mission_dict = self.CONFIG_DICT['missions_dict']

        rng_base = random.SystemRandom()

        wanderer_monster_number_rand = rng_base.randint(1, 7)
        wanderer_monster = self.CONFIG_DICT['monsters_dict'][wanderer_monster_number_rand]
        wanderer_monster_text = self.CONFIG_DICT['monsters_msg_3']

        the_mission_text = '{}\n{}{}'.format(the_mission_dict[mission_number_rand][1],wanderer_monster_text,wanderer_monster)
        self.textEdit_the_mission.setText(the_mission_text)
        self.QLabel_the_title.setText(the_mission_dict[mission_number_rand][0])



        self.pushButton_aisles.setEnabled(True)
        self.pushButton_rooms.setEnabled(True)
        self.pushButton_treasures_finds.setEnabled(True)
        self.pushButton_treasures_random.setEnabled(False)
        self.pushButton_treasure_card.setEnabled(False)
        self.pushButton_traps_and_secret_doors_finder.setEnabled(True)
        self.pushButton_hero_attack.setEnabled(True)
        self.pushButton_monster_attack.setEnabled(True)
        self.pushButton_round.setEnabled(True)


        self.pushButton_the_mission.setEnabled(False)

        #################CREATE THE DUNGEON####################
        #self.create_the_dungeon(self.START_FROM, self.ARRIVE_TO,self.MIN_PATH)
        self.HQ_SOLO.create_the_dungeon('1', 'C', 5) #add random choice

        self.set_chronicle(the_mission_text)
        the_primary_path_txt = 'The primary path is:\n{}'.format(self.HQ_SOLO.PRIMARY_PATH)
        self.set_chronicle(the_primary_path_txt)
        the_secondary_path_txt = 'The secondary path is:\n{}'.format(self.HQ_SOLO.SECONDARY_PATH)
        self.set_chronicle(the_secondary_path_txt)



    def set_chronicle(self, nt):
        self.new_text = nt
        now = datetime.now()
        self.CHRONICLE = '--- {} ---- \n\n {} \n\n --- \n\n {}'.format(now,self.new_text, self.CHRONICLE)
        self.textEdit_chronicle.setText(self.CHRONICLE)


    def on_pushButton_round_pressed(self):
        self.textEdit_messages.setText("")

        #self.textEdit_aisles.setText("")
        #self.textEdit_monsters.setText("")
        #self.textEdit_room_description.setText("")
        #self.textEdit_treasures_finder.setText("")
        #self.textEdit_treasures_description.setText("")
        #self.textEdit_treasure_cards_description.setText("")
        #self.textEdit_traps.setText("")
        #self.textEdit_secret_doors.setText("")
        self.textEdit_combat_text.setText("")
        self.CURRENT_ROUND = int(self.lineEdit_round.text())
        next_turn = self.CURRENT_ROUND+1
        self.lineEdit_round.setText(str(next_turn))
        self.CURRENT_ROUND = next_turn
        self.pushButton_treasures_finds.setEnabled(True)
        self.pushButton_treasures_random.setEnabled(False)
        self.pushButton_treasure_card.setEnabled(False)


    def on_pushButton_aisles_pressed(self):
        msg = ""
        self.textEdit_messages.setText("")
        #self.textEdit_traps.setText("")
        #self.textEdit_aisles.setText("")
        print("Error 1")
        current_POV = self.comboBox_pov.currentText() ##TODO  AGGIUNGERE IL DUNGEOM SECONDARIO
        if current_POV not in self.HQ_SOLO.POINT_OF_VIEW_EXPLORED:
            print("Error 2")
            ###TODO Spostare
            self.HQ_SOLO.POINT_OF_VIEW_EXPLORED.append(current_POV)
            msg += self.HQ_SOLO.how_is_the_dungeon(current_POV, self.CURRENT_ROUND)
            ###TODO SPOSTARE
            msg += '\n'+self.HQ_SOLO.random_monsters_on_aisles(self.CURRENT_ROUND)
        else:
            print("Error 3")
            msg += self.HQ_SOLO.random_monsters_on_aisles(self.CURRENT_ROUND)

        print("Error 4")
        random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
        print("Error 5")
        message = "{}\n{}".format(random_trap, msg)
        self.textEdit_messages.setText(message)

        #self.textEdit_traps.setText(random_trap)
        #self.textEdit_aisles.setText(msg)

        #chronicle
        self.set_chronicle(msg)
        self.set_chronicle(random_trap)

    def on_pushButton_treasures_finds_pressed(self):
        #self.textEdit_traps.setText("")
        #self.textEdit_treasures_finder.setText("")
        #self.textEdit_treasures_description.setText("")
        #self.textEdit_treasure_cards_description.setText("")

        res = self.HQ_SOLO.treasures(self.HQ_SOLO.random_numbers())
        msg = res[0]
        self.TREASURES_FINDS = res[1]
        if self.TREASURES_FINDS == 1:
            self.pushButton_treasures_random.setEnabled(True)
            self.pushButton_treasure_card.setEnabled(False)
        else:
            self.pushButton_treasures_random.setEnabled(False)
            self.pushButton_treasure_card.setEnabled(True)
        #self.textEdit_treasures_finder.setText("")
        #self.textEdit_treasures_finder.setText(str(msg))

        message = str(msg)
        self.textEdit_messages.setText("")
        self.textEdit_messages.setText(message)



    def on_pushButton_treasure_card_pressed(self):
        #self.textEdit_traps.setText("")
        #self.textEdit_treasures_finder.setText("")
        #self.textEdit_treasures_description.setText("")
        #self.textEdit_treasure_cards_description.setText("")

        msg = self.HQ_SOLO.treasure_card(self.HQ_SOLO.random_numbers())
        #self.textEdit_treasure_cards_description.setText("")
        #self.textEdit_treasure_cards_description.setText(str(msg))

        message = str(msg)
        self.textEdit_messages.setText(message)


        self.pushButton_treasure_card.setEnabled(False)


    def on_pushButton_treasures_random_pressed(self):
        #self.textEdit_traps.setText("")
        #self.textEdit_treasures_finder.setText("")
        #self.textEdit_treasures_description.setText("")
        #self.textEdit_treasure_cards_description.setText("")


        forniture = self.comboBox_fornitures.currentText()
        print("here 1")

        msg = self.HQ_SOLO.treasure_random(self.HQ_SOLO.random_numbers(), forniture)
        print("here2 ")

        self.pushButton_treasures_random.setEnabled(False)
        self.TREASURES_FINDS = 0

        #self.textEdit_treasures_description.setText(str(msg))
        #self.textEdit_traps.setText(random_trap)

        random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
        print("here")
        message = "{}\n{}".format(str(msg), random_trap)
        self.textEdit_messages.setText(message)

        self.set_chronicle(message)


    def on_pushButton_traps_and_secret_doors_finder_pressed(self):
        #self.textEdit_traps.setText("")
        msg_traps = self.HQ_SOLO.traps(self.HQ_SOLO.random_numbers())
        msg_secret_door = self.HQ_SOLO.secret_doors(self.HQ_SOLO.random_numbers())
        message = self.CONFIG_DICT['traps_and_secret_doors_msg_1'].format(msg_traps, msg_secret_door[0], msg_secret_door[1])
        self.textEdit_messages.setText(message)
        self.set_chronicle(message)
        self.textEdit_chronicle.setText(self.CHRONICLE)


    def on_pushButton_rooms_pressed(self):
        ####NEW CODE############
        msg_room = ''
        random_trap = ''
        #self.textEdit_traps.setText("")
        #self.textEdit_room_description.setText('')
        #self.textEdit_monsters.setText('')

        self.textEdit_messages.setText("")

        room_to_explore = self.comboBox_room_n.currentText()
        if room_to_explore in self.HQ_SOLO.ROOMS_EXPLORED:
            room_explored = 1
            random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
            #self.textEdit_traps.setText(random_trap)
            msg_trap = random_trap
            self.set_chronicle(random_trap)
        else:
            room_explored = 0
            self.HQ_SOLO.ROOMS_EXPLORED.append(room_to_explore)
        current_turn = int(self.lineEdit_round.text())
        room_dimension = str(self.HQ_SOLO.ROOMS_NUM_TILES[str(room_to_explore)])
        msg_temp = self.HQ_SOLO.room_generator(room_dimension, current_turn,room_explored)
        if current_turn == 1 or current_turn == 2:
            msg_room = self.HQ_SOLO.CONFIG_DICT['aux_msg_1'].format(msg_temp[0])
            random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
            #self.textEdit_traps.setText(random_trap)
            msg_trap = random_trap
            self.set_chronicle(random_trap)
        else:
            if msg_temp[2] != '':
                self.CHRONICLE = '{} \n\n --- \n\n {}'.format(self.CHRONICLE, msg_temp[2])
                self.textEdit_chronicle.setText(self.CHRONICLE)
                msg_room = msg_temp[2]
                random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
                msg_trap = random_trap
                #self.textEdit_traps.setText(random_trap)
                #self.set_chronicle(random_trap)
                #self.set_chronicle(msg_room)
            elif msg_temp[0] == '' and msg_temp[2] == '' and room_explored == 1:
                msg_room = self.HQ_SOLO.CONFIG_DICT['aux_msg_7']
                random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
                msg_trap = random_trap
                #self.textEdit_traps.setText(random_trap)
                #self.set_chronicle(random_trap)
                #self.set_chronicle(msg_room)
            elif msg_temp[0] == '' and msg_temp[2] == '' and room_explored == 0:
                msg_room = self.HQ_SOLO.CONFIG_DICT['aux_msg_6']
                random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
                msg_trap = random_trap
                #self.textEdit_traps.setText(random_trap)
                #self.set_chronicle(random_trap)
                #self.set_chronicle(msg_room)
            else:
                msg_room = msg_temp[0]
                random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
                msg_trap = random_trap
                #self.textEdit_traps.setText(random_trap)
                #self.set_chronicle(random_trap)
                #self.set_chronicle(msg_room)

        msg_room = msg_room.replace(';.', '.')


        #self.textEdit_room_description.setText(str(msg_room))
        msg = msg_trap + "\n"+ msg_room

        #self.textEdit_monsters.setText(str(msg_temp[1]))
        msg += str(msg_temp[1])

        self.textEdit_messages.setText(msg)
        self.set_chronicle(msg)
        #self.set_chronicle(msg_room)
        #self.set_chronicle(str(msg_temp[1]))

    def on_pushButton_monster_attack_pressed(self):
        self.textEdit_combat_text.setText("")
        self.textEdit_messages.setText("")
        print("here 20")
        monster_category = self.comboBox_monster_attack.currentText()
        monster_group = 0
        monster_sight = 0
        if self.checkBox_group.isChecked() == True:
            monster_group = 1

        if self.checkBox_sight.isChecked() == True:
            monster_sight = 1

        mode_result = self.HQ_SOLO.fighting_system(monster_category, monster_group, monster_sight) #1 attack - 0 escape
        print("here 21")

        if mode_result == 1:
            msg_attack_list = self.CONFIG_DICT['attack_messages'][1]

            rng_base = random.SystemRandom()
            msg_attack = msg_attack_list[rng_base.randint(0, len(msg_attack_list)-1)]

            rng_base = random.SystemRandom()
            msg_attack_choice = msg_attack.format(self.CONFIG_DICT['choice_dict'][rng_base.randint(1, 5)])

            rng_base = random.SystemRandom()
            msg_attack_choice_direction = msg_attack_choice.format(self.CONFIG_DICT['monster_direction_dict'][rng_base.randint(1, 4)])

            self.textEdit_combat_text.setText(str(msg_attack_choice_direction))
            monster_attack_msg = 'Attacco del mostro:\n{}'.format(msg_attack_choice_direction)
            self.set_chronicle(monster_attack_msg)
        else:
            msg_escape_list = self.CONFIG_DICT['attack_messages'][2]
            rng_base = random.SystemRandom()
            msg_escape = msg_escape_list[rng_base.randint(0, len(msg_escape_list)-1)]
            self.textEdit_combat_text.setText(msg_escape)
            escape_message_msg = 'Attacco del mostro:\n{}'.format(msg_escape)
            self.set_chronicle(escape_message_msg)

    def on_pushButton_hero_attack_pressed(self):
        #self.textEdit_traps.setText("")
        self.textEdit_messages.setText("")
        print("here 10")

        random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
        self.textEdit_messages.setText(random_trap)

        print("here 11")

        #self.textEdit_traps.setText(random_trap)
        #

        self.set_chronicle(random_trap)
        rand_value = self.HQ_SOLO.random_numbers()
        self.textEdit_combat_text.setText(self.HQ_SOLO.hero_attack(rand_value))



    ############################ TODO spostare in functions ####################



app = QtWidgets.QApplication(sys.argv)

#load language
translator = QtCore.QTranslator()
local_language = locale.getdefaultlocale()
if local_language[0] == 'it_IT':
    translator.load("./languages/IT_it.qm")
elif local_language[0] == 'en_EN':
    translator.load("./languages/EN_en.qm")
elif local_language[0] == 'es_ES':
    translator.load("./languages/ES_es.qm")
else:
    translator.load("./languages/EN_en.qm")

app.installTranslator(translator)
window = Ui()
#window.showFullScreen()
window.adjustSize()



app.exec_()