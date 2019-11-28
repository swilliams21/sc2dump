import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import *
import random


class MarineReaperBotEasy(sc2.BotAI):


    async def on_step(self, iteration):
        """worker1 = self.units.worker().random"""

        await self.distribute_workers()
        await self.trainreaper()
        await self.trainmarine()
        await self.buildscv()
        await self.checksupply()
        await self.buildbarracks()
        await self.buildrefinery()
        await self.expand()
        await self.reaperscout()
        await self.flood()
        await self.reapernotdie()

    async def buildscv(self):
        for cc in self.units(COMMANDCENTER).ready.noqueue:
            if self.can_afford(SCV) and self.units(SCV).amount < (self.units(COMMANDCENTER).amount * 14) +10:
                await self.do(cc.train(SCV))

    async def checksupply(self):
        if self.supply_left < 2 + (self.supply_used/10) and not self.already_pending(SUPPLYDEPOT):
            cc = self.units(COMMANDCENTER).ready
            if cc.exists:
                if self.can_afford(SUPPLYDEPOT):
                    if self.units(SUPPLYDEPOT).amount > 0:
                        sd = self.units(SUPPLYDEPOT)
                        await self.build(SUPPLYDEPOT, near=sd.first)
                    else:
                        if self.units(SCV).amount>0:
                            s = self.units(SCV).random
                            p = s.position.towards(self.start_location, 10)
                            await self.build(SUPPLYDEPOT, p)


    async def buildbarracks(self):

        if self.units(BARRACKS).amount + 0 < 4 + self.units(COMMANDCENTER).amount - 1:
            cc = self.units(COMMANDCENTER).ready
            sd = self.units(SUPPLYDEPOT)
            if cc.exists and sd.exists:
                if self.can_afford(BARRACKS):
                    await self.build(BARRACKS, near=sd.random)

    async def buildrefinery(self):
        if self.units(BARRACKS).amount > 1 and self.units(REFINERY).amount <= 1:
            for cc in self.units(COMMANDCENTER).ready:
                v = self.state.vespene_geyser.closer_than(15.0, cc)
                for ve in v:
                    if self.can_afford(REFINERY):
                            if not self.units(REFINERY).closer_than(1,ve).exists:
                                worker = self.select_build_worker(ve.position)
                                if worker is None:
                                    break
                                await self.do(worker.build(REFINERY, ve))

    async def expand(self):
        if self.can_afford(COMMANDCENTER):
                if self.units(COMMANDCENTER).amount < 3:
                    await self.expand_now()



    async def trainmarine(self):
        if True:
            for b in self.units(BARRACKS).ready.noqueue:
                if self.can_afford(MARINE):
                    await self.do(b.train(MARINE))

    async def trainreaper(self):
        if True:
            for b in self.units(BARRACKS).ready.noqueue:
                if self.can_afford(REAPER):
                    await self.do(b.train(REAPER))

    async def reaperscout(self):
        if True:
            for r in self.units(REAPER):
                if len(self.known_enemy_structures)==0:
                    if r.is_idle:
                        #el = self.enemy_start_locations[0]
                        el = self.state.mineral_field.random.position
                        await self.do(r.attack(el))
                else:
                    if r.is_idle:
                        p = self.game_info.map_center.towards(self.known_enemy_structures.random.position, (self.supply_used)+4)
                        await self.do(r.attack(p))

    async def reapernotdie(self):
        if True:
            for r in self.units(REAPER):
                death = self.known_enemy_units.closer_than(3,  r)
                if death.exists:
                    p = r.position.towards(death[0].position,  -7)
                    await self.do(r.move(p))
                else:
                    if r.health_percentage < 5/7:
                        p = self.game_info.map_center.towards(self.enemy_start_locations[0], (self.supply_used)-10)
                        await self.do(r.move(p))

    async def flood(self):
        if True:
            if len(self.known_enemy_structures)>0:
               if self.units.idle.amount > 30:
                    for a in self.units(MARINE):
                        await self.do(a.attack(self.known_enemy_structures[0].position))
            else:
                if self.units.idle.amount > 80:
                    for a in self.units:
                        await self.do(a.attack(self.mineral_field.random.position))


"""TEST SCRIPT BELOW"""
"""
run_game(maps.get("Abyssal Reef LE"), [
    Bot(Race.Terran, MarineReaperBotEasy()),
    Computer(Race.Random, Difficulty.Easy)
], realtime=True)

run_game(maps.get("(2)16-Bit LE"), [
    Bot(Race.Terran, MarineReaperBotEasy()),
    Computer(Race.Random, Difficulty.Easy)
], realtime=True)
run_game(maps.get("(2)Acid Plant LE"), [
    Bot(Race.Terran, MarineReaperBotEasy()),
    Computer(Race.Random, Difficulty.Easy)
], realtime=True)
run_game(maps.get("Abyssal Reef LE"), [
    Bot(Race.Terran, MarineReaperBotEasy()),
    Computer(Race.Random, Difficulty.Easy)
], realtime=True)
run_game(maps.get("Odyssey LE"), [
    Bot(Race.Terran, MarineReaperBotEasy()),
    Computer(Race.Random, Difficulty.Easy)
], realtime=True)
run_game(maps.get("Proxima Station LE"), [
    Bot(Race.Terran, MarineReaperBotEasy()),
    Computer(Race.Random, Difficulty.Easy)
], realtime=True)"""