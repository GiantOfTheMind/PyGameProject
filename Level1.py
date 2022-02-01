import pygame
from Tiles import Tile
from Player import Player
from Exit import Exit
from Coins import Coin


tile_size = 64


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

        self.score = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        self.player = pygame.sprite.GroupSingle()

        self.exit = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == 'X':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                if cell == 'E':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    exit1 = Exit((x, y), tile_size)
                    self.exit.add(exit1)
                if cell == 'C':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    coin = Coin((x, y), tile_size)
                    self.coins.add(coin)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def coin_collect(self):
        player = self.player.sprite

        if pygame.sprite.spritecollide(player, self.coins, True):
            self.score += 100


    def exit_collision(self):
        player = self.player.sprite

        if pygame.sprite.spritecollide(player, self.exit, False):
            return True
        return False

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        self.exit.update(self.world_shift)
        self.exit.draw(self.display_surface)

        self.coins.draw(self.display_surface)

        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.coin_collect()

        self.player.draw(self.display_surface)

        if self.exit_collision():
            return False, self.score
        return True, self.score





