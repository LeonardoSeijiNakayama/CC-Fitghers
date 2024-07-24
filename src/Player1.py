import pygame



class Player1():
    def __init__(self, player, x, y, flip, sprite_sheet, info, animacao_sprites):
        self.player = player
        self.tam = info[0]
        self.img_escala = info[1]
        self.offset = info[2]
        self.flip = flip
        self.lista_animacao = self.carrega_imagens(sprite_sheet, animacao_sprites)
        self.acao = 0
        self.indice_frame = 0
        self.image = self.lista_animacao[self.acao][self.indice_frame]
        self.tempo_att = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, 80, 128)
        self.vel_y = 0
        self.correndo = False
        self.pulando = False
        self.tipoAtaque = 0
        self.cooldownAtaque = 0
        self.hit = False
        self.atacando = False
        self.vida = 100
        self.vivo = True
        
    def carrega_imagens(self, sprite_sheet, animacao_sprites):
        #extraindo as imagens do spritesheet individualmente
        lista_animacao = []
        for y, animacao in enumerate(animacao_sprites):
            lista_temp_img = []
            for i in range(animacao):
                temp_img = sprite_sheet.subsurface(i * self.tam, y * self.tam, self.tam, self.tam)
                lista_temp_img.append(pygame.transform.scale(temp_img, (self.tam * self.img_escala, self.tam * self.img_escala)))
            lista_animacao.append(lista_temp_img)
        return lista_animacao
    
        
    def move(self, LARGURA_TELA, ALTURA_TELA, surface, target):
        
        VELOCIDADE = 8
        GRAVIDADE = 2
        dx = 0
        dy = 0
        self.correndo = False
        self.tipoAtaque = 0
        
        
        #get keys-------------------------------------------------------------------------------------------------------------------------------------------
        key = pygame.key.get_pressed()
        
        if self.vivo == True:
            
            if self.atacando == False: 
                #checa os controles do p1
                if self.player == 1: 
                #movimento--------------------------------------------------------------------------------------------------------------------------------------
                    if key[pygame.K_a]:
                        dx = -VELOCIDADE
                        self.correndo = True
                    if key[pygame.K_d]:
                        dx = VELOCIDADE
                        self.correndo = True
                    if key[pygame.K_w] and self.pulando == False:
                        self.vel_y = -30
                        self.pulando = True
                        
                    #ataque------------------------------------------------------------------------------------------------------------------------------------------------
                    if key[pygame.K_t] or key[pygame.K_r]:
                        self.ataque(surface, target)
                        if key[pygame.K_r]:
                            self.tipoAtaque = 1
                        if key[pygame.K_t]:
                            self.tipoAtaque = 2
                            
                #checa os controles do p2=================================================================================================================================
                if self.player == 2: 
                #movimento--------------------------------------------------------------------------------------------------------------------------------------
                    if key[pygame.K_LEFT]:
                        dx = -VELOCIDADE
                        self.correndo = True
                    if key[pygame.K_RIGHT]:
                        dx = VELOCIDADE
                        self.correndo = True
                    if key[pygame.K_UP] and self.pulando == False:
                        self.vel_y = -30
                        self.pulando = True
                        
                    #ataque------------------------------------------------------------------------------------------------------------------------------------------------
                    if key[pygame.K_k] or key[pygame.K_l]:
                        self.ataque(surface, target)
                        if key[pygame.K_k]:
                            self.tipoAtaque = 1
                        if key[pygame.K_l]:
                            self.tipoAtaque = 2
                            
                            
            
                
        
        #aplicando gravidade---------------------------------------------------------------------------------------------------------
        self.vel_y += GRAVIDADE
        dy += self.vel_y
            
        #mantem player dentro da janela---------------------------------------------------------------------------------------------
        if self.rect.left + dx < 0:
            dx = -self.rect.left
            
        if self.rect.right + dx > LARGURA_TELA:
            dx = LARGURA_TELA - self.rect.right
            
        if self.rect.bottom + dy > ALTURA_TELA-128:
            self.vel_y = 0
            dy = ALTURA_TELA - 128 - self.rect.bottom
            self.pulando = False;
            
        #mantem players olhando um para o outro-----------------------------------------------------------------------------------------------------------------------------------
        if self.vivo == True:
            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True
            
        #aplica cooldown dos ataques
        if self.cooldownAtaque > 0:
            self.cooldownAtaque -= 1
        
        #atualiza posicao-----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.rect.x += dx
        self.rect.y += dy
    
    #atualiza animacao 
    def update(self):
        #checa as acoes do player
        if self.vida <=0:
            self.vida = 0
            self.vivo = False
            self.att_acao(6)
        elif self.hit == True:
            self.att_acao(5)
        elif self.atacando == True:
            if self.tipoAtaque == 1:
                self.att_acao(3)
            elif self.tipoAtaque == 2:
                self.att_acao(4)
                
        elif self.pulando == True:
            self.att_acao(2)
            
        elif self.correndo == True:
            self.att_acao(1)
            
        else:
            self.att_acao(0)
        
        cooldown_animacao = 70
        self.image = self.lista_animacao[self.acao][self.indice_frame]
        if pygame.time.get_ticks() - self.tempo_att > cooldown_animacao:
            self.indice_frame += 1
            self.tempo_att = pygame.time.get_ticks()
        #checa se a animacao acabou
        if self.indice_frame >= len(self.lista_animacao[self.acao]):
            #checa se o player esta morto, se estiver termina a animacao
            if self.vivo == False:
                self.indice_frame = len(self.lista_animacao[self.acao]) - 1
            else:
                self.indice_frame = 0
                #checa se o ataque terminou
                if self.acao == 3 or self.acao == 4:
                    self.atacando = False
                    self.cooldownAtaque = 20
                #checa se tomou um ataque
                if self.acao == 5:
                    self.hit = False
                    #checa se o player estava atacando enquanto foi atacado
                    self.atacando = False
                    self.cooldownAtaque = 20
        
        
    def ataque(self, surface, target):
        if self.cooldownAtaque == 0:
            self.atacando = True;
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2*self.rect.width, self.rect.height)
            if(attacking_rect.colliderect(target.rect)):
                target.vida -= 10
                target.hit = True
            #pygame.draw.rect(surface,(0, 255, 0), attacking_rect)
        
    def att_acao(self, nova_acao):
        #checa se a nova acao e dieferente da anterior
        if nova_acao != self.acao:
            self.acao = nova_acao
            #atualiza a animacao do comeco
            self.indice_frame = 0
            self.tempo_att = pygame.time.get_ticks()
        
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.img_escala), self.rect.y - (self.offset[1] * self.img_escala)))
        