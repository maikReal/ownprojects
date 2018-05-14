package com.mygdx.game;

import Screens.MainGame;
import com.badlogic.gdx.Game;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.assets.AssetManager;
import com.badlogic.gdx.audio.Music;
import com.badlogic.gdx.audio.Sound;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;

public class Start2d extends Game {

	public SpriteBatch batch;
	public static final int V_WIDTH = 300;
	public static final int V_HEIGHT = 220;
	public static final float PPM = 100;
    private Music music;


	@Override
	public void create () {
		batch = new SpriteBatch();

        music = Gdx.audio.newMusic(Gdx.files.internal("core/music/song.mp3"));
        music.setLooping(true);
        music.setVolume(0.3f);
        music.play();


		setScreen(new MainGame(this));
	}


    @Override
	public void render () {
		super.render();

	}

}
