package Screens;


import Scenes.Hud;
import com.badlogic.gdx.*;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.graphics.OrthographicCamera;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.Animation;
import com.badlogic.gdx.graphics.g2d.Animation.PlayMode;
import com.badlogic.gdx.graphics.g2d.Sprite;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.graphics.g2d.TextureRegion;
import com.badlogic.gdx.math.Vector3;
import com.mygdx.game.GifDecoder;
import com.mygdx.game.InputControllers;
import com.mygdx.game.Start2d;


public class MainGame extends ApplicationAdapter implements Screen {
    Start2d game;
    OrthographicCamera camera;
    Animation animation;

    int width = Gdx.graphics.getWidth();
    int height = Gdx.graphics.getHeight();
    float y;
    private Texture leftImg;
    InputControllers controller;
    private Sprite  playButton, exitButton, playButtonPresed, exitButtonPressed;


    SpriteBatch batch;
    private Hud hud;



    public MainGame(Start2d game){
        this.game = game;

        camera = new OrthographicCamera(width, height);
        camera.position.set(new Vector3(width/2, height/2, 0));

    }

    @Override
    public void show() {

        //game.setScreen(new LevelOne(this));


        batch = new SpriteBatch();

        animation = GifDecoder.loadGIFAnimation(PlayMode.LOOP,
                Gdx.files.internal("/Users/apple/IdeaProjects/test/core/assets/download.gif").read());

        leftImg = new Texture("/Users/apple/IdeaProjects/test/core/assets/illustration.png");
        playButton = new Sprite(new Texture("core/assets/Play .png"));
        exitButton = new Sprite(new Texture("core/assets/Exit .png"));
//        playButton = new Sprite(new Texture("core/assets/Play Selected.png"));
//        exitButton = new Sprite(new Texture("core/assets/Exit Selected.png"));
        playButton.setPosition((width/2)/2 + 5, (height/2));
        playButton.setSize(90, 30);
        exitButton.setPosition((width/2)/2 + 5, (height/2) - 50);
        exitButton.setSize(90, 30);

        controller = new InputControllers(playButton);


    }


    @Override
    public void render(float delta) {
        y += Gdx.graphics.getDeltaTime() + 0.2;

        Gdx.gl.glClearColor(0, 0, 0, 1);
        Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT);


        camera.update();
        game.batch.setProjectionMatrix(camera.combined);

        game.batch.begin();


        game.batch.draw((TextureRegion) animation.getKeyFrame(y), (width/2)/2 - 110, (height/2) + 80, 320,80);
        game.batch.draw(leftImg, width/2, 0, width/2, height);

        playButton.draw(game.batch);
        exitButton.draw(game.batch);



        game.batch.end();

        if (Gdx.input.justTouched()) {
            game.setScreen(new Transition(game));
            dispose();
        }

    }


    @Override
    public void pause() {

    }

    @Override
    public void resume() {

    }

    @Override
    public void hide() {

    }

    @Override
    public void dispose() {

    }




}
