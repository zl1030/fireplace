from utils import *


def test_metamorphosis():
	game = prepare_game()
	old_power = game.player1.hero.power
	metamorphosis = game.player1.give("BT_429")
	metamorphosis.play()
	game.player1.hero.power.use(target=game.player2.hero)
	game.end_turn()
	game.end_turn()
	game.player1.hero.power.use(target=game.player2.hero)
	assert game.player1.hero.power.id == old_power.id


def test_kayn_sunfury():
	game = prepare_game()
	footman = game.player1.give(GOLDSHIRE_FOOTMAN)
	wisp = game.player1.give(WISP)
	footman.play()
	wisp.play()
	game.end_turn()
	boar = game.player2.give("CS2_171")
	boar.play()
	assert boar.targets == [footman]
	kayn = game.player2.give("BT_187")
	kayn.play()
	assert boar.targets == [game.player1.hero, footman, wisp]
	game.player2.give("CS2_029").play(target=kayn)
	assert boar.targets == [footman]


def test_skull_of_guldan():
	game = prepare_empty_game()
	game.player1.give(WISP)
	skull = game.player1.give("BT_601")
	game.player1.give(WISP)
	pyroblasts = [game.player1.give(PYROBLAST) for i in range(3)]
	for card in pyroblasts:
		card.shuffle_into_deck()
	skull.play()
	for card in pyroblasts:
		assert card.cost == 10


def test_skull_of_guldan_outcast():
	game = prepare_empty_game()
	game.player1.give(WISP)
	skull = game.player1.give("BT_601")
	pyroblasts = [game.player1.give(PYROBLAST) for i in range(3)]
	for card in pyroblasts:
		card.shuffle_into_deck()
	skull.play()
	for card in pyroblasts:
		assert card.cost == 7


def test_imprisoned_antaen():
	game = prepare_game()
	antaen = game.player1.give("BT_934")
	antaen.play()
	assert antaen.dormant == 2
	game.end_turn()

	deathwing = game.player2.give("NEW1_030")
	deathwing.play()
	assert game.player1.field[0] == antaen
	game.end_turn()

	assert antaen.dormant == 1
	assert not antaen.can_attack()
	game.end_turn()

	assert not deathwing.can_attack(antaen)
	moonfire = game.player2.give(MOONFIRE)
	assert antaen not in moonfire.play_targets
	game.end_turn()

	assert not antaen.dormant
	assert antaen.can_attack()
	assert deathwing.health + game.player2.hero.health == 30 + 12 - 10
	deathwing2 = game.player1.give("NEW1_030")
	deathwing2.play()
	assert game.player1.field == [deathwing2]
