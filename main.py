import petrinet as pn

PN = pn.create_net_from_file(open("init_state.pn", "r"))
PN.output_state()
PN.fire_trans(1)
PN.output_state()
PN.fire_trans(2)
PN.output_state()

# pn.generate_net_file(open("new_state.pn", "w"))
# PN = pn.create_net_from_file(open("new_state.pn", "r"))
# PN.output_state()
# PN.fire_trans(0)
# PN.output_state()
