package com.mygdx.game;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Input;
import com.badlogic.gdx.InputProcessor;
import com.badlogic.gdx.graphics.g2d.Sprite;

public class InputControllers implements InputProcessor {

    private Sprite sprite;
    int keycode;
    boolean bool = false;

    public InputControllers (Sprite sprite){
        this.sprite = sprite;
    }

    // Когда мы нажимаем кнопку. Возвращает, что было нажато
    @Override
    public boolean keyDown(int keycode) {
        System.out.println(keycode);
        this.keycode = keycode;
        bool = true;
        return true;
    }

    // Какую кнопку мы отпустили
    @Override
    public boolean keyUp(int keycode) {
        bool = false;
        return false;
    }

    // Какой символ набрали с клавиатуры
    @Override
    public boolean keyTyped(char character) {
        return false;
    }

    // Возвращает координаты нажатой области мышкой
    @Override
    public boolean touchDown(int screenX, int screenY, int pointer, int button) {
        return false;
    }

    // Возвращает координаты области, когда мы отжали мышку
    @Override
    public boolean touchUp(int screenX, int screenY, int pointer, int button) {
        return false;
    }

    // Зажали мышкой, водим по экрану и она возвращат нам постоянно новые координаты
    @Override
    public boolean touchDragged(int screenX, int screenY, int pointer) {
        return false;
    }

    // Двигаем мышкой и она постоянно возвращает нам координты
    @Override
    public boolean mouseMoved(int screenX, int screenY) {
        // Так задаются координаты для спрайта
//        sprite.setPosition(screenX, Gdx.graphics.getHeight() - screenY);
        return false;
    }

    // На сколько проскролили
    @Override
    public boolean scrolled(int amount) {
        return false;
    }

    public void update(){
        if (bool){
            if (keycode == Input.Keys.LEFT) sprite.setPosition(sprite.getX() - 10,
                    sprite.getY());
            if (keycode == Input.Keys.RIGHT) sprite.setPosition(sprite.getX() + 10,
                    sprite.getY());
            if (keycode == Input.Keys.UP) sprite.setPosition(sprite.getX(),
                    sprite.getY() + 10);
            if (keycode == Input.Keys.DOWN) sprite.setPosition(sprite.getX(),
                    sprite.getY() - 10);
        }

    }
}
