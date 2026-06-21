# 组员C负责模块：交互系统与状态管理

# 宠物当前状态值（0-100）
PET_STATUS = {
    "hunger": 80,   # 饱食度
    "mood":   80,   # 心情
    "energy": 80,   # 体力
}

# 交互动作配置列表
INTERACTIONS = [
    {"action": "feed", "effect": "饱食度+20", "desc": "喂食，让宠物吃饱"},
    {"action": "play", "effect": "心情+20",   "desc": "玩耍，提升宠物心情"},
    {"action": "rest", "effect": "体力+20",   "desc": "休息，恢复宠物体力"},
]
