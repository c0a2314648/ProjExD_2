import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1600, 900
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRectまたは爆弾Rectの画面内外判定用の関数
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向判定結果, 縦方向判定結果 (True:画面内/Fase:画面外)
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def change_kk():  # 追加課題１
    """
    飛ぶ方向に従って画像を回転または反転するために用いる辞書を作製する関数
    戻り値：辞書の中身
    """
    k1 = pg.image.load("fig/3.png")
    k2 = pg.transform.flip(pg.image.load("fig/3.png"),True, False)
    k3 = pg.transform.flip(pg.image.load("fig/3.png"),False, True)
    return  {(-5, 0):pg.transform.rotozoom(k1, 0, 1.0),  # 左
             (-5, +5):pg.transform.rotozoom(k1, 45, 1.0),  # 左下
             (0,+5):pg.transform.rotozoom(k3, 90, 1.0),  # 下
             (+5, +5):pg.transform.rotozoom(k2, -45, 1.0),  # 右下
             (+5, 0):pg.transform.rotozoom(k2, 0, 1.0),  # 右
             (+5, -5):pg.transform.rotozoom(k2, 45, 1.0),  # 右上
             (0, -5):pg.transform.rotozoom(k3, 270, 1.0),  # 上
             (-5, -5):pg.transform.rotozoom(k1, 315, 1.0),  # 左上
             (0, 0):pg.transform.rotozoom(k1, 0, 1.0) }  # 常時
    


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img = pg.Surface((20,20))
    bd_img.set_colorkey((0,0,0))
    pg.draw.circle(bd_img, (255,0,0), (10,10), 10)
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    kk_mv = change_kk()

    clock = pg.time.Clock()
    tmr = 0
    key_dir = {pg.K_UP:(0,-5), pg.K_DOWN:(0,5), pg.K_LEFT:(-5,0), pg.K_RIGHT:(5,0)}
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct):  #こうかとん爆弾がぶつかったら
            print("Gsme Over")
            finish(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for i,j in key_dir.items():
            if key_lst[i]:
                sum_mv[0] += j[0]
                sum_mv[1] += j[1]
        kk_rct.move_ip(sum_mv)
        kk_img = kk_mv[tuple(sum_mv)]
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bd_rct.move_ip(vx, vy)
        screen.blit(bd_img, bd_rct)
        yoko, tate = check_bound(bd_rct)
        if not yoko:  # 横方向にはみ出てたら
            vx *= -1
        if not tate:  # 縦方向にはみ出てたら
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


def finish(screen:pg.Surface):  # 追加課題２
    back = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(back,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    back.set_alpha(200)
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    kk_cr = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    screen.blit(back, [0,0])
    screen.blit(txt, [650, 450])
    screen.blit(kk_cr, [500, 400])
    screen.blit(kk_cr, [1000, 400])
    pg.display.update()
    time.sleep(5)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
