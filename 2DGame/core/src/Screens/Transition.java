package Screens;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.graphics.g2d.Animation;
import com.badlogic.gdx.graphics.g2d.TextureRegion;
import com.mygdx.game.GifDecoder;
import com.mygdx.game.Start2d;

public class Transition implements Screen {

    Animation animation;
    float y;
    private int width = Gdx.graphics.getWidth();
    private int height = Gdx.graphics.getHeight();
    private Start2d game;
    private int i = 0;


    public Transition(Start2d game){
        this.game = game;

        for (; i > 6; i++){
            i += 1;

        }

    }

    @Override
    public void show() {

        animation = GifDecoder.loadGIFAnimation(Animation.PlayMode.LOOP,
                Gdx.files.internal("/Users/apple/IdeaProjects/test/core/assets/loading.gif").read());

    }

    @Override
    public void render(float delta) {
        y += Gdx.graphics.getDeltaTime() + 0.01;
        Gdx.gl.glClearColor(0, 0, 0, 1);
        Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT);



        game.batch.begin();

        game.batch.draw((TextureRegion) animation.getKeyFrame(y), width/3 + 40, height/2 - 40, 150, 100);


        game.batch.end();

        if (y > 12){
            game.setScreen(new LevelOne(game));
        }

    }

    @Override
    public void resize(int width, int height) {

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
