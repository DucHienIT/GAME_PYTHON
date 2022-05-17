if event.type == self.goku_stop:
            
            if self.PLAYER.isAttack == False:
                if self.PLAYER.isRun == False:
                    self.PLAYER.animationStop()
                    self.PLAYER.isAttack = False
                    self.PLAYER.comboCount = 0
                else:
                    self.PLAYER.animationRun()
        
            else:
                self.PLAYER.animationAttack()
            if self.MonsterInDisplay:
                for monster in self.MONSTERs:
                    monster.animationRun()