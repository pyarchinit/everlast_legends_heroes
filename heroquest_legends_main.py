#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
/***************************************************************************
        Heroquest's Legends Solo by Mandor the Druid
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
        CONFIG = open('./languages/IT_it.txt', "r")
    else :
        CONFIG = open('./languages/EN_en.txt', "r")
    data_config = CONFIG.read()
    CONFIG_DICT = eval(data_config)
    CONFIG.close()
    HQ_SOLO = ""

    CURRENT_ROUND = 1

    MONSTER_LIST = ''

    TREASURES_FINDS = 0

    CHRONICLE = ""

    POV_LIST = []

    PRIMARY_PATH = []
    START_FROM = 'D'
    ARRIVE_TO = 'F'  # randomly selected by the app from point of views kesy
    MIN_PATH = 4  # randomly selected by the app between 3 and 6

    SECONDARY_PATH = []
    THE_SECONDARY_START = ''
    THE_SECONDARY_ARRIVE = ''
    THE_SECONDARY_MIN_PATH = ''

    POINT_OF_VIEW_EXPLORED = []

    POINT_OF_VIEW = {
        'A': ('1', '4'),
        'B': ('1', '2'),
        'C': ('2', '3'),
        'D': ('3', '4'),
        'E': ('1', '5', '6'),
        'F': ('2', '6', '7'),
        'G': ('3', '7', '8'),
        'H': ('4', '5', '8'),
        '1': ('A', 'B', 'E'),
        '2': ('B', 'C', 'F'),
        '3': ('C', 'D', 'G'),
        '4': ('A', 'D', 'H'),
        '5': ('E', 'H'),
        '6': ('E', 'F'),
        '7': ('F', 'G'),
        '8': ('G', 'H')}

    DUNGEON_TO_ROOM = {
        'A1': ('401', '402', '403'),
        'B1': ('301', '302', '303'),
        'B2': ('301', '304'),
        'C2': ('201', '204'),
        'C3': ('201', '202', '203'),
        'D3': ('101', '102', '103'),
        'D4': ('101', '104'),
        'A4': ('401', '404'),
        'E1': ('303', '403', '501'),
        'E5': ('403', '406', '501'),
        'E6': ('303', '305', '501'),
        'F2': ('204', '205', '304', '305', '501'),
        'F6': ('303', '305', '501'),
        'F7': ('203', '205', '501'),
        'G3': ('103', '203', '501'),
        'G7': ('203', '205', '501'),
        'G8': ('103', '105', '501'),
        'H4': ('104', '105', '404', '405', '406', '501'),
        'H5': ('403', '406', '501'),
        'H8': ('103', '105', '501')}

    ROOM_TO_ROOM = {
        '101': ('102', '104'),
        '102': ('101', '103', '105'),
        '103': ('102', '105'),
        '104': ('101', '105'),
        '105': ('102', '103', '104'),

        '201': ('202', '204'),
        '202': ('201', '203', '205'),
        '203': ('202', '205'),
        '204': ('201', '205'),
        '205': ('202', '203', '204'),

        '301': ('302', '304'),
        '302': ('301', '303', '305'),
        '303': ('302', '305'),
        '304': ('301', '305'),
        '305': ('302', '303', '304'),

        '401': ('402', '404'),
        '402': ('401', '403', '404', '405', '406'),
        '403': ('402'),
        '404': ('401', '404', '405', '406'),
        '405': ('402', '404', '406'),
        '406': ('402', '405')}

    ROOM_TO_DUNGEON = {
        '101': ('D3', 'D4'),
        '102': ('D3'),
        '103': ('D3', 'G3', 'G8'),
        '104': ('D4', 'H4'),
        '105': ('H4', 'H8'),

        '201': ('C2', 'C3'),
        '202': ('C3'),
        '203': ('C3', 'G3', 'G7'),
        '204': ('C2', 'F2'),
        '205': ('F2', 'F7'),

        '301': ('B1', 'B2'),
        '302': ('B1'),
        '303': ('B1', 'E1', 'E6'),
        '304': ('B2', 'F2'),
        '305': ('F2', 'F6'),

        '401': ('A1', 'A4'),
        '402': ('A1'),
        '403': ('A1', 'E1'),
        '404': ('A4', 'H4'),
        '405': ('H4'),
        '406': ('H4', 'H5'),

        '501': (
        'E1', 'E5', 'E6', 'F2', 'F6', 'F7', 'G3', 'G7', 'G8',
        'H4', 'H5', 'H8')}


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
        map.show()

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
        for keys in self.POINT_OF_VIEW.keys():
            self.POV_LIST.append(keys)

        self.comboBox_pov.clear()
        self.comboBox_pov.addItems(self.POV_LIST)


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
        self.create_the_dungeon(self.START_FROM, self.ARRIVE_TO,self.MIN_PATH)

        self.set_chronicle(the_mission_text)
        the_primary_path_txt = 'The primary path is:\n{}'.format(self.PRIMARY_PATH)
        self.set_chronicle(the_primary_path_txt)
        the_secondary_path_txt = 'The secondary path is:\n{}'.format(self.SECONDARY_PATH)
        self.set_chronicle(the_secondary_path_txt)

    def create_the_dungeon(self, s, a, m):
        #INSERT VALUES
        start = s #CHOOSED RANDOMLY BY THE GAME
        arrive = a #CHOOSED RANDOMLY BY THE GAME
        min_path = m #CHOOSED RANDOMLY BY THE GAME


        #the_primary_path = ''
        #THEN PUSH THE BUTTON
        #self.PRIMARY_PATH = ''
        #self.SECONDARY_PATH = ''


        self.PRIMARY_PATH = self.find_route(start,arrive)
        while len(self.PRIMARY_PATH) < min_path or arrive != self.PRIMARY_PATH[-1]:
            self.PRIMARY_PATH = self.find_route(start, arrive)

        #THE GAME CHOOSE A SECONDARY PATH
        half = len(self.PRIMARY_PATH) // 2
        the_secondary_path_temp = self.PRIMARY_PATH[0:half]

        for i in self.POINT_OF_VIEW.keys():
            if i not in self.PRIMARY_PATH:
                self.THE_SECONDARY_ARRIVE = i
                break

        self.THE_SECONDARY_START = the_secondary_path_temp[-1]
        #CHOOSED RANDOMLY BY THE GAME

        self.THE_SECONDARY_MIN_PATH = 3 #len(self.PRIMARY_PATH) #the current path lenght of primary_path
        #the_path = ''

        #THEN PUSH THE BUTTON

        #INSERT VALUES

        #THEN PUSH THE BUTTON

        self.SECONDARY_PATH = self.find_route(self.THE_SECONDARY_START,self.THE_SECONDARY_ARRIVE)
        while len(self.SECONDARY_PATH) >= len(self.PRIMARY_PATH) or self.THE_SECONDARY_ARRIVE != self.SECONDARY_PATH[-1]:
            self.SECONDARY_PATH = self.find_route(self.THE_SECONDARY_START, self.THE_SECONDARY_ARRIVE)
        #return self.PRIMARY_PATH

    def find_route(self, b, a):
        start = b
        arrive = a
        current = start
        path_temp = [start]
        cont = 0
        while current != arrive and cont <= 25:
            local_paths = self.POINT_OF_VIEW[current] #POINT_OF_VIEW
            length_list = len(local_paths)
            rng = random.SystemRandom()
            slice_number = rng.randint(0, int(length_list)-1)
            current_temp_pov = local_paths[slice_number]
            if current_temp_pov in path_temp:
                pass
            else:
                path_temp.append(current_temp_pov)
                current = current_temp_pov
                cont = 0
            cont += 1
        return path_temp


    def set_chronicle(self, nt):
        self.new_text = nt
        now = datetime.now()
        self.CHRONICLE = '--- {} ---- \n\n {} \n\n --- \n\n {}'.format(now,self.new_text, self.CHRONICLE)
        self.textEdit_chronicle.setText(self.CHRONICLE)


    def on_pushButton_round_pressed(self):
        self.textEdit_aisles.setText("")
        self.textEdit_monsters.setText("")
        self.textEdit_room_description.setText("")
        self.textEdit_treasures_finder.setText("")
        self.textEdit_treasures_description.setText("")
        self.textEdit_treasure_cards_description.setText("")
        self.textEdit_traps.setText("")
        self.textEdit_secret_doors.setText("")
        self.textEdit_combat_text.setText("")
        self.CURRENT_ROUND = int(self.lineEdit_round.text())
        next_turn = self.CURRENT_ROUND+1
        self.lineEdit_round.setText(str(next_turn))
        self.CURRENT_ROUND = next_turn
        self.pushButton_treasures_finds.setEnabled(True)
        self.pushButton_treasures_random.setEnabled(False)
        self.pushButton_treasure_card.setEnabled(False)


    def on_pushButton_aisles_pressed(self):
        self.textEdit_traps.setText("")
        current_turn = int(self.lineEdit_round.text())
        self.textEdit_aisles.setText("")
        if self.radioButton_aisles_not_explored.isChecked() == True:
            if current_turn == 1 or current_turn == 2:
                msg_num = self.HQ_SOLO.random_numbers()
                while (msg_num) >= 21:
                    msg_num = self.HQ_SOLO.random_numbers()  # return always door at first and second turn
                msg = self.HQ_SOLO.aisles(msg_num)
            else:
                msg = self.HQ_SOLO.aisles(self.HQ_SOLO.random_numbers())
        else:
            msg = self.HQ_SOLO.random_monsters_on_aisles(self.CURRENT_ROUND)


        self.textEdit_aisles.setText("")

        ###TODO Spostare
        current_POV = self.comboBox_pov.currentText()
        self.POINT_OF_VIEW_EXPLORED.append(current_POV)
        the_dungeon = self.how_is_the_dungeon(current_POV)
        ###TODO SPOSTARE

        #self.textEdit_aisles.setText(str(msg)+the_dungeon) OLD AISLES MESSAGES
        self.textEdit_aisles.setText(the_dungeon)

        random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
        self.textEdit_traps.setText(random_trap)
        self.set_chronicle(random_trap)

    def on_pushButton_treasures_finds_pressed(self):
        self.textEdit_traps.setText("")
        self.textEdit_treasures_finder.setText("")
        self.textEdit_treasures_description.setText("")
        self.textEdit_treasure_cards_description.setText("")
        res = self.HQ_SOLO.treasures(self.HQ_SOLO.random_numbers())
        msg = res[0]
        self.TREASURES_FINDS = res[1]
        if self.TREASURES_FINDS == 1:
            self.pushButton_treasures_random.setEnabled(True)
            self.pushButton_treasure_card.setEnabled(False)
        else:
            self.pushButton_treasures_random.setEnabled(False)
            self.pushButton_treasure_card.setEnabled(True)
        self.textEdit_treasures_finder.setText("")
        self.textEdit_treasures_finder.setText(str(msg))


    def on_pushButton_treasure_card_pressed(self):
        self.textEdit_traps.setText("")
        self.textEdit_treasures_finder.setText("")
        self.textEdit_treasures_description.setText("")
        self.textEdit_treasure_cards_description.setText("")
        msg = self.HQ_SOLO.treasure_card(self.HQ_SOLO.random_numbers())
        self.textEdit_treasure_cards_description.setText("")
        self.textEdit_treasure_cards_description.setText(str(msg))
        self.pushButton_treasure_card.setEnabled(False)


    def on_pushButton_treasures_random_pressed(self):
        self.textEdit_traps.setText("")
        self.textEdit_treasures_finder.setText("")
        self.textEdit_treasures_description.setText("")
        self.textEdit_treasure_cards_description.setText("")
        forniture = self.comboBox_fornitures.currentText()
        msg = self.HQ_SOLO.treasure_random(self.HQ_SOLO.random_numbers(), forniture)
        self.pushButton_treasures_random.setEnabled(False)
        self.TREASURES_FINDS = 0
        self.textEdit_treasures_description.setText(str(msg))
        random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
        self.textEdit_traps.setText(random_trap)
        self.set_chronicle(random_trap)


    def on_pushButton_traps_and_secret_doors_finder_pressed(self):
        self.textEdit_traps.setText("")
        msg_traps = self.HQ_SOLO.traps(self.HQ_SOLO.random_numbers())
        msg_secret_door = self.HQ_SOLO.secret_doors(self.HQ_SOLO.random_numbers())
        if str(type(msg_secret_door)) == "<class 'list'>":
            self.textEdit_secret_doors.setText(msg_secret_door[0])
            self.textEdit_room_description.setText('')
            self.textEdit_room_description.setText(msg_secret_door[1])

            self.set_chronicle(msg_secret_door[0]+msg_secret_door[1])


            self.textEdit_chronicle.setText(self.CHRONICLE)
        else:
            self.textEdit_secret_doors.setText(msg_secret_door)
        self.textEdit_traps.setText(str(msg_traps))


    def on_pushButton_rooms_pressed(self):
        self.textEdit_traps.setText("")
        self.textEdit_room_description.setText('')
        self.textEdit_monsters.setText('')
        if self.radioButton_explored.isChecked() == True:
            room_explored = 1
            random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
            self.textEdit_traps.setText(random_trap)
            self.set_chronicle(random_trap)
        else:
            room_explored = 0
        current_turn = int(self.lineEdit_round.text())
        msg_temp = self.HQ_SOLO.room_generator(self.lineEdit_room_dimension.text(), current_turn,room_explored)
        if current_turn == 1 or current_turn == 2:
            msg_room = self.HQ_SOLO.CONFIG_DICT['aux_msg_1'].format(msg_temp[0])
            random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
            self.textEdit_traps.setText(random_trap)
            self.set_chronicle(random_trap)
        else:
            if msg_temp[2] != '':
                self.CHRONICLE = '{} \n\n --- \n\n {}'.format(self.CHRONICLE, msg_temp[2])
                self.textEdit_chronicle.setText(self.CHRONICLE)
                msg_room = msg_temp[2]
                random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
                self.textEdit_traps.setText(random_trap)
                self.set_chronicle(random_trap)
                self.set_chronicle(msg_room)
            elif msg_temp[0] == '' and msg_temp[2] == '' and room_explored == 1:
                msg_room = self.HQ_SOLO.CONFIG_DICT['aux_msg_7']
                random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
                self.textEdit_traps.setText(random_trap)
                self.set_chronicle(random_trap)
                self.set_chronicle(msg_room)
            elif msg_temp[0] == '' and msg_temp[2] == '' and room_explored == 0:
                msg_room = self.HQ_SOLO.CONFIG_DICT['aux_msg_6']
                random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
                self.textEdit_traps.setText(random_trap)
                self.set_chronicle(random_trap)
                self.set_chronicle(msg_room)
            else:
                msg_room = msg_temp[0]
                random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
                self.textEdit_traps.setText(random_trap)
                self.set_chronicle(random_trap)
                self.set_chronicle(msg_room)

        msg_room = msg_room.replace(';.', '.')

        self.textEdit_room_description.setText(str(msg_room))

        self.textEdit_monsters.setText(str(msg_temp[1]))

        self.set_chronicle(random_trap)
        self.set_chronicle(msg_room)
        self.set_chronicle(str(msg_temp[1]))




    def on_pushButton_monster_attack_pressed(self):
        self.textEdit_combat_text.setText("")
        self.textEdit_traps.setText("")
        monster_category = self.comboBox_monster_attack.currentText()
        monster_group = 0
        monster_sight = 0
        if self.checkBox_group.isChecked() == True:
            monster_group = 1

        if self.checkBox_sight.isChecked() == True:
            monster_sight = 1

        mode_result = self.HQ_SOLO.fighting_system(monster_category, monster_group, monster_sight) #1 attack - 0 escape

        if mode_result == 1:
            msg_attack_list = self.CONFIG_DICT['attack_messages'][1]

            rng_base = random.SystemRandom()
            msg_attack = msg_attack_list[rng_base.randint(0, len(msg_attack_list)-1)]

            rng_base = random.SystemRandom()
            msg_attack_choice = msg_attack.format(self.CONFIG_DICT['choice_dict'][rng_base.randint(1, 5)])

            rng_base = random.SystemRandom()
            msg_attack_choice_direction = msg_attack_choice.format(self.CONFIG_DICT['monster_direction_dict'][rng_base.randint(1, 4)])

            self.textEdit_combat_text.setText(str(msg_attack_choice_direction))
        else:
            msg_escape_list = self.CONFIG_DICT['attack_messages'][2]
            rng_base = random.SystemRandom()
            msg_escape = msg_escape_list[rng_base.randint(0, len(msg_escape_list)-1)]
            self.textEdit_combat_text.setText(msg_escape)

    def on_pushButton_hero_attack_pressed(self):
        self.textEdit_traps.setText("")

        random_trap = self.HQ_SOLO.random_trap(self.CURRENT_ROUND)
        self.textEdit_traps.setText(random_trap)
        self.set_chronicle(random_trap)
        rand_value = self.HQ_SOLO.random_numbers()
        self.textEdit_combat_text.setText(self.HQ_SOLO.hero_attack(rand_value))



    ############################ TODO spostare in functions ####################

    def put_the_doors(self, d):
        dungeon_id = d
        rooms_list = self.DUNGEON_TO_ROOM[dungeon_id]
        door_msg = ''
        for i in rooms_list:
            rng = random.SystemRandom()
            num = rng.randint(0, 99)
            if (num % 2) == 0:
                door_msg += "Room {0} has a door. \n".format(str(i))
            else:
                door_msg += "No doors for room {}. \n".format(str(i))

        return door_msg


    def how_is_the_dungeon(self, pv):
        pointofview = pv
        path = self.PRIMARY_PATH

        single_points = self.POINT_OF_VIEW[pointofview]

        msg = '\nMessaggi dungeon e pov\n'

        if pointofview == path[-1]:
            msg += "This is a Dead-end road...you can only con back. Put Rocks to any other point of view"
        else:
            for i in single_points:
                if i not in path:
                    msg += "A collapse blocks access to this part of the dungeon (Put a collapse blocks to POV {})\n".format(str(i))
                else:
                    if i == path[-1]:
                        msg += "The dungeon continues through the darkness, (you can walk to POV {})\n".format(str(i))
                        if i.isdigit() == True:
                            dungeon_id = '{}{}'.format(str(pointofview), str(i))
                            msg_doors = self.put_the_doors(dungeon_id)
                            msg += msg_doors
                        else:
                            dungeon_id = '{}{}'.format(str(i), str(pointofview))
                            msg_doors = self.put_the_doors(dungeon_id)
                            msg += msg_doors

                    else:
                        index_number = path.index(pointofview)+1
                        if i == path[index_number] and i not in self.POINT_OF_VIEW_EXPLORED :  #IF i the next pov
                            msg += "The dungeon continues through the darkness. (you can walk to POV {})\n".format(str(i))
                            if i.isdigit() == True:
                                dungeon_id = '{}{}'.format(str(pointofview), str(i))
                                msg_doors = self.put_the_doors(dungeon_id)
                                msg += msg_doors
                            else:
                                dungeon_id = '{}{}'.format(str(i), str(pointofview))
                                msg_doors = self.put_the_doors(dungeon_id)
                                msg += msg_doors

                        elif i != path[index_number] and i in self.POINT_OF_VIEW_EXPLORED:
                                msg += "You can come back on your owm passes (you can walk to POV {})\n".format(str(i))

                        elif i == path[index_number] and i in self.POINT_OF_VIEW_EXPLORED:
                                msg += "No way to go on....the pass is blocked (The dungeon is collapse to POV {}".format(str(i))

                        elif i != path[index_number] and i not in self.POINT_OF_VIEW_EXPLORED:
                                msg += "A collapse blocks access to this part of the dungeon (Put a collapse blocks to POV {})\n".format(str(i))
                                    #"The dungeon continues through the darkness but the roof doesn't appear solid,you can walk to POV {} if you obtain a shield after launching a combat dice".format(str(i))


        return msg


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