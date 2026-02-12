import numpy as np
import math
import random

num_yellow_gifts = 35
num_purple_gifts = 13
total_gifts = num_yellow_gifts + num_purple_gifts

v_zero = np.zeros(total_gifts)
v_yellow_one_hot = np.array([1] * num_yellow_gifts + [0] * num_purple_gifts)
v_purple_one_hot = np.array([0] * num_yellow_gifts + [1] * num_purple_gifts)
v_one_hot = np.ones(total_gifts)

v_yellow = v_yellow_one_hot/num_yellow_gifts
v_purple = v_purple_one_hot/num_purple_gifts
v = v_one_hot/total_gifts

n1_map = {1: 9.32, 2: 9.63, 3: 15.88, 4: 1.80, 5: 22.96, 6: 9.73, 7: 7.10, 8: 5.34,
              9: 0.40, 10: 0.40, 11: 9.88, 12: 3.79, 13: 0.18, 14: 0.18, 15: 0.18, 16: 0.18,
              17: 0.18, 18: 0.18, 19: 0.18, 20: 0.18, 21: 0.18, 22: 0.18, 23: 0.18, 24: 0.18,
              25: 0.18, 26: 0.18, 27: 0.18, 28: 0.18, 29: 0.18, 30: 0.18, 31: 0.18, 32: 0.18,
              33: 0.18}

n2_map = {1: 13.86, 2: 13.13, 3: 1.87, 4: 13.25, 5: 5.71, 6: 3.80, 7: 3.30, 8: 0.22,
              9: 0.22, 10: 5.73, 11: 9.88, 12: 0.47, 13: 0.47, 14: 0.47, 15: 0.47, 16: 0.47,
              17: 0.47, 18: 0.47, 19: 0.47, 20: 0.47, 21: 0.47, 22: 0.47, 23: 0.47, 24: 0.47,
              25: 0.47, 26: 0.47, 27: 0.47, 28: 0.47, 29: 0.47, 30: 0.47, 31: 0.47, 32: 0.47,
              33: 1.25, 34: 0.50, 35: 0.19, 36: 1.02, 37: 0.28, 38: 3.03, 39: 1.21, 40: 2.06,
              41: 0.15, 42: 0.13, 43: 0.05, 44: 0.41, 45: 0.41, 46: 0.41, 47: 0.41, 48: 0.41,
              49: 0.41, 50: 0.41, 51: 0.41, 52: 0.41, 53: 0.41, 54: 0.41, 55: 0.41, 56: 0.41,
              57: 0.41, 58: 0.32, 59: 0.32, 60: 0.32, 61: 0.32, 62: 0.32, 63: 0.32, 64: 0.32,
              65: 0.32, 66: 0.32, 67: 0.32, 68: 0.32}

n3_map = {1: 36.19, 2: 9.98, 3: 9.05, 4: 6.03, 5: 5.34, 6: 1.39, 7: 1.86, 8: 9.28,
              9: 12.53, 10: 0.70, 11: 0.23, 12: 0.23, 13: 0.65, 14: 0.65, 15: 0.65, 16: 0.65,
              17: 0.65, 18: 0.65, 19: 0.65, 20: 0.65, 21: 0.65, 22: 0.65, 23: 0.65}

# gift indices for node 2's specialized flower nodes
n2_flower_index = {44: [1, 15], 45: [2, 17], 46: [3, 12], 47: [4, 5, 10, 16, 33, 24], 48: [6, 7, 8],
49: [9, 13, 14, 27], 50: [11, 19, 21, 23, 26], 51: [18, 20, 30, 31], 52: [22, 28],
53: [25], 54: [29], 55: [32], 56: [34],
57: [35]}

# REMEMBER TO -1 n2_flower_index ELTS! SINCE ITS 1's indexing!

# v sorted from best to worst options
n1_prio = [11, 3]
# for node_1 nodes with gift values
n1_vec_map = {11: v_yellow, 3: 0.6224 * v_yellow}
# v watch out for middle node 2 prio, that can be custom sorted based on input params
n2_prio = [10] + list(range(44, 58)) + [2]
n2_vec_map = {10: v_yellow, 2: 0.4363 * v_yellow}

for i in range(44, 58):
  flower_i_one_hot_vec = v_zero.copy()
  for idx in n2_flower_index[i]:
    flower_i_one_hot_vec[idx-1] = 1
  n2_vec_map[i] = flower_i_one_hot_vec/np.sum(flower_i_one_hot_vec)

n3_prio = [8, 2, 1]
n3_vec_map = {8: 0.75 * 2.5 * v_yellow + 0.25 * 1.5 * v_purple,
              2: 0.2326 * 1.5 * v_purple,
              1: 0.1923 * 2.5 * v_yellow}
cuml_arr = []
for item in n2_flower_index.values():
  cuml_arr += item
cuml_arr.sort()
#print(cuml_arr) # should be 1, 2, ..., 35

node_i_map_dict = {0: n1_map, 1: n2_map, 2: n3_map}
node_i_prio_dict = {0: n1_prio, 1: n2_prio, 2: n3_prio}
node_i_vec_map_dict = {0: n1_vec_map, 1: n2_vec_map, 2: n3_vec_map}


def compute_craft_exp(student_gift_exp_vec):
  expected_gifts = np.zeros(total_gifts)
  for node_i in range(3):
    node_i_map = node_i_map_dict[node_i].copy()
    node_i_prio_arr = node_i_prio_dict[node_i]
    node_i_vec_map = node_i_vec_map_dict[node_i]
    subnode_array = [] # there will be 5 subnode indices here
    for subnode_attempt in range(5):
      obtained_subnode = random.choices(list(node_i_map.keys()),
                          weights=list(node_i_map.values()), k=1)[0]
      # ^ this will be 1-indexed subnode index
      del node_i_map[obtained_subnode]
      subnode_array.append(obtained_subnode)

    rolled_subnode_five = set(subnode_array)

    if not rolled_subnode_five.intersection(set(node_i_prio_arr)):
      # then we have gotten zero subnodes containing gifts
      #print("node " +str(node_i+1)+ " exp: " + str(0))
      continue

    for gift_node in node_i_prio_arr:
      # ^ traverses from best to worst gift nodes
      if gift_node in rolled_subnode_five:
        expected_gifts += node_i_vec_map[gift_node]
        #print("node " +str(node_i+1)+ " exp: " + str(node_i_vec_map[gift_node] @ student_gift_exp_vec))
        break
  return expected_gifts @ student_gift_exp_vec


def get_sorted_n2_vec(student_gift_exp_vec):
  def n2_gift_nodes_exp_count(gift_node):
    return n2_vec_map[gift_node] @ student_gift_exp_vec
  return sorted(n2_prio, key=n2_gift_nodes_exp_count, reverse=True)

def compute_average_craft_exp(student_gift_pref, number_of_trials):
  student_gift_exp_vec = convert_gift_pref_to_exp_vec(student_gift_pref)
  # anti pattern. Okay
  n2_prio_sorted = get_sorted_n2_vec(student_gift_exp_vec)
  node_i_prio_dict[1] = n2_prio_sorted
  #print(n2_prio_sorted)
  total_exp = 0
  for trial in range(number_of_trials):
    total_exp += compute_craft_exp(student_gift_exp_vec)
  avg_exp = total_exp/number_of_trials
  return math.floor(avg_exp * 100)/100.0

def convert_gift_pref_to_exp_vec(student_gift_pref):
  # gift pref is dictionary of {{gift_id (1's idx), value [1, 3]},...}
  exp_vec = v_yellow_one_hot * 20 + v_purple_one_hot * 120 # baseline exp vec
  yellow_pref_conversion = {1: 20, 2: 40, 3: 60}
  purple_pref_conversion = {1: 0, 2: 60, 3: 120}
  for g in student_gift_pref:
    gift_idx = g.gift_id # 1 indexed so watch out
    pref = g.value
    if gift_idx <= num_yellow_gifts:
      exp_vec[gift_idx-1] += yellow_pref_conversion[pref]
    else:
      exp_vec[gift_idx-1] += purple_pref_conversion[pref]
  return exp_vec


def best_yellow_gift_exp(student_gift_pref):
  best_yellow_exp = 20
  for g in student_gift_pref:
    yellow_pref_conversion = {1: 40, 2: 60, 3: 80}
    if g.gift_id <= num_yellow_gifts:
      best_yellow_exp = max(yellow_pref_conversion[g.value], best_yellow_exp)
  return best_yellow_exp

# Return dictionary with all relevant bond exp components per month
# Also return dict has total exp per month
def compute_bond_exp_per_month_comp(student_gift_pref, num_daily_headpats=4,
    crafting_monthlies=False, gift_monthlies=False,
    num_red_bouquet_packs_per_year=0, eligma_mini_keystones=True,
    frr_tryhard = False, extra_exp_per_month=0, number_trials=5000):
  # ^ frr tryhard means f99+ every month, not means f75 every month
  # actually for frr tryhard stat, pick value between [0, 1=true, 2] to choose your tryhard level

  component_exp = dict()

  keystone_per_week = 17
  keystone_per_day = keystone_per_week/7
  average_num_days_per_month = 30.44
  num_yellow_keystones_per_month = 70
  average_daily_lessons_exp = 30 # this is a complete guess, I need to measure the actual stats
  favorite_yellow_gift_exp = best_yellow_gift_exp(student_gift_pref)
  student_exp_vec = convert_gift_pref_to_exp_vec(student_gift_pref)
  avg_yellow_gift_exp = v_yellow @ student_exp_vec
  avg_purple_gift_exp = v_purple @ student_exp_vec
  total_assault_gift_exp = 2 * favorite_yellow_gift_exp # assuming maxed out TA rewards
  grand_assault_gift_exp = 3 * favorite_yellow_gift_exp + avg_purple_gift_exp # maxed GA
  average_crafting_exp = compute_average_craft_exp(student_gift_pref, number_trials)
  bonus_exp_due_to_yellow_gift_minus_two_yellow = max(favorite_yellow_gift_exp - 40, 0)

  monthly_yellow_gifts_from_event_shop = 81.8
  monthly_purple_gifts_from_event_shop = 4.6
  """
  these above values were calculated by tallying up total number of gifts from
  march 26 2025 (start of jp shupo event) to nov 19 2025 (end of jp kisaki rerun event)
  which tallied a total of 64 * 10 yellow gifts and 36 purple gifts from event shops
  """

  component_exp["Headpats"] = num_daily_headpats * 15 * average_num_days_per_month
  component_exp["F2P Crafting"] = (keystone_per_day * average_num_days_per_month * average_crafting_exp 
                       + 10 * average_crafting_exp * eligma_mini_keystones)
  component_exp["Lessons"] = average_daily_lessons_exp * average_num_days_per_month
  component_exp["Event Shop Gifts"] = (monthly_yellow_gifts_from_event_shop * avg_yellow_gift_exp
                        + monthly_purple_gifts_from_event_shop * avg_purple_gift_exp)
  component_exp["GA/TA Gifts"] = total_assault_gift_exp + grand_assault_gift_exp
  component_exp["FRR Gifts"] = (4 * favorite_yellow_gift_exp + avg_purple_gift_exp
                        + frr_tryhard * (2 * favorite_yellow_gift_exp +
                          2 * avg_purple_gift_exp))
  
  if (bonus_exp_due_to_yellow_gift_minus_two_yellow > 0):
    component_exp["Extra EXP From F2P Yellow Giftbox Crafting"] = (bonus_exp_due_to_yellow_gift_minus_two_yellow 
                       * num_yellow_keystones_per_month)
  if (num_red_bouquet_packs_per_year > 0):
    component_exp["Red Bouquet Packs"] = 1500 * num_red_bouquet_packs_per_year / 12
  if (crafting_monthlies):
    component_exp["Crafting Monthly Pack"] = (10 * average_crafting_exp + 15 * favorite_yellow_gift_exp)
  if (gift_monthlies):
    component_exp["Gift Monthly Pack"] = (5 * favorite_yellow_gift_exp +
                          10 * avg_yellow_gift_exp + avg_purple_gift_exp)
  if (extra_exp_per_month > 0):
    component_exp["Misc EXP Per Month"] = extra_exp_per_month


  total_monthly_exp = 0
  for k, v in component_exp.items():
    total_monthly_exp += v

  component_exp["Total EXP"] = total_monthly_exp

  return component_exp


def expected_num_months_to_complete_bond_100(bond_exp_per_month_value, current_bond_exp=0):
  exp_left = 240000 - current_bond_exp
  return math.floor(exp_left/bond_exp_per_month_value * 1000) / 1000.0

def zipper(map):
  # Convert kv map to [[k, v], ...] type array
  zipper_arr = []
  for k, v in map.items():
    zipper_arr.append([k, v])
  return zipper_arr