class Arc:
    def __init__(self, ctd_place, weight):
        self.ctd_place = ctd_place
        self.weight = weight


class Place:
    def __init__(self, name, nt):
        self.name = name
        self.no_tokens = nt


class Transition:
    no_tokens = 0
    in_adj = []
    out_adj = []

    def __init__(self, iadj, oadj):
        self.in_adj = iadj
        self.out_adj = oadj


class PetriNet:
    place_list = []
    trans_list = []

    def __init__(self, pl, tl):
        self.place_list = pl
        self.trans_list = tl

    def is_enabled(self, trans_id):
        trans = self.trans_list[trans_id]

        enabled = True

        for arc in trans.in_adj:
            if self.place_list[arc.ctd_place].no_tokens < arc.weight:
                enabled = False

        return enabled

    def fire_trans(self, trans_id):
        trans = self.trans_list[trans_id]

        if not self.is_enabled(trans_id):
            print("Specified transition is not enabled!")
            return
        else:
            print("Fired transition " + str(trans_id) + ".\n")

        for arc in trans.in_adj:
            trans.no_tokens += arc.weight
            self.place_list[arc.ctd_place].no_tokens -= arc.weight

        for arc in trans.out_adj:
            self.place_list[arc.ctd_place].no_tokens += min(trans.no_tokens, arc.weight)
            trans.no_tokens -= min(trans.no_tokens, arc.weight)

        trans.no_tokens = 0

    def output_state(self):
        it = 0
        for place in self.place_list:
            print("Tokens in " + place.name + ": " + str(place.no_tokens))
            it += 1
        print("\n")


def create_net_from_file(file):
    place_list = []
    trans_list = []

    no_elem = file.readline().strip().split(" ")
    names = file.readline().strip().split(" ")
    no_tokens = file.readline().strip().split(" ")

    for place_it in range(0, int(no_elem[0])):
        temp_place = Place(names[place_it], int(no_tokens[place_it]))

        place_list.append(temp_place)

    for trans_it in range(0, int(no_elem[1])):
        trans_adj = file.readline().split(" ")

        arc_list_in = []
        arc_list_out = []

        for trans_in_it in range(0, int(trans_adj[0])):
            ctd_place, weight = file.readline().split(" ")

            ctd_place_id = 0
            for place in place_list:
                if place.name == ctd_place:
                    break
                ctd_place_id += 1

            temp_arc = Arc(ctd_place_id, int(weight))
            arc_list_in.append(temp_arc)

        for trans_in_it in range(0, int(trans_adj[1])):
            ctd_place, weight = file.readline().split(" ")

            ctd_place_id = 0
            for place in place_list:
                if place.name == ctd_place:
                    break
                ctd_place_id += 1

            temp_arc = Arc(ctd_place_id, int(weight))
            arc_list_out.append(temp_arc)

        temp_trans = Transition(arc_list_in, arc_list_out)
        trans_list.append(temp_trans)

    ret_net = PetriNet(place_list, trans_list)
    file.close()
    return ret_net


def generate_net_file(file):
    no_places = input("Number of places in the net: ")
    no_trans = input("Number of transitions in the net: ")
    file.write(str(no_places) + " " + str(no_trans) + "\n")

    name_list = []
    token_list = []

    for place in range(0, int(no_places)):
        name = input("Name of the place: ")
        name_list.append(name)
        no_tokens = input("Number of tokens in place " + name + ": ")
        token_list.append(no_tokens)

    for name in name_list:
        file.write(name + " ")
    file.write("\n")

    for tokens in token_list:
        file.write(tokens + " ")
    file.write("\n")

    for trans in range(0, int(no_trans)):
        no_inputs = input("Number of arcs going into transition " + str(trans) + ": ")
        no_outputs = input("Number of arcs going out of transition " + str(trans) + ": ")
        file.write(no_inputs + " " + no_outputs + "\n")

        for arc in range(0, int(no_inputs)):
            arc_ctd_place = input("Place where arc " + str(arc) + " is coming from: ")
            arc_weight = input("Weight of arc " + str(arc) + ": ")
            file.write(arc_ctd_place + " " + arc_weight + "\n")

        for arc in range(0, int(no_outputs)):
            arc_ctd_place = input("Place where arc " + str(arc) + " is going to: ")
            arc_weight = input("Weight of arc " + str(arc) + ": ")
            file.write(arc_ctd_place + " " + arc_weight + "\n")
    print("\n")

    file.close()
