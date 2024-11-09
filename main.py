from dataclasses import dataclass
from typing import List

VARIANT = 0  # Ничего - 0, Астма - 1, Заражение - 2, Всё - 3

# Размер рюкзака
REAL_STORAGE_SIZE = 9
# Длинна строки при выводе
STORAGE_LINE_SIZE = 3


@dataclass
class Item:
    name: str
    sign: str
    size: int
    cost: int


inhaler = Item("inhaler", "i", 1,  5)
antidot = Item("antidot", "d", 1, 10)

items = [
    Item("rifle",    "r", 3, 25),
    Item("talisman", "t", 1, 25),
    Item("medkit",   "m", 2, 20),
    Item("axe",      "x", 3, 20),
    Item("supplies", "s", 2, 20),
    Item("crossbow", "c", 2, 20),
    Item("pistol",   "p", 2, 15),
    Item("ammo",     "a", 2, 15),
    Item("flask",    "f", 1, 15),
    Item("knife",    "k", 1, 15)
]

needs = []

if VARIANT & 1:
    needs.append(inhaler)
else:
    items.append(inhaler)

if VARIANT & 2:
    needs.append(antidot)
else:
    items.append(antidot)

STORAGE_SIZE = REAL_STORAGE_SIZE - sum([i.size for i in needs])


def make_backpack_table():
    dp = [[0] * (STORAGE_SIZE + 1) for _ in range(len(items) + 1)]
    for i, item in enumerate(items, 1):
        for a in range(1, STORAGE_SIZE + 1):
            if item.size <= a:
                dp[i][a] = max(item.cost + dp[i - 1][a - item.size], dp[i - 1][a])
            else:
                dp[i][a] = dp[i - 1][a]

    return dp


def get_items_in_backpack(dp: List[List[int]]):
    current = dp[len(items)][STORAGE_SIZE]
    a = STORAGE_SIZE
    ans = []

    for i in range(len(items), 0, -1):
        if current <= 0:
            break
        if current == dp[i - 1][a]:
            continue
        else:
            item = items[i - 1]
            ans.append(item)
            current -= item.cost
            a -= item.size

    return ans + needs


if __name__ == '__main__':
    backpack = get_items_in_backpack(make_backpack_table())
    sign_list = [elem.sign for elem in backpack for _ in range(elem.size)]

    for idx in range(0, len(sign_list), STORAGE_LINE_SIZE):
        print(",".join(
            f"[{sign}]" for sign in sign_list[idx:idx + STORAGE_LINE_SIZE]
        ))
    print()

    print("Итоговые очки выживания:", sum(elem.cost for elem in backpack))
