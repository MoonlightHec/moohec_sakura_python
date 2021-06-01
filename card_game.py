from collections import Counter
from itertools import combinations


def is_continuous_array(number_list):
    """
    判断数组中的元素是否连续
    :param number_list:
    :return:
    """
    length = len(number_list)
    for i, item in enumerate(number_list):
        if i + 1 < length and int(item) + 1 != int(number_list[i + 1]):
            return False
    return True


def phazed_score(hand):
    default_value = {'A': 1, "0": 10, "J": 11, "Q": 12, "K": 13}
    number_list = []
    for item in hand:
        if item[0] in default_value.keys():
            number_list.append(int(default_value[item[0]]))
        else:
            number_list.append(int(item[0]))
    res = 0
    for it in number_list:
        res += it
    return res


def match_rule1(group):
    """
    匹配规则1
    :param group:
    :return:
    """
    number_list = []
    for item in group:
        number_list.append(item[0])
    number_group_list = Counter(number_list)  # 统计数组的值出现次数
    number_count = len(number_group_list)  # 统计数组的值出现次数
    if number_count == 1 or (number_count == 2 and number_group_list['A'] == 1):
        return True
    return False


def match_rule2(group):
    """
    匹配规则2
    :param group:
    :return:
    """
    number_list = []
    color_list = []
    for item in group:
        number_list.append(item[0])
        color_list.append(item[-1])
    number_group_list = Counter(number_list)  # 统计数组的值出现次数
    color_group_list = Counter(color_list)  # 统计数组花色出现的次数
    color_count = len(color_group_list)  # 统计后数组花色的长度
    not_a_list = []
    # 计算非A的花色数量
    for it in group:
        if it[0] != "A":
            not_a_list.append(it[-1])
    if color_count == 1 or (number_group_list['A'] <= 2 and 1 < color_count <= 3 and len(Counter(not_a_list)) == 1):
        return True
    return False


def match_rule3(group):
    """
    匹配规则3
    :param group:
    :return:
    """
    number_list = []
    for item in group:
        number_list.append(item[0])
    number_list = Counter(number_list)  # 统计数组的值出现次数
    number_count = len(number_list)  # 统计后数组值的长度
    if number_count == 1 or (number_count == 2 and number_list['A'] <= 2):
        return True
    return False


def match_rule4(group):
    """
    匹配规则4
    :param group:
    :return:
    """
    number_list = []
    for item in group:
        number_list.append(item[0])
    number_stat_list = Counter(number_list)
    if number_stat_list['A'] > 2:
        return False
    default_value = {"0": 10, "J": 11, "Q": 12, "K": 13}
    number = []
    for item in number_list:
        if item in default_value.keys():
            number.append(str(default_value[item]))
        else:
            number.append(str(item))
    length = len(number)
    for index, item in enumerate(number):
        if number[index] == 'A' and index + 1 < length:
            if index == 0 and number[index] == 'A':
                number[index] = int(number[index + 1]) - 1
            else:
                number[index] = int(number[index - 1]) + 1
    return is_continuous_array(number)


def match_rule5(group):
    """
    匹配规则5
    :param group:
    :return:
    """
    number_list = []
    color_list = {}
    for item in group:
        number_list.append(item[0])
        if item[0] != "A":
            if item[-1] == 'D' or item[-1] == "H":
                color_list['red'] = 1
            else:
                color_list['black'] = 1
    if match_rule4(number_list):
        return len(color_list) == 1
    return False


def match_rule6(group):
    """
    匹配规则6
    :param group:
    :return:
    """
    return 34 == phazed_score(group)


def match_rule7(group):
    if match_rule6(group):
        color_list = {}
        for item in group:
            if item[-1] == 'D' or item[-1] == "H":
                color_list['red'] = 1
            else:
                color_list['black'] = 1
        return len(color_list) == 1
    return False


def phazed_group_type(group):
    lenght = len(group)
    hit_list = []
    # 匹配规则1
    if lenght == 3:
        if match_rule1(group):
            hit_list.append(1)
    # 匹配规则2
    if lenght == 7:
        if match_rule2(group):
            hit_list.append(2)
    # 匹配规则3
    if lenght == 4:
        if match_rule3(group):
            hit_list.append(3)
    # 匹配规则4
    if lenght == 8:
        if match_rule4(group):
            hit_list.append(4)
    # 匹配规则5
    if lenght == 4:
        if match_rule5(group):
            hit_list.append(5)
    # 匹配规则6
    if match_rule6(group):
        hit_list.append(6)
    # 匹配规则7
    if match_rule7(group):
        hit_list.append(7)
    return hit_list


def phazed_phase_type(phase):
    rule_list = []
    hit_list = []
    for item in phase:
        res = phazed_group_type(item)
        if len(res) > 0:
            for it in res:
                hit_list.append(it)
    hit_list = Counter(hit_list)
    length = len(phase)
    if length == 1:
        if hit_list[2] >= 1:
            rule_list.append(2)
        if hit_list[4] >= 1:
            rule_list.append(5)
    if length == 2:
        if hit_list[1] >= 2:
            rule_list.append(1)
        if hit_list[6] >= 2:
            rule_list.append(3)
        if hit_list[3] >= 2:
            rule_list.append(4)
        if hit_list[5] >= 1 and hit_list[3] >= 1:
            rule_list.append(7)
        if hit_list[7] >= 2:
            rule_list.append(6)
    return rule_list


# part 3
def phazed_is_valid_play(play, player_id, table, phase_status, turn_history, hand, discard):
    output = False
    if play[0] == 1:
        output = valid_rule1()
    elif play[0] == 2:
        output = valid_rule2(play=play, discard=discard)
    elif play[0] == 3:
        output = valid_rule3(play=play)
    elif play[0] == 4:
        output = valid_rule4(play, player_id, table, phase_status, hand)
    elif play[0] == 5:
        output = valid_rule5(play, player_id, table, phase_status, hand)
    return output


# paly1 牌组顶部抽牌
def valid_rule1():
    return True


# play2 弃牌堆抽牌
def valid_rule2(play, discard):
    if discard:
        return play[1] == discard


# play3 打出phase
def valid_rule3(play):
    # 得到将要打出的牌符合的phase
    goal_list = phazed_phase_type(play[1][1])
    return play[1][0] in goal_list


# play4 打出一张牌
def valid_rule4(play, player_id, table, phase_status, hand):
    # 获取玩家出牌信息
    player_card = play[1][0]
    player_group = play[1][1][1]
    player_index = play[1][1][2]
    if player_card in hand:
        # 判断是否与试图打到的组别类型一致
        player_put = table[player_id][1]
        player_put[player_group].insert(player_index, player_card)
        goal_list = phazed_phase_type(player_put)
        if phase_status[player_id] in goal_list:
            return True
    return False


# play5 弃牌
def valid_rule5(play, player_id, table, phase_status, hand):
    drop_card = play[1]
    # 必须是玩家持有的牌
    if drop_card in hand:
        # 该回合所玩的是“累计”玩法
        if phase_status[player_id] in [3, 6]:
            last_puts = table[player_id][1]
            # 该回合出的牌
            congest_list = []
            for put in last_puts:
                congest_list += put
            congest_num = phazed_score(congest_list)
            if congest_num not in [34, 55, 68]:
                return False
    return True


# part 5

def phazed_play(player_id, table, turn_history, phase_status, hand, discard):
    # 获取当前玩家已经执行的步骤
    player_history = turn_history[player_id][1]
    player_done_last = player_history[-1][0]
    player_status = phase_status[player_id]
    # 如果玩家已经抽牌，判断手牌是否有符合的phase
    # 对手牌排列组合，去对比phase规则
    if player_done_last == 1:
        for i in range(1, len(hand) + 1):
            hand_lists = list(combinations(hand, i))
            for hand_list in hand_lists:
                if player_status in phazed_phase_type(hand_list):
                    # 要打出的牌
                    player_phazed = (3, hand_list)
                    return player_phazed
                else:
                # 现有牌的价值
                price_card = phazed_score(table[player_id][1] + hand_list)
                if price_card in (34, 55):
                    player_phazed = (3, hand_list[0])
                    return
            pass


def part1():
    print(phazed_group_type(['2C', '2S', '2H']))
    print(phazed_group_type(['2C', '2C', '4C', 'KC', '9C', 'AH', 'JC']))
    print(phazed_group_type(['4H', '4S', 'AC', '4C']))
    print(phazed_group_type(['4H', '5S', 'AC', '7C', '8H', 'AH', '0S', 'JC']))
    print(phazed_group_type(['4H', '5D', 'AC', '7H']))
    print(phazed_group_type(['KS', '0D', '8C', '3S']))
    print(phazed_group_type(['KS', '0C', '8C', '3S']))
    print(phazed_group_type(['2C', '2C', '4C', 'KC', '9C', 'AS', '3C']))
    print(phazed_group_type(['4H', '5D', '7C', 'AC']))


def part2():
    print(phazed_phase_type([['2C', '2S', '2H'], ['7H', '7C', 'AH']]))
    print(phazed_phase_type([['2C', '2C', '4C', 'KC', '9C', 'AH', 'JC']]))
    print(phazed_phase_type([['2C', 'KH', 'QS', '7H'],
                             ['3H', '7S', '0D', 'KD', 'AD']]))
    print(phazed_phase_type([['4H', '4S', 'AC', '4C'],
                             ['7H', '7C', 'AH', 'AC']]))
    print(phazed_phase_type([['4H', '5S', 'AC', '7C',
                              '8H', 'AH', '0S', 'JC']]))
    print(phazed_phase_type([['2C', 'KC', 'QS', '7C'],
                             ['3H', '7H', '0D', 'KD', 'AD']]))
    print(phazed_phase_type([['4H', '5D', 'AC', '7H'],
                             ['7H', '7C', 'AH', 'AS']]))


def part3():
    print(phazed_is_valid_play(play=(3, (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']])), player_id=0, table=[(None, []), (None, []), (None, []), (None, [])],
                               turn_history=[(0, [(2, 'JS')])], phase_status=[0, 0, 0, 0],
                               hand=['AS', '2S', '2S', '2C', '5S', '5S', '7S', '8S', '9S', '0S', 'JS'], discard=None))
    print(phazed_is_valid_play(play=(4, ('KC', (1, 0, 0))), player_id=1, table=[(None, []), (2, [['2S', '2S', 'AS', '5S', '5S', '7S', 'JS']]), (None, []), (None, [])],
                               turn_history=[(0, [(2, 'JS'), (5, 'JS')]), (1, [(1, 'XX'), (3, (2, [['2S', '2S', 'AS', '5S', '5S', '7S', 'JS']]))])], phase_status=[0, 2, 0, 0],
                               hand=['5D', '0S', 'JS', 'KC'],
                               discard='JS'))
    print(phazed_is_valid_play(play=(5, 'JS'), player_id=1, table=[(None, []), (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']]), (None, []), (None, [])],
                               turn_history=[(0, [(2, 'JS'), (5, 'JS')]), (1, [(1, 'XX'), (3, (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']]))])], phase_status=[0, 1, 0, 0],
                               hand=['AD', '8S', '9S', '0S', 'JS'],
                               discard='JS'))


def part4():
    print(phazed_score(['KS', '0D', '8C', '3S']))


def part5():
    print(phazed_play(player_id=1, table=[(None, []), (5, [['2C', '3H', '4D', 'AD', '6S', '7C', '8S', '9H', '0S', 'JS']]), (None, []), (None, [])],
                      turn_history=[
                          (0, [(2, 'JS'), (5, 'JS')]),
                          (1, [
                              (2, 'JS'),
                              (3, (5, [['2C', '3H', '4D', 'AD', '6S', '7C', '8S', '9H']])),
                              (4, ('0S', (1, 0, 8))),
                              (4, ('JS', (1, 0, 9)))
                          ])],
                      phase_status=[0, 5, 0, 0], hand=['5D'], discard=None))


if __name__ == '__main__':
    # print('part1')
    # part1()
    # print('\npart2')
    # part2()
    # print('\npart3')
    part3()
    # print('\npart4')
    # part4()
    # part5()
