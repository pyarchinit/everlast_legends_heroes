#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
/***************************************************************************
    Heroquest Legends Solo by Mandor the Druid
                              -------------------
    begin                : 2021-01-02
    copyright            : (C) 2021 by Luca Mandolesi
    email                : mandoluca at gmail.com
    version              : 0.95 ALPHA
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
import random
import sqlite3

from permutations_iter import Permutation_class

#TODO se il mostro può attaccare subito perchè vicino all'eroe, segnalare se poi si allontana o resta lì
#TODO E' nella linea di vista del mostro l'eroe?
#TODO I MOSTRI SONO IN GRUPPO SE SI VEDONO RECIPROCAMENTE
#TODO inserire sequenza di movimento mostri se quello con più punti attacco, quello che si muove di più
#TODO quando si trova la stanza finale cambiare il testo dei mostri: vengono caricati dei mostri con la descrizione finale ma il testo può dire: nessun mostro in vista.
#TODO quandi ci si trova a metà di un nuovo corridoio decidere come fare ad esplorarlo.
#TODO far apparire più porte tra stanze
#TODO aggiungere opzione per avere percorsi tra stanze e scegliere il numero della stanza finale
#TODO far apparire più mostri nei corridoi
#TODO come capire se si ripassa da un corridoio già esplorato?

class Heroquest_solo:
    """main class for variables management"""
    rng = random.SystemRandom()
    TOTAL_NUMBER_OF_TURNS = rng.randint(10, 12)

    rng = random.SystemRandom()
    MAX_ROOM_COUNTER = rng.randint(5, 6)

    CURRENT_ROOM_COUNTER = 0

    MISSION_PERCENT_MADE = 0

    ESCAPE_FOUND = 0

    FIRST_ROOM = 0

    CONFIG_DICT = ''


    THE_MISSION = ''

    SPECIAL_ROOM_CHARGED = ''

    MONSTER_CLASS = ''

    POV_LIST = []

    ROOMS_NUMBERS_LIST = []

    PRIMARY_PATH = []
    START_FROM = ''
    ARRIVE_TO = ''  # randomly selected by the app from point of views kesy
    MIN_PATH = 4  # randomly selected by the app between 3 and 6

    SECONDARY_PATH = []
    THE_SECONDARY_START = ''
    THE_SECONDARY_ARRIVE = ''
    THE_SECONDARY_MIN_PATH = ''

    COMPLEX_PATH = []

    POINT_OF_VIEW_EXPLORED = []

    DUNGEON_EXPLORED = []

    ROOMS_EXPLORED_LAST_TURN = 0

    DOORS_TO_ROOMS_APPLIED = []

    ROOMS_EXPLORED = []

    CONNECTION = sqlite3.connect('./db_heroquest_legends.sqlite')
    CURSOR = CONNECTION.cursor()

    NEW_DATA_TO_TEST_DELETE = 0

    ROOMS_RANDOM_EVENTS = []

    """DATA FROM DATABASE"""
    #charge alls the fornitures linked to ID
    db_fornitures_query = CURSOR.execute("Select * from fornitures")
    db_fornitures_charged = db_fornitures_query.fetchall()

    #charge alls the monsters linked to ID
    db_monsters_query = CURSOR.execute("Select * from monsters")
    db_monsters_charged = db_monsters_query.fetchall()


    FORNITURES_QTY_DICT = {"1":db_fornitures_charged[0][2],
                           "2":db_fornitures_charged[1][2],
                           "3":db_fornitures_charged[2][2],
                           "4":db_fornitures_charged[3][2],
                           "5":db_fornitures_charged[4][2],
                           "6":db_fornitures_charged[5][2],
                           "7":db_fornitures_charged[6][2],
                           "8":db_fornitures_charged[7][2],
                           "9":db_fornitures_charged[8][2],
                           "10":db_fornitures_charged[9][2],
                           "11":db_fornitures_charged[10][2],
                           "12":db_fornitures_charged[11][2],
                           "13":db_fornitures_charged[12][2]}

    MONSTERS_QTY_DICT = {"1":db_monsters_charged[0][2],
                         "2":db_monsters_charged[1][2],
                         "3":db_monsters_charged[2][2],
                         "4":db_monsters_charged[3][2],
                         "5":db_monsters_charged[4][2],
                         "6":db_monsters_charged[5][2],
                         "7":db_monsters_charged[6][2],
                         "8":db_monsters_charged[7][2],
                         "9":db_monsters_charged[8][2]}

    MONSTERS_COMBAT_VALUES_DICT = {"1":db_monsters_charged[0][4],
                                   "2":db_monsters_charged[1][4],
                                   "3":db_monsters_charged[2][4],
                                   "4":db_monsters_charged[3][4],
                                   "5":db_monsters_charged[4][4],
                                   "6":db_monsters_charged[5][4],
                                   "7":db_monsters_charged[6][4],
                                   "8":db_monsters_charged[7][4],
                                   "9":db_monsters_charged[8][4]}

    MONSTERS_CATEGORY = {"1":db_monsters_charged[0][1],
                         "2":db_monsters_charged[1][1],
                         "3":db_monsters_charged[2][1],
                         "4":db_monsters_charged[3][1],
                         "5":db_monsters_charged[4][1],
                         "6":db_monsters_charged[5][1],
                         "7":db_monsters_charged[6][1],
                         "8":db_monsters_charged[7][1],
                         "9":db_monsters_charged[8][1]
                         }

    """DATA FROM INTERNAL DICT FOR DUNGEON GENERATION"""
    POINT_OF_VIEW = {
        "A": ("1", "4"),
        "B": ("1", "2"),
        "C": ("2", "3"),
        "D": ("3", "4"),
        "E": ("1", "5", "6"),
        "F": ("2", "6", "7"),
        "G": ("3", "7", "8"),
        "H": ("4", "5", "8"),
        "1": ("A", "B", "E"),
        "2": ("B", "C", "F"),
        "3": ("C", "D", "G"),
        "4": ("A", "D", "H"),
        "5": ("E", "H"),
        "6": ("E", "F"),
        "7": ("F", "G"),
        "8": ("G", "H")}

    DUNGEON_TO_ROOM = {
        "A1": ("401", "402", "403"),
        "B1": ("301", "302", "303"),
        "B2": ("301", "304"),
        "C2": ("201", "204"),
        "C3": ("201", "202", "203"),
        "D3": ("101", "102", "103"),
        "D4": ("101", "104"),
        "A4": ("401", "404"),
        "E1": ("303", "403", "501"),
        "E5": ("403", "406", "501"),
        "E6": ("303", "305", "501"),
        "F2": ("204", "205", "304", "305", "501"),
        "F6": ("303", "305", "501"),
        "F7": ("203", "205", "501"),
        "G3": ("103", "203", "501"),
        "G7": ("203", "205", "501"),
        "G8": ("103", "105", "501"),
        "H4": ("104", "105", "404", "405", "406", "501"),
        "H5": ("403", "406", "501"),
        "H8": ("103", "105", "501")}

    ROOM_TO_ROOM = {
        "101": ("102", "104"),
        "102": ("101", "103", "105"),
        "103": ("102", "105"),
        "104": ("101", "105"),
        "105": ("102", "103", "104"),

        "201": ("202", "204"),
        "202": ("201", "203", "205"),
        "203": ("202", "205"),
        "204": ("201", "205"),
        "205": ("202", "203", "204"),

        "301": ("302", "304"),
        "302": ("301", "303", "305"),
        "303": ("302", "305"),
        "304": ("301", "305"),
        "305": ("302", "303", "304"),

        "401": ("402", "404"),
        "402": ("401", "403", "404", "405", "406"),
        "403": ("402"),
        "404": ("401", "404", "405", "406"),
        "405": ("402", "404", "406"),
        "406": ("402", "405")}

    ROOM_TO_DUNGEON = {
        "101": ("D3", "D4"),
        "102": ("D3"),
        "103": ("D3", "G3", "G8"),
        "104": ("D4", "H4"),
        "105": ("H4", "H8"),

        "201": ("C2", "C3"),
        "202": ("C3"),
        "203": ("C3", "G3", "G7"),
        "204": ("C2", "F2"),
        "205": ("F2", "F7"),

        "301": ("B1", "B2"),
        "302": ("B1"),
        "303": ("B1", "E1", "E6"),
        "304": ("B2", "F2"),
        "305": ("F2", "F6"),

        "401": ("A1", "A4"),
        "402": ("A1"),
        "403": ("A1", "E1"),
        "404": ("A4", "H4"),
        "405": ("H4"),
        "406": ("H4", "H5"),

        "501": (
        "E1", "E5", "E6", "F2", "F6", "F7", "G3", "G7", "G8",
        "H4", "H5", "H8")}

    ROOMS_NUM_TILES = {
        '101': 12,
        '102': 12,
        '103': 15,
        '104': 20,
        '105': 20,
        '201': 16,
        '202': 16,
        '203': 15,
        '204': 16,
        '205': 16,
        '301': 16,
        '302': 12,
        '303': 20,
        '304': 16,
        '305': 15,
        '401': 16,
        '402': 20,
        '403': 15,
        '404': 16,
        '405': 6,
        '406': 6,
        '501': 30}



    def __init__(self, cd):
        """The class is instanced with dictionary from config file"""
        self.CONFIG_DICT = cd
        #self.r_num = random

        #position dict
        self.position_dict = self.CONFIG_DICT["position_dict"]

        #fornitures dict
        self.forniture_dict = self.CONFIG_DICT['fornitures_dict']

        #treasures dict that you can find inside a cest or in other forniture
        self.treasures_card_dict =  self.CONFIG_DICT['treasures_card_dict']

        #monsters dict that you can find inside a Room or in a aisle
        self.monsters_dict = self.CONFIG_DICT['monsters_dict']

    def special_data_mission_charged(self, mn):
        self.THE_MISSION = "{}".format(mn)
        print("THE MISSION")
        print(self.THE_MISSION)
        self.SPECIAL_ROOM_CHARGED = self.CONFIG_DICT["specials_rooms"][self.THE_MISSION]
        print("SPECIAL ROOM CHARGED")
        print(self.SPECIAL_ROOM_CHARGED)
        self.MONSTER_CLASS = self.CONFIG_DICT["monster_class"][self.THE_MISSION]

        #remove_forniture_for_special_room
        id_forniture_special_room_list = self.SPECIAL_ROOM_CHARGED[0] #charge id list
        print("special room list:"+str(id_forniture_special_room_list))
        for i in id_forniture_special_room_list:
            values_str = "{}".format(i)
            print("VALUES STRS")
            print(str(values_str))
            tot_forniture = self.FORNITURES_QTY_DICT[values_str]
            new_tot_forniture = tot_forniture-1
            self.FORNITURES_QTY_DICT[values_str] = new_tot_forniture

    def charge_point_of_views(self):
        for keys in self.POINT_OF_VIEW.keys():
            self.POV_LIST.append(keys)
        return self.POV_LIST

    def charge_rooms_numbers(self):
        for keys in self.ROOMS_NUM_TILES.keys():
            self.ROOMS_NUMBERS_LIST.append(keys)
        return self.ROOMS_NUMBERS_LIST

    def random_numbers(self):
        """ a random number generator based on four D6.
        A simple statistic to understand the probability of success
        >= X == y%
        4 = 100%
        5 = 99.92%
        6 = 99.61%
        7 = 98.84%
        8 = 97.30%
        9 = 94.60%
        10 = 90.28%
        11 = 84.10%
        12 = 76.08%
        13 = 66.44%
        14 = 55.63%
        15 = 44.37%
        16 = 33.50%
        17 = 23.92%
        18 = 15.90%
        19 = 9.72%
        20 = 5.40%
        21 = 2.70%
        22 = 1.16%
        23 = 0.39%
        24 = 0.08% """

        rng = random.SystemRandom()
        value_1 = rng.randint(1, 6)

        rng = random.SystemRandom()
        value_2 = rng.randint(1, 6)

        rng = random.SystemRandom()
        value_3 = rng.randint(1, 6)

        rng = random.SystemRandom()
        value_4 = rng.randint(1, 6)

        rn_list = [value_1, value_2, value_3, value_4]

        rn_sum = sum(rn_list)

        return rn_sum

    def mission_percent_made(self, ct):
        current_turn = ct

        total_comparison_value = self.TOTAL_NUMBER_OF_TURNS+self.MAX_ROOM_COUNTER
        partial_comparison_value =current_turn+self.CURRENT_ROOM_COUNTER

        self.MISSION_PERCENT_MADE = (partial_comparison_value/total_comparison_value)*100

        #TODO TO DELETE
        total_turn = "total_turns_made {}".format(self.TOTAL_NUMBER_OF_TURNS)
        total_rooms = "total_rooms {}".format(self.MAX_ROOM_COUNTER)
        current_turn_made = "current_turn_made {}".format(current_turn)
        current_room_made = "current_room_made {}".format(self.CURRENT_ROOM_COUNTER)
        totale_percent_made = "total_percent_made {}".format(self.MISSION_PERCENT_MADE)

    def permutation_sum(self,l):
        """NEW SYSTEM FOR ROOM GENERATION NOT USED BY NOW"""

        sum(l)
        if s == self.N:
            self.RES.append(l)
            return
        elif s > self.N:
            return
        for x in range(1, self.N + 1):
            self.permutation_sum(l + [x])
    """
    def room_generator_2(self, room_dimension, ct, re):
        #NEW SYSTEM FOR ROOM GENERATION NOT USED BY NOW
        #create random rooms with fornitures 2

        #create random rooms with fornitures
        #turn controller INPUT

        self.current_turn = ct

        #room controller INPUT
        self.room_explored = int(re)
        rng = random.SystemRandom()
        value = rng.randint(1, 2)

        self.room_dimension = int(room_dimension)/value #total of room's tiles

        #forniture_square_taken
        tot_square_taken = 0

        #messages controller
        msg_forniture = ''
        msg_monsters = ''
        msg_end = ''
        msg_list = []

        #roll the dice and select a random number of fornitures between 1 and 3
        rng = random.SystemRandom()
        forniture_numbers = rng.randint(1, 4)
        count = 0

        ac = Permutation_class(int(self.room_dimension))
        ac.rec([])
        dimensions_list = Permutation_class.res
        len_list_options= len(dimensions_list)
        rng = random.SystemRandom()
        slice_number = rng.randint(1, int(len_list_options))
        """


    def room_generator(self, room_dimension, ct, re):
        """create random rooms with fornitures"""
        #turn controller INPUT

        self.current_turn = ct

        #room controller INPUT
        self.room_explored = int(re)
        rng = random.SystemRandom()
        value = rng.randint(1, 2)
        rng = random.SystemRandom()
        room_dimension = int(room_dimension)-rng.randint(1, 2)
        self.room_dimension = int(room_dimension)/value #total of room's tiles

        #forniture_square_taken
        tot_square_taken = 0

        #messages controller
        msg_forniture = ''
        msg_monsters = ''
        msg_end = ''
        msg_list = []

        #roll the dice and select a random number of fornitures between 1 and 3
        rng = random.SystemRandom()
        forniture_numbers = rng.randint(1, 4)
        #count = 0
        #if the current turn is max or equal and the escape is founded
        print("room gen 1")
        if self.room_explored == 0:
            if self.CURRENT_ROOM_COUNTER < self.MAX_ROOM_COUNTER:
                self.CURRENT_ROOM_COUNTER += 1
        if self.current_turn >= self.TOTAL_NUMBER_OF_TURNS and self.ESCAPE_FOUND==0 and self.room_explored == 0 and self.CURRENT_ROOM_COUNTER >= self.MAX_ROOM_COUNTER:
            print("room gen 2")

            msg_end = self.SPECIAL_ROOM_CHARGED[1] #Replace the number with THE_MISSION = RAND_NUM
            self.ESCAPE_FOUND = 1
            print("room gen 3")

        else:
            if self.room_explored == 0: #if the room is not explored
                count = 0 #counter
                for i in range(forniture_numbers):
                    rng_0 = random.SystemRandom()
                    alea = rng_0.randint(0, 10)
                    if alea <= 4:
                        rng_1 = random.SystemRandom()
                        id_forniture_rand = rng_1.randint(12, 13)
                    else:
                        rng_1 = random.SystemRandom()
                        id_forniture_rand_1 = rng_1.randint(0, 6)

                        rng_2 = random.SystemRandom()
                        id_forniture_rand_2 = rng_2.randint(1, 5)  #create a random ID for fornitures between 1 and 13

                        id_forniture_rand = str(id_forniture_rand_1+id_forniture_rand_2)

                    #verify if the fornitures is still present
                    print("room gen 10")

                    forniture_residue = self.FORNITURES_QTY_DICT[str(id_forniture_rand)]

                    if forniture_residue > 0:
                        # charge from DB the selected fornitures
                        print("room gen 11")
                        query_select = '{}{}'.format("SELECT * FROM fornitures WHERE id_forniture = ", id_forniture_rand)
                        res = self.CURSOR.execute(query_select)
                        forniture_selected = res.fetchone()

                        print("room gen 13"+query_select)
                        square_taken_temp = forniture_selected[4]
                        tot_square_taken += square_taken_temp
                        #if there is residue space in rooms
                        print("room gen 14")
                        if tot_square_taken < self.room_dimension:
                            if count == 0:
                                print("room gen 15")
                                if id_forniture_rand == "11" or id_forniture_rand == "12":
                                    rng = random.SystemRandom()
                                    msg_forniture = '{} {} {};'.format(msg_forniture, self.forniture_dict[str(id_forniture_rand)],self.position_dict[str(rng.randint(1, 3))])
                                    print("room gen 16")
                                else:
                                    rng = random.SystemRandom()
                                    msg_forniture = '{} {} {};'.format(msg_forniture, self.forniture_dict[str(id_forniture_rand)],self.position_dict[str(rng.randint(1, 5))])
                                new_forniture_residue = forniture_residue - 1
                                self.FORNITURES_QTY_DICT[id_forniture_rand] = new_forniture_residue
                                count = 1
                            else:
                                rng = random.SystemRandom()
                                msg_forniture = '{} {} {};'.format(msg_forniture, self.forniture_dict[str(id_forniture_rand)],
                                                                 self.position_dict[str(rng.randint(1, 5))])
                                new_forniture_residue = forniture_residue - 1
                                self.FORNITURES_QTY_DICT[str(id_forniture_rand)] = new_forniture_residue
                        else: #no forniture is added and the temporary squares is re added
                            print("room gen 18")
                            tot_square_taken -= square_taken_temp
                    else: #if the forniture is not present
                        print("room gen 19")
                        msg_forniture = msg_forniture
                if msg_forniture != '':
                    print("room gen 20")
                    msg_rand = rng.randint(0, 3)
                    aux_message = ['aux_msg_2', 'aux_msg_3', 'aux_msg_4', 'aux_msg_5']
                    msg_forniture = '{} {}.'.format(self.CONFIG_DICT[aux_message[msg_rand]], msg_forniture)
            else:
                print("room gen 21")
                msg_forniture = self.CONFIG_DICT['aux_msg_7']

        #generate the room
        if self.FIRST_ROOM == 1:
            print("room gen 22")
            if self.ESCAPE_FOUND == 2:
                print("room gen 22.1")
                msg_monsters = self.monsters_generator_2(self.random_numbers(),tot_square_taken, self.current_turn,0)
            if self.ESCAPE_FOUND == 0:
                print("room gen 22.2")
                msg_monsters = self.monsters_generator_2(self.random_numbers(),tot_square_taken, self.current_turn,0)
            if self.ESCAPE_FOUND == 1:
                print("room gen 22.3")
                msg_monsters = self.monsters_generator_2(self.random_numbers(),tot_square_taken, self.current_turn,1)
                self.ESCAPE_FOUND = 2
        else:
            print("room gen 23")
            msg_monsters = self.CONFIG_DICT['monsters_msg_first_room']
            self.FIRST_ROOM = 1
        print("room gen 25")
        msg_list.append(msg_forniture)
        msg_list.append(msg_monsters)
        msg_list.append(msg_end)

        return msg_list

    def monsters_generator_2(self, rv, square_taken, ct,n):
        """create random group of monsters based on squares taken by fornitures"""
        self.rv = rv #the random values to know to create the percentage of possibilities to find monsters

        self.residual_tiles = int(square_taken) #total of room's tiles residue
        self.current_turn = ct
        self.n = n #if in this turn the special room is founded

        msg_monsters = ''
        monsters_msg_partial = ''
        print("monst gen 1")
        if self.rv >= 20:
            print("monst gen 2")
            return '{} {}'.format(msg_monsters, self.CONFIG_DICT['monsters_msg_2'])
        else:
            print("monst gen 3")

            if self.residual_tiles >= 0 and self.residual_tiles <= 3:
                print("monst gen 4")
                rng_base = random.SystemRandom()
                monsters_number = rng_base.randint(1, 2)
            elif self.residual_tiles > 3 and self.residual_tiles <= 6:
                print("monst gen 5")
                rng_base = random.SystemRandom()
                monsters_number = rng_base.randint(1, 5)
            elif self.residual_tiles > 6 and self.residual_tiles <= 12:
                print("monst gen 6")

                rng_base = random.SystemRandom()
                monsters_number = rng_base.randint(1, 6)
            elif self.residual_tiles > 12 and self.residual_tiles <= 30:
                print("monst gen 8")

                rng_base = random.SystemRandom()
                monsters_number = rng_base.randint(4, 6)
            else:
                print("monst gen 9")

                rng_base = random.SystemRandom()
                monsters_number = 1
            print("monst gen 10")
            query_string_base="Select id_monster from monsters where "
            query_string_where = ""
            print("monst class lenght: "+str(len(self.MONSTER_CLASS)))
            for cm in self.MONSTER_CLASS:
                if query_string_where == "":
                    query_string_where = "monster_class = '{}' or monster_class LIKE '%{}' or monster_class LIKE '{}%' or monster_class LIKE '%{}%'".format(cm, cm, cm, cm)
                    print("monst gen 10.1: "+query_string_where)
                else:
                    query_string_where += " or monster_class = '{}' or monster_class LIKE '%{}' or monster_class LIKE '{}%' or monster_class LIKE '%{}%'".format(cm, cm, cm, cm)
                    print("monst gen 10.2: " + query_string_where)
            print("monst gen 11")
            query_string = '{} {}'.format(query_string_base, query_string_where)

            print("monst gen 12")

            for i in range(monsters_number):
                #choose id based on monster class
                print("monst gen 12.1")
                print(query_string)
                db_monsters_class_query = self.CURSOR.execute(query_string)
                print("monst gen 12.2")
                db_monsters_class_charged = db_monsters_class_query.fetchall()
                print("monst gen 12.3")
                db_monsters_class_charged_list = []
                print("monst gen 13")
                for i in db_monsters_class_charged:
                    db_monsters_class_charged_list.append(i[0])
                print("monst gen 14")
                db_monsters_class_charged_lenght = len(db_monsters_class_charged_list)-1
                rng = random.SystemRandom()
                id_monster_rand = db_monsters_class_charged_list[rng.randint(0, db_monsters_class_charged_lenght)]
                print("monst gen 15")
                monsters_residue = int(self.MONSTERS_QTY_DICT[str(id_monster_rand)])
                print("monst gen 16")
                if monsters_residue > 0:
                    print("monst gen 17")
                    rng = random.SystemRandom()
                    monsters_msg_partial = '{} {} {};'.format(monsters_msg_partial,
                                                              self.monsters_dict[str(id_monster_rand)],
                                                              self.position_dict[str(rng.randint(1, 5))])

                    new_monster_residue = int(monsters_residue) - 1

                    self.MONSTERS_QTY_DICT[str(id_monster_rand)] = new_monster_residue
            print("monst gen 18")
            if monsters_msg_partial != '':
                msg_monsters = '{} {} {}'.format(self.CONFIG_DICT['monsters_msg_intro'], monsters_msg_partial, self.CONFIG_DICT['monsters_msg_close'])
            else:
                if self.n == 0:
                    msg_monsters = '{} {}'.format(self.CONFIG_DICT['monsters_msg_intro'],self.CONFIG_DICT['monsters_msg_2'])
                else:
                    msg_monsters = '{} {}'.format(self.CONFIG_DICT['monsters_msg_intro'],self.CONFIG_DICT['monsters_msg_5'])

        return msg_monsters

    def random_monsters_on_aisles(self, n):
        turn = n
        self.mission_percent_made(turn)
        rn = self.random_numbers()
        comparison_value = 0
        if self.MISSION_PERCENT_MADE >= 100:
            comparison_value = 5
        elif self.MISSION_PERCENT_MADE >= 70:
            comparison_value = 10
        elif self.MISSION_PERCENT_MADE >= 20:
            comparison_value = 18
        else:
            comparison_value = 15

        if rn >= comparison_value:

            query_string_base="Select id_monster from monsters where "
            query_string_where = ""
            for cm in self.MONSTER_CLASS:
                if query_string_where == "":
                    query_string_where = "monster_class = '{}' or monster_class LIKE '%{}' or monster_class LIKE '{}%' or monster_class LIKE '%{}%'".format(cm, cm, cm, cm)
                else:
                    query_string_where += " or monster_class = '{}' or monster_class LIKE '%{}' or monster_class LIKE '{}%' or monster_class LIKE '%{}%'".format(cm, cm, cm, cm)

            query_string = '{} {}'.format(query_string_base, query_string_where)

            db_monsters_class_query = self.CURSOR.execute(query_string)
            db_monsters_class_charged = db_monsters_class_query.fetchall()
            db_monsters_class_charged_list = []
            for i in db_monsters_class_charged:
                db_monsters_class_charged_list.append(i[0])

            db_monsters_class_charged_lenght = len(db_monsters_class_charged_list) - 1
            rng = random.SystemRandom()
            id_monster_rand = db_monsters_class_charged_list[rng.randint(0, db_monsters_class_charged_lenght)]
            monsters_residue = self.MONSTERS_QTY_DICT[str(id_monster_rand)]

            if monsters_residue > 0:
                msg_monsters = self.CONFIG_DICT['aux_msg_9'].format(self.monsters_dict[str(id_monster_rand)])
                new_monster_residue = monsters_residue - 1
                self.MONSTERS_QTY_DICT[str(id_monster_rand)] = new_monster_residue
                if msg_monsters == "":
                    return "Per ora tutto ok!" #TODO sistemare il null
                else:
                    return msg_monsters
            else:
                return self.CONFIG_DICT['aux_msg_10']
        else:
            return self.CONFIG_DICT['aux_msg_10']



    def put_the_doors(self, d):
        """"Receive the POV and describe where are the doors"""
        print("PUT_THE_DOORS 1")
        dungeon_id = d
        print("PUT_THE_DOORS 3")
        rooms_tup = self.DUNGEON_TO_ROOM[dungeon_id]
        print("PUT_THE_DOORS 4")
        rooms_list = []
        for e in rooms_tup:
            rooms_list.append(e)
        for i in rooms_list:
            if i in self.ROOMS_EXPLORED or i in self.DOORS_TO_ROOMS_APPLIED:
                rooms_list.remove(i)
        door_msg = ''
        if len(rooms_list) > 0:
            for room_num in rooms_list:
                num = self.random_numbers()

                if num >=12 and self.FORNITURES_QTY_DICT["13"]>=1 and room_num not in self.ROOMS_EXPLORED and room_num not in self.DOORS_TO_ROOMS_APPLIED:
                    rng = random.SystemRandom()
                    self.DOORS_TO_ROOMS_APPLIED.append(str(room_num))
                    door_type_msg = rng.randint(1, 2)
                    if door_type_msg == 1:
                        print("Door type ms 1")
                        door_msg += self.CONFIG_DICT["dungeon_msg_01"].format(str(room_num))
                        new_doors_residue = self.FORNITURES_QTY_DICT["13"] - 1
                        self.FORNITURES_QTY_DICT["11"] = new_doors_residue
                    else:
                        print("Door msg plus")
                        door_msg += self.CONFIG_DICT['dungeon_msg_02'].format(str(room_num))
                        new_doors_residue = self.FORNITURES_QTY_DICT["13"] - 1
                        self.FORNITURES_QTY_DICT["11"] = new_doors_residue
                else:
                    print("Door pass to verify")
                    pass #TODO VERIFY THIS PASS....
                    #door_msg += "No doors for room {}. \n".format(str(room_num))
            print("door_msg 9867: " + str(door_msg))
        else:
            door_msg = self.CONFIG_DICT['dungeon_msg_22']
        print("door_msg: 6587"+door_msg)
        return door_msg


    def how_is_the_dungeon(self, pv, r):
        print("How_is_the_dungeon")
        """DESCRIBE THE DUNGEON MAIN BASED ON PRIMARY PATH AND SECONDARY PATH. THERE ARE MANY DIFFERENT CASE
        THAT THIS FUNCTION ANALYSE AND PASS TO def run_how_is_the_dungeon"""

        pointofview = pv
        round = r

        msg = self.CONFIG_DICT['dungeon_msg_00'].format(str(round))

        #ESTENSIONE DEL PRIMO PATH DAL PRIMO A PARTIRE DAL PRIMO PUNTO DEL PRIMARY PATH
        if pointofview == self.START_FROM and pointofview == self.THE_SECONDARY_START:
            print("HITD OP1")
            pov_direction = self.run_how_is_the_dungeon(pointofview, 1)
            msg += self.CONFIG_DICT['dungeon_msg_13'].format(str(pov_direction))
            self.POINT_OF_VIEW_EXPLORED.append(pointofview)
            return msg

        # ESTENSIONE DALL'ULTIMO PUNTO DEL PRIMARY PATH
        elif pointofview == self.ARRIVE_TO and pointofview == self.THE_SECONDARY_START:
            print("HITD OP2")
            pov_direction = self.run_how_is_the_dungeon(pointofview, 2)
            msg += self.CONFIG_DICT['dungeon_msg_14'].format(str(pov_direction))
            self.POINT_OF_VIEW_EXPLORED.append(pointofview)

            return msg

        #BIFORCAZIONE AL CENTRO se il punto corrente corrisponde a qualcosa in primary path e inizio del secondario: alla biforcazione
        elif pointofview in self.PRIMARY_PATH and pointofview == self.THE_SECONDARY_START:
            print("HITD OP3")
            pov_direction = self.run_how_is_the_dungeon(pointofview, 3)

            msg += self.CONFIG_DICT['dungeon_msg_15'].format(str(pov_direction)) #self.CONFIG_DICT['dungeon_msg_12'].format(str(next_pov_primary),str(next_pov_secondary))
            self.POINT_OF_VIEW_EXPLORED.append(pointofview)

            return msg

        elif pointofview == self.START_FROM:
            print("HITD OP4")
            pov_direction = self.run_how_is_the_dungeon(pointofview, 4)
            msg += self.CONFIG_DICT['dungeon_msg_16'].format(str(pov_direction))
            self.POINT_OF_VIEW_EXPLORED.append(pointofview)

            return msg


        elif pointofview == self.ARRIVE_TO:
            print("HITD OP5")
            pov_direction = self.run_how_is_the_dungeon(pointofview, 5)
            msg += self.CONFIG_DICT['dungeon_msg_17'].format(pov_direction)
            self.POINT_OF_VIEW_EXPLORED.append(pointofview)

            return msg

        elif pointofview == self.THE_SECONDARY_ARRIVE:
            print("HITD OP6 a")
            pov_direction = self.run_how_is_the_dungeon(pointofview, 6)
            print("HITD OP6 b")
            msg += self.CONFIG_DICT["dungeon_msg_18"].format(pov_direction)
            print("HITD OP6 c")
            self.POINT_OF_VIEW_EXPLORED.append(pointofview)
            print("HITD OP6 d")
            return msg

        elif pointofview in self.PRIMARY_PATH:
            print("HITD OP7")
            pov_direction = self.run_how_is_the_dungeon(pointofview, 7)
            msg += self.CONFIG_DICT['dungeon_msg_19'].format(pov_direction)
            self.POINT_OF_VIEW_EXPLORED.append(pointofview)
            return msg

        elif pointofview in self.SECONDARY_PATH:
            print("HITD OP8")
            pov_direction = self.run_how_is_the_dungeon(pointofview, 8)
            msg += self.CONFIG_DICT['dungeon_msg_19'].format(pov_direction)
            self.POINT_OF_VIEW_EXPLORED.append(pointofview)
            return msg

        elif pointofview not in self.COMPLEX_PATH:
            print("HITD OP9")
            msg += self.CONFIG_DICT['dungeon_msg_20']
            self.POINT_OF_VIEW_EXPLORED.append(pointofview)
            return msg


    def run_how_is_the_dungeon(self, pov, sn):
        """DUNGEON CREATION SYSTEM: DESCRIBE THE DUNGEON STARTING FROM A POV AND A CASE, BASED ON
        POV AND PRIMARY AND SECONDARY PATH"""
        self.pointofview_l = pov
        self.system_number = sn

        #carica i singoli punti di vista legati al punto di vista corrente
        single_points = self.POINT_OF_VIEW[self.pointofview_l]

        msg = self.CONFIG_DICT['dungeon_msg_23']

        if self.system_number == 1:
            pov_1 = self.PRIMARY_PATH[1]
            pov_2 = self.SECONDARY_PATH[1]

            for i in single_points:
                if i == pov_1 or i == pov_2:
                    msg += self.CONFIG_DICT['dungeon_msg_21'].format(str(i))
                    if i.isdigit() is True:
                        dungeon_id = '{}{}'.format(str(self.pointofview_l), str(i))
                        msg_doors = self.put_the_doors(dungeon_id)
                        msg += msg_doors
                    else:
                        dungeon_id = '{}{}'.format(str(i), str(self.pointofview_l))
                        msg_doors = self.put_the_doors(dungeon_id)
                        msg += msg_doors
                else:
                    if i not in self.POINT_OF_VIEW_EXPLORED:
                        msg += self.CONFIG_DICT['dungeon_msg_24'].format(str(i))

            return msg

        if self.system_number == 2:
            pov_1 = self.SECONDARY_PATH[1]

            for i in single_points:
                if i == pov_1:
                    msg += self.CONFIG_DICT['dungeon_msg_21'].format(str(i))
                    if i.isdigit() is True:
                        dungeon_id = '{}{}'.format(
                            str(self.pointofview_l), str(i))
                        msg_doors = self.put_the_doors(
                            dungeon_id)
                        msg += msg_doors
                        self.DUNGEON_EXPLORED.append(dungeon_id)
                    else:
                        dungeon_id = '{}{}'.format(str(i), str(
                            self.pointofview_l))
                        msg_doors = self.put_the_doors(
                            dungeon_id)
                        msg += msg_doors
                        self.DUNGEON_EXPLORED.append(dungeon_id)
                else:
                    if i not in self.POINT_OF_VIEW_EXPLORED:
                        msg +=  self.CONFIG_DICT['dungeon_msg_25'].format(str(i))

            return msg

        if self.system_number == 3:
            pov_1 = self.PRIMARY_PATH[self.PRIMARY_PATH.index(self.pointofview_l)+1]
            pov_3 = self.PRIMARY_PATH[self.PRIMARY_PATH.index(self.pointofview_l)-1]
            pov_2 = self.SECONDARY_PATH[1]

            for i in single_points:
                if i == pov_1 or i == pov_2 or i == pov_3 :
                    if i in self.POINT_OF_VIEW_EXPLORED:
                        msg += self.CONFIG_DICT['dungeon_msg_26'].format(str(i))
                    else:
                        msg += self.CONFIG_DICT['dungeon_msg_21'].format(str(i))
                        if i.isdigit() is True:
                            dungeon_id = '{}{}'.format(
                                str(self.pointofview_l), str(i))
                            msg_doors = self.put_the_doors(
                                dungeon_id)
                            msg += msg_doors
                            self.DUNGEON_EXPLORED.append(
                                dungeon_id)
                        else:
                            dungeon_id = '{}{}'.format(str(i),
                                                       str(
                                                           self.pointofview_l))
                            msg_doors = self.put_the_doors(
                                dungeon_id)
                            msg += msg_doors
                            self.DUNGEON_EXPLORED.append(
                                dungeon_id)

                else:
                    msg += self.CONFIG_DICT['dungeon_msg_27'].format(str(i))
            return msg

        if self.system_number == 4:
            pov_1 = self.START_FROM
            for i in single_points:
                if str(i) == self.PRIMARY_PATH[self.PRIMARY_PATH.index(pov_1)+1]:
                    msg += self.CONFIG_DICT['dungeon_msg_21'].format(str(i))
                    if i.isdigit() is True:
                        dungeon_id = '{}{}'.format(
                            str(self.pointofview_l), str(i))
                        msg_doors = self.put_the_doors(
                            dungeon_id)
                        msg += msg_doors
                        self.DUNGEON_EXPLORED.append(dungeon_id)
                    else:
                        dungeon_id = '{}{}'.format(str(i), str(
                            self.pointofview_l))
                        msg_doors = self.put_the_doors(
                            dungeon_id)
                        msg += msg_doors
                        self.DUNGEON_EXPLORED.append(dungeon_id)
                else:
                    if i not in self.POINT_OF_VIEW_EXPLORED:
                        msg += self.CONFIG_DICT['dungeon_msg_25'].format(str(i))
            return msg

        if self.system_number == 5:

            msg = self.CONFIG_DICT['dungeon_msg_28']
            return msg

        if self.system_number == 6:
            msg = self.CONFIG_DICT['dungeon_msg_29']
            for i in single_points:
                if i not in self.COMPLEX_PATH:
                    msg += self.CONFIG_DICT['dungeon_msg_24'].format(str(i))

            return msg

        if self.system_number == 7:
            for i in single_points:
                if str(i) == self.PRIMARY_PATH[self.PRIMARY_PATH.index(self.pointofview_l)+1] or str(i) == self.PRIMARY_PATH[self.PRIMARY_PATH.index(self.pointofview_l)-1]:
                    msg += self.CONFIG_DICT['dungeon_msg_30'].format(str(i))

                    if i.isdigit() is True:
                        dungeon_id = '{}{}'.format(str(self.pointofview_l), str(i))
                        msg_doors = self.put_the_doors(dungeon_id)
                        if msg_doors != '' and i not in self.POINT_OF_VIEW_EXPLORED:
                            msg += msg_doors
                            self.DUNGEON_EXPLORED.append(dungeon_id)
                        elif msg_doors != '':
                            rng_1 = random.SystemRandom()  # you'll find a weapon
                            rand_num = rng_1.randint(1, 3)
                            if rand_num == 1:
                                msg += self.CONFIG_DICT['dungeon_msg_31'].format(msg_doors)
                            elif rand_num == 2:
                                msg += self.CONFIG_DICT['dungeon_msg_32'].format(msg_doors)
                            else:
                                msg = self.CONFIG_DICT['dungeon_msg_33']

                            self.DUNGEON_EXPLORED.append(dungeon_id)
                    else:
                        dungeon_id = '{}{}'.format(str(i), str(self.pointofview_l))
                        msg_doors = self.put_the_doors(
                            dungeon_id)
                        self.DUNGEON_EXPLORED.append(dungeon_id)
                        if msg_doors != '' and i in self.POINT_OF_VIEW_EXPLORED:
                            msg += self.CONFIG_DICT['dungeon_msg_34']
                            msg += msg_doors
                            self.DUNGEON_EXPLORED.append(
                                dungeon_id)
                        elif msg_doors != '':
                            rng_1 = random.SystemRandom()  # you'll find a weapon
                            rand_num = rng_1.randint(1, 3)
                            if rand_num == 1:
                                msg += self.CONFIG_DICT['dungeon_msg_31'].format(msg_doors)
                            elif rand_num == 2:
                                msg += self.CONFIG_DICT['dungeon_msg_32'].format(msg_doors)
                            else:
                                msg = self.CONFIG_DICT['dungeon_msg_33']

                            self.DUNGEON_EXPLORED.append(
                                dungeon_id)
                elif str(i) != self.PRIMARY_PATH[-2]:
                    msg += self.CONFIG_DICT['dungeon_msg_35'].format(str(i))
                else:
                    if i not in self.COMPLEX_PATH:
                        msg += self.CONFIG_DICT['dungeon_msg_25'].format(str(i))
            return msg


        if self.system_number == 8:
            for i in single_points:
                if str(i) == self.SECONDARY_PATH[self.SECONDARY_PATH.index(self.pointofview_l)+1] or str(i) == self.SECONDARY_PATH[self.SECONDARY_PATH.index(self.pointofview_l)-1]:
                    msg += self.CONFIG_DICT['dungeon_msg_36'].format(str(i))
                    if i.isdigit() is True:
                        dungeon_id = '{}{}'.format(
                            str(self.pointofview_l), str(i))
                        msg_doors = self.put_the_doors(
                            dungeon_id)
                        msg += msg_doors
                        self.DUNGEON_EXPLORED.append(dungeon_id)
                    else:
                        dungeon_id = '{}{}'.format(str(i), str(
                            self.pointofview_l))
                        msg_doors = self.put_the_doors(
                            dungeon_id)
                        msg += msg_doors
                        self.DUNGEON_EXPLORED.append(dungeon_id)
                else:
                    if i not in self.POINT_OF_VIEW_EXPLORED:
                        msg += self.CONFIG_DICT['dungeon_msg_25'].format(str(i))
            return msg




        #TODO realizzare gli altri casi




        """
        #se il punto di vista non fa parte di nessuno dei due path = VICOLO CIECO
        if pointofview not in self.COMPLEX_PATH:
            msg += self.CONFIG_DICT['dungeon_msg_09']
            #msg += "This is a Dead-end road...you can only con back. Put Rocks to any other point of view"

        #se il punto di vista corrente non è nel path corrente e risulta già esplorato
        elif pointofview not in path and pointofview in self.POINT_OF_VIEW_EXPLORED:
            msg += self.CONFIG_DICT['dungeon_msg_10']
            #msg += "This is a strange place ... The road is blocked to POV {} \n".format(str(i))

        #se il punto correte è l'ultimo del path che si sta seguendo
        elif pointofview == path[-1] or pointofview == self.ARRIVE_TO or pointofview == self.THE_SECONDARY_ARRIVE:
            msg += self.CONFIG_DICT['dungeon_msg_11']
            #msg += "This is a Dead-end road...you can only con back. Put Rocks to any other point of view"

        #se il punto corrente corrisponde alla biforcazione
        elif pointofview == self.THE_SECONDARY_START:
            try:
                next_pov_primary = self.PRIMARY_PATH[self.PRIMARY_PATH.index(pointofview)+1]
            except:
                pass
            next_pov_secondary = self.SECONDARY_PATH[self.SECONDARY_PATH.index(pointofview)+1]
            msg += self.CONFIG_DICT['dungeon_msg_12'].format(str(next_pov_primary),str(next_pov_secondary))


        elif pointofview == self.THE_SECONDARY_ARRIVE:
            msg += self.CONFIG_DICT['dungeon_msg_11']

        #else:
        #per ogni punto di vista legato al punto di vista corrente
        for i in single_points:
            if i not in self.COMPLEX_PATH:
                #STRADA BLOCCATA VERSO OGNI ALTRA VIA...vi state smarrendo
                msg += self.CONFIG_DICT['dungeon_msg_13'].format(str(i))
            else:
                #se il POV fa parte dei percorsi

                #se il POV è l'ultimo del path corrente e il punto di vista è diverso dal pov iniziale del path corrente
                #si può preseguire
                if i == path[-1] and pointofview != path[0]:
                    msg += self.CONFIG_DICT['dungeon_msg_08'].format(str(i))
                    if i.isdigit() == True:
                        dungeon_id = '{}{}'.format(str(pointofview), str(i))
                        msg_doors = self.put_the_doors(dungeon_id)
                        msg += msg_doors
                    else:
                        dungeon_id = '{}{}'.format(str(i), str(pointofview))
                        msg_doors = self.put_the_doors(dungeon_id)
                        msg += msg_doors
                else:
                    try:
                        index_number = path.index(pointofview)+1
                        #se il punto di vista che si vede dal POV corrente successivo è uguale al
                        #pov successivo nel path corrente e non è stato esplorato metti le porte
                        if i == path[index_number] and i not in self.POINT_OF_VIEW_EXPLORED :  #IF i the next pov
                            msg += self.CONFIG_DICT['dungeon_msg_03'].format(str(i))
                            if i.isdigit() == True:
                                dungeon_id = '{}{}'.format(str(pointofview), str(i))
                                msg_doors = self.put_the_doors(dungeon_id)
                                msg += msg_doors
                            else:
                                dungeon_id = '{}{}'.format(str(i), str(pointofview))
                                msg_doors = self.put_the_doors(dungeon_id)
                                msg += msg_doors
                        # se il punto di vista che si vede dal POV corrente successivo è uguale al
                        #è diverso dai punti fi vista successivi del path corrente e i è stato esplorato
                        elif i != path[index_number] and i in self.POINT_OF_VIEW_EXPLORED:
                            msg += self.CONFIG_DICT['dungeon_msg_04'].format(str(i))

                        elif i == path[index_number] and i in self.POINT_OF_VIEW_EXPLORED and i != self.THE_SECONDARY_START:
                            msg += self.CONFIG_DICT['dungeon_msg_05'].format(str(i))

                        elif i != path[index_number] and i not in self.POINT_OF_VIEW_EXPLORED and i != self.THE_SECONDARY_START and i not in self.SECONDARY_PATH:
                            msg += self.CONFIG_DICT['dungeon_msg_06'].format(str(i))
                    except:
                        pass
                                    #"The dungeon continues through the darkness but the roof doesn't appear solid,you can walk to POV {} if you obtain a shield after launching a combat dice".format(str(i))
                    """


    def create_the_dungeon(self):
        print("Create the dungeon 0")
        """THIS FUNCTION CREATE THE DUNGEON. WILL BE GENERATED 2 PATH, PRIMARY AND SECONDARY"""
        pov_list = list(self.POINT_OF_VIEW.keys())
        pov_length = len(pov_list)-1
        #INSERT VALUES
        rng_n = random.SystemRandom()
        pov_length_rand = pov_length-rng_n.randint(1, 3)
        start = pov_list[rng_n.randint(0, pov_length_rand)] #CHOOSED RANDOMLY BY THE GAME
        print("start: {}".format(start))
        rng_n = random.SystemRandom()
        pov_length_rand = pov_length - rng_n.randint(2, 4)
        arrive = pov_list[rng_n.randint(0, pov_length_rand)] #CHOOSED RANDOMLY BY THE GAME
        print("arrive: {}".format(arrive))
        rng_n = random.SystemRandom()
        min_path = rng_n.randint(4, 6) #CHOOSED RANDOMLY BY THE GAME
        print("Create the dungeon 1")

        #the_primary_path = ''
        #THEN PUSH THE BUTTON
        #self.PRIMARY_PATH = ''
        #self.SECONDARY_PATH = ''
        print("Create the dungeon 2 - first run 7 find route")
        print("start: {}".format(start))
        print("arrive: {}".format(arrive))
        self.PRIMARY_PATH = self.find_route(start, arrive)
        while len(self.PRIMARY_PATH) < min_path or arrive != self.PRIMARY_PATH[-1]:
            self.PRIMARY_PATH = self.find_route(start, arrive)
        print("Create the dungeon 3")

        #THE GAME CHOOSE A SECONDARY PATH
        half = len(self.PRIMARY_PATH) // 2
        the_secondary_path_temp = self.PRIMARY_PATH[0:half]
        print("Create the dungeon 4")

        for i in self.POINT_OF_VIEW.keys():
            if i not in self.PRIMARY_PATH:
                self.THE_SECONDARY_ARRIVE = i
                break
        print("Create the dungeon 5")
        self.THE_SECONDARY_START = the_secondary_path_temp[-1]
        #CHOOSED RANDOMLY BY THE GAME

        self.THE_SECONDARY_MIN_PATH = len(self.PRIMARY_PATH)-2 #the current path lenght of primary_path
        #the_path = ''

        #THEN PUSH THE BUTTON

        #INSERT VALUES

        #THEN PUSH THE BUTTON
        print("Create the dungeon 6 - second run find route")
        print("II start: {}".format(self.THE_SECONDARY_START))
        print("II arrive: {}".format(self.THE_SECONDARY_ARRIVE))
        self.SECONDARY_PATH = self.find_route(self.THE_SECONDARY_START,self.THE_SECONDARY_ARRIVE)
        while self.THE_SECONDARY_ARRIVE != self.SECONDARY_PATH[-1]: # len(self.SECONDARY_PATH) >= len(self.PRIMARY_PATH) or
            self.SECONDARY_PATH = self.find_route(self.THE_SECONDARY_START, self.THE_SECONDARY_ARRIVE)

        print("Create the dungeon 7")

        third_path_temp = []
        for i in self.SECONDARY_PATH:
            if i in self.PRIMARY_PATH and self.SECONDARY_PATH[self.SECONDARY_PATH.index(i) + 1] not in self.PRIMARY_PATH:
                third_path_temp.append(i)
            elif i not in self.PRIMARY_PATH:
                third_path_temp.append(i)
        print("Create the dungeon 8")

        self.SECONDARY_PATH = third_path_temp

        self.START_FROM = self.PRIMARY_PATH[0]
        self.ARRIVE_TO = self.PRIMARY_PATH[-1]

        self.THE_SECONDARY_START = self.SECONDARY_PATH[0]
        self.THE_SECONDARY_ARRIVE = self.SECONDARY_PATH[-1]

        self.COMPLEX_PATH = self.PRIMARY_PATH + self.SECONDARY_PATH
        print("Create the dungeon 9")


    def find_route(self, b, a):
        start = b
        arrive = a
        current = start
        path_temp = [start]
        cont = 0
        while current != arrive and cont <= 1000:
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

    """DEPRECATED
    def aisles(self, rv):
        #sistem for discover aisles
        self.rv = rv #recive a random number beetween 4 and 24 for number of doors
        rng = random.SystemRandom()
        self.LR_n = rng.randint(1, 2) #select beetween left ora right
        rock_msg_value = self.random_numbers()

        #generate a rock message and a monster
        if rock_msg_value > 0 and rock_msg_value <= 15:
            rocks_msg = self.CONFIG_DICT['aisles_msg_1']
        elif rock_msg_value > 15 and rock_msg_value <= 18:
            rocks_msg = self.CONFIG_DICT['aisles_msg_2']
        else:
            rng = random.SystemRandom()
            rocks_msg = self.CONFIG_DICT['aisles_msg_3'].format(self.monsters_dict[rng.randint(1, 7)])

        #aisles generators with doors
        if self.rv > 1 and self.rv <= 12 and self.FORNITURES_QTY_DICT[11] >= 1:  #one door
            msg_1 = self.CONFIG_DICT['aisles_msg_4'].format(self.position_dict[str(self.LR_n)], rocks_msg)
            new_doors_residue = self.FORNITURES_QTY_DICT[11] - 1
            self.FORNITURES_QTY_DICT[11] = new_doors_residue

            return '{} {}'.format(msg_1, self.CONFIG_DICT['aisles_msg_8'])

        elif self.rv > 12 and self.rv <= 14 and self.FORNITURES_QTY_DICT[11] >= 2: #NO DOORS
            return self.CONFIG_DICT['aisles_msg_7']

        elif self.rv > 14 and self.rv <= 19 or self.FORNITURES_QTY_DICT[11] == 0: #two doors
            rng = random.SystemRandom()
            msg_1 = self.CONFIG_DICT['aisles_msg_5'].format(
                self.position_dict[str(rng.randint(1, 2))],
                self.position_dict[str(rng.randint(1, 2))],
                rocks_msg)
            new_doors_residue = self.FORNITURES_QTY_DICT[11] - 2
            self.FORNITURES_QTY_DICT[11] = new_doors_residue
            return '{} {}'.format(msg_1, self.CONFIG_DICT[
                'aisles_msg_8'])

        elif self.rv > 19 and self.rv <= 24 and self.FORNITURES_QTY_DICT[11] >= 3:  #three door
            rng = random.SystemRandom()
            msg_1 = self.CONFIG_DICT['aisles_msg_6'].format(self.position_dict[str(rng.randint(1, 2))], self.position_dict[str(rng.randint(1, 2))], self.position_dict[str(rng.randint(1, 2))], rocks_msg)
            new_doors_residue = self.FORNITURES_QTY_DICT[11] - 3
            self.FORNITURES_QTY_DICT[11] = new_doors_residue

            return '{} {}'.format(msg_1, self.CONFIG_DICT['aisles_msg_8'])
        """

    def treasures(self, rv):
        self.rv = rv
        if self.rv > 1 and self.rv <= 15:
            return (self.CONFIG_DICT['treasures_msg_1'], 0) #you find nothing. Draw a treasure card.
        elif self.rv > 15 and self.rv <= 22 :
            return (self.CONFIG_DICT['treasures_msg_2'], 1) #you find a random treasure
        elif self.rv > 22:
            return (self.CONFIG_DICT['treasures_msg_3'], 0) #You find a trap!
        else:
            return (self.CONFIG_DICT['treasures_msg_4'], 0) #you find nothing. Draw a treasure card.

    def treasure_random(self, rv, forniture):
        """"create a random treasures inside chest"""
        self.forniture = forniture
        self.rv = rv
        if self.rv > 1 and self.rv <= 13 and (forniture != 'Room' or forniture != 'Stanza'): #add any translation for the word room #a special treasure
            forniture_id_txt = self.CONFIG_DICT['forniture_name_reconversion_dict'][self.forniture]
            treasure_list = self.CONFIG_DICT['treasures_random_type'][forniture_id_txt]
            max_rand_value = len(treasure_list)-1
            rng = random.SystemRandom()
            value_for_selection = rng.randint(0, max_rand_value)
            msg_random_treasure = treasure_list[value_for_selection]
            return msg_random_treasure

        elif self.rv > 13 and self.rv <= 20: #you'll find gold coins
            rng = random.SystemRandom()
            msg = self.CONFIG_DICT['chest_msg_2'].format(rng.randrange(50, 150, 5))
            return msg

        elif self.rv > 20 and self.rv <= 22:  #you'll find a trap!
            return self.CONFIG_DICT['chest_msg_3']

        else:
            rng_1 = random.SystemRandom() #you'll find a weapon
            weapon_rand_num = rng_1.randint(1, 9)
            msg = self.CONFIG_DICT['chest_msg_4'].format(self.CONFIG_DICT['weapons_dict'][weapon_rand_num])

            return msg

    def treasure_card(self, rv):
        """"create a random treasures inside chest"""
        self.rv = rv
        if self.rv >= 19 and self.rv <= 20: #you'll find a healing potion
            treasure_description = self.treasures_card_dict[str(19)]
            return treasure_description
        elif self.rv > 20 and self.rv <= 24: #you'll find a wanderer monster
            treasure_description = self.treasures_card_dict[str(5)]
            return treasure_description
        else:
            rng_1 = random.SystemRandom()
            treasure_description = self.treasures_card_dict[str(rng_1.randint(1, 20))]
            return treasure_description

    def secret_doors(self, rv):
        """Create random doors for aisles"""
        self.rv = rv


        if self.rv >= 1 and self.rv <= 16:
            msg = [self.CONFIG_DICT['secret_doors_msg_1'],''] #no secret doors
        elif self.rv > 16 and self.rv <= 21:
            rng = random.SystemRandom()
            value_LR = rng.randint(1, 3)
            msg = [self.CONFIG_DICT['secret_doors_msg_2'].format(self.position_dict[str(value_LR)]),''] #find a secret doot
        elif self.rv > 21 and self.rv <= 23:
            msg = [self.CONFIG_DICT['secret_doors_msg_3'],''] #find a trapdoor
        elif self.rv > 23 and self.ESCAPE_FOUND == 0:
            self.ESCAPE_FOUND = 1
            msg = [self.CONFIG_DICT['secret_doors_msg_4'], self.SPECIAL_ROOM_CHARGED[1]]
        return msg

    def traps(self, rv):
        """search for traps"""
        self.rv = rv
        if self.rv <= 17:
            return self.CONFIG_DICT['traps_msg_1']
        elif self.rv > 17 and self.rv <= 22:
            return self.CONFIG_DICT['traps_msg_2']
        else:
            return self.CONFIG_DICT['traps_msg_3']

    def fighting_system(self, mc, mg, ms):

        self.monster_category = mc
        self.monster_group = mg
        self.monster_sight = ms

        #COMBAT VALUE FROM DB
        combat_value_dict = self.CONFIG_DICT['combat_value_dict']
        monster_converted = self.CONFIG_DICT['monster_name_reconversion_dict'][self.monster_category]
        combat_value = combat_value_dict[monster_converted]

        #IF GROUPED aggresivity_bonus VALUE RANDOM 1-3 TO ADD
        #RANDO VALUE 4D6
        aggresivity_bonus = 0
        if self.monster_group == 1:
            rng = random.SystemRandom()
            aggresivity_bonus = rng.randint(2, 8)

        if self.monster_sight == 1:
            rng = random.SystemRandom()
            aggresivity_bonus += rng.randint(5, 10)

        aggr_rand_num = self.random_numbers()

        aggression_value = combat_value+aggr_rand_num

        final_aggression_value = aggression_value+aggresivity_bonus

        if final_aggression_value > 30:
            #heroe mode
            return 1
        else:
            #villan mode
            return 2

    def monster_raid(self, c):
        self.choice = c
        msg = ''
        if self.choice == 1:
            msg = self.CONFIG_DICT['raid_message_1'].format(str(self.ROOMS_EXPLORED_LAST_TURN))
        if self.choice == 2:
            msg = self.CONFIG_DICT['raid_message_2'].format(str(self.ROOMS_EXPLORED_LAST_TURN))

        return msg



    def hero_attack(self, rv):
        self.rv = rv
        if self.rv < 23:
            msg = self.CONFIG_DICT['aux_msg_12']
            return str(msg)
        else:
            rng = random.SystemRandom()
            msg_list = self.CONFIG_DICT['attack_messages'][3]
            msg = [rng.randint(0, len(msg_list))]
            return str(msg)


    def random_trap(self, n):
        self.turn = int(n)

        comparison_value = 0
        rn = self.random_numbers()

        if self.turn > 25:
            comparison_value = 16

        elif self.turn > 20:
            comparison_value = 17

        elif self.turn >= 15:
            comparison_value = 19

        elif self.turn >= 1:
            comparison_value = 23

        if rn >= comparison_value:
            rng = random.SystemRandom()
            rand_num = rng.randint(1, 3)
            if rand_num == 1 or rand_num == 2:
                return self.CONFIG_DICT['monsters_msg_4']
            else:
                return self.CONFIG_DICT['aux_msg_8']
        else:
            return self.CONFIG_DICT['aux_msg_11']


    def adventure_start_from(self):
        rng = random.SystemRandom()
        rand_num = rng.randint(1, 2)
        if rand_num == 1:
            start_from = self.START_FROM
            return self.CONFIG_DICT["the_begin_msg_1"].format(start_from)
        else:
            if self.START_FROM.isdigit() is True:
                dungeon_id = '{}{}'.format(self.PRIMARY_PATH[1], self.START_FROM)
            else:
                dungeon_id = '{}{}'.format(self.START_FROM, self.PRIMARY_PATH[1],)

            room_id = self.DUNGEON_TO_ROOM[dungeon_id]
            rng = random.SystemRandom()
            rand_num = rng.randint(0, len(room_id)-1)
            start_from = room_id[rand_num]
            self.ROOMS_EXPLORED.append(start_from)
            return self.CONFIG_DICT["the_begin_msg_2"].format(start_from, dungeon_id)


#TODO FIGTHTING SYSTEM
