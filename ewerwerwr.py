from itertools import product

# Категории и их элементы с баллами
categories = {
    "Background": [("Edge Runners", 90), ("Devastators", 90), ("Corrupts", 88), ("Sentinels", 88), ("Villagers", 85)],
    "Shoes": [("Black Shoes", 110), ("Barefoot", 110), ("Brown Shoes", 110), ("White Shoes", 108),
              ("White Sneakers", 108), ("Blue Convi", 108), ("Green Sneakers", 108), ("Yellow Convi", 108),
              ("Pink Sneakers", 108), ("Blue Sneakers", 108), ("Yellow Sneakers", 108), ("Green Convi", 108),
              ("Red Convi", 107), ("Black Convi", 107), ("Red Sneakers", 107)],
    "Mouth": [("Gold Teeth", 113), ("Orc", 111), ("Vampyre", 111), ("Dumb", 111), ("Effort", 110),
              ("Mischievous", 110), ("Doubtful", 109), ("Rascal", 109), ("Malign", 109), ("Surprise", 107),
              ("Serious", 105), ("Angry", 105), ("Dubious", 105), ("Happy", 105), ("Neutral", 105)],
    "Eyes": [("Scar Red", 134), ("Scar Blue", 134), ("Martian", 134), ("Cyclop", 134), ("Lizzard", 134),
             ("X", 134), ("Neutral Black", 133), ("Neutral Brown", 133), ("Monster", 133), ("Cry", 133),
             ("Perceptive Blue", 132), ("Fearful Blue", 132), ("Happy", 132), ("Annoyed Black", 132),
             ("Very Angry Green", 132), ("Fearful Green", 132), ("Angry Red", 132), ("Perceptive Red", 132),
             ("Perceptive Brown", 132), ("Angry Green", 132), ("Perceptive Green", 132), ("Very Angry Red", 132),
             ("Angry Brown", 132), ("Very Angry Blue", 132), ("Annoyed Brown", 132), ("Drunk Green", 132),
             ("Drunk Brown", 132), ("Annoyed Blue", 132), ("Blind", 132), ("Annoyed Green", 132),
             ("Drunk Black", 132), ("Fearful Brown", 132), ("Angry Blue", 131), ("Neutral Blue", 130),
             ("Neutral Green", 130)],
    "Clothes": [("Bone Necklace", 126), ("Ninja Mask", 126), ("Red Ammunition Belt", 126), ("Red Rags", 126),
                ("Beige Ammunition Belt", 126), ("White Rags", 126), ("Blue Rags", 126), ("Toxic Lab Suit", 126),
                ("Naked", 125), ("Open Sports Sg", 125), ("Closed Sports Sg", 125), ("Green Hoodie", 124),
                ("Raven Scarf", 124), ("Gryff Scarf", 124), ("Slyth Scarf", 124), ("Huff Scarf", 124),
                ("Orange Hoodie", 124), ("Red Scarf", 124), ("Gray Scarf", 124), ("White Scarf", 124),
                ("Black Scarf", 124), ("Blue Coat", 123), ("Red Cloth", 123), ("Beige Hoodie", 123),
                ("Violet Hoodie", 123), ("Red Coat", 123), ("Black Coat", 122), ("Black Hoodie", 122)],
    "Accessories": [("Pixel Glasses", 115), ("Cyber Glasses", 112), ("Toxic Mask", 112), ("Green Tracker", 112),
                    ("Red Tracker", 112), ("Pirate Patch", 112), ("Grid Glasses", 112), ("Lenses", 112),
                    ("Monocle", 112), ("Snorkel", 112), ("Scientist", 112), ("Gas Mask", 112), ("Blue Tracker", 112),
                    ("Golden Glasses", 111), ("Sport Glasses", 111), ("Rainbow Glasses", 111), ("Nothing", 107)],
    "Hat": [("Pepe", 150), ("Loki Helmet", 150), ("Farm Hat", 150), ("Ronin Hat", 150), ("White Cap", 150),
            ("Samurai Helmet", 150), ("Gold Crown", 150), ("Doge", 150), ("Flowers", 150), ("Moku Cap", 150),
            ("Hat", 149), ("Tiki Hat", 149), ("Green Mohican", 149), ("Ratz", 149), ("Pirate Hat", 149),
            ("Luu Cap", 149), ("Graduation", 149), ("Cowboy Hat", 149), ("Black Bonnet", 149), ("Banana", 149),
            ("Soldier Helmet", 149), ("Red Bonnet", 149), ("Red Mohican", 149), ("White Bonnet", 149), ("Cat", 149),
            ("Poke Cap", 149), ("Beret", 149), ("Bald", 149), ("Paddle Beret", 149), ("Chef Hat", 149), ("Rasta", 149),
            ("Witch", 149), ("Pilot Cap", 149), ("Police Cap", 149), ("Lumi Cap", 149), ("Miner Yellow", 149),
            ("Ice Cream", 149), ("Miner Blue", 149), ("Christmas Hat", 149), ("Red Bandana", 149), ("Sg Cap", 149),
            ("Back Black Cap", 149), ("Red Cap", 148), ("Green Cap", 148), ("Black Cap", 148), ("Back Red Cap", 148),
            ("Back Green Cap", 148), ("Blue Cap", 148), ("Violet Mohican", 148), ("Back Blue Cap", 148)],
    "Right Hand": [("Glitchstar", 125), ("Btc", 125), ("Heart Balloon", 125), ("Pixel Diamond", 125),
                   ("Tribally Balloon", 125), ("Rose", 124), ("W-3", 123), ("R2-025", 123), ("T-k2", 123),
                   ("Uy-01", 123), ("M33-12", 123), ("Gg-04", 123), ("Closed", 122), ("I Catch You", 122),
                   ("Electric", 122), ("Ready", 121), ("Ice", 121), ("Acid", 121), ("Poison", 121),
                   ("Blue Fire", 121), ("Blue Bat Cyclops", 120), ("Bat", 120), ("Red Bat Cyclops", 120),
                   ("Black Bat Cyclops", 120), ("Dark Fire", 119), ("Fire", 119)]
}

# Целевая сумма баллов
target_score = 947

# Поиск всех комбинаций, сумма баллов которых равна target_score
valid_combinations = []

for combination in product(*categories.values()):
    total_score = sum(item[1] for item in combination)
    if total_score == target_score:
        valid_combinations.append([item[0] for item in combination])

# Выведем первые 5 найденных комбинаций (если есть)
valid_combinations[:5]
