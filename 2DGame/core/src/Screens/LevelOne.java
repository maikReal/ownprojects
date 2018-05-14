package Screens;

import Sprites.Player;
import Tools.B2WorldCreator;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Input;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.audio.Music;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.graphics.OrthographicCamera;
import com.badlogic.gdx.maps.tiled.TiledMap;
import com.badlogic.gdx.maps.tiled.TmxMapLoader;
import com.badlogic.gdx.maps.tiled.renderers.OrthogonalTiledMapRenderer;
import com.badlogic.gdx.math.Vector2;
import com.badlogic.gdx.physics.box2d.*;
import com.badlogic.gdx.utils.viewport.FitViewport;
import com.badlogic.gdx.utils.viewport.Viewport;
import com.mygdx.game.Start2d;

public class LevelOne implements Screen {

    private Start2d game;
    private OrthographicCamera gamecam;
    private Viewport gamePort;

    // TiledMapVariables
    private TmxMapLoader mapLoader;
    private TiledMap map;
    private OrthogonalTiledMapRenderer renderer;

    // Box2dVariables
    private World world;
    private Box2DDebugRenderer b2dr;

    private Player player;

    private BodyDef bDef;
    private Body body;

//    private Music music;


    public LevelOne(Start2d game) {

        this.game = game;
        gamecam = new OrthographicCamera();
        gamePort = new FitViewport(Start2d.V_WIDTH / Start2d.PPM, Start2d.V_HEIGHT / Start2d.PPM, gamecam);


        mapLoader = new TmxMapLoader();
        map = mapLoader.load("/Users/apple/IdeaProjects/test/core/assets/editedmap.tmx");
        renderer = new OrthogonalTiledMapRenderer(map, 1 / Start2d.PPM);

        gamecam.position.set(gamePort.getWorldWidth() / 2, gamePort.getWorldHeight() / 2, 0);

        world = new World(new Vector2(0, -10), true);
        b2dr = new Box2DDebugRenderer();

        player = new Player(world);
        new B2WorldCreator(world, map);

//        music = Gdx.audio.newMusic(Gdx.files.internal("core/music/song.mp3"));
//        music.setLooping(true);
//        music.setVolume(0.3f);
//        music.play();




    }


    @Override
    public void show() {

    }

    public void handleInput(float dt){
        if (Gdx.input.isKeyJustPressed(Input.Keys.UP))
            player.b2body.applyLinearImpulse(new Vector2(0 ,4.5f), player.b2body.getWorldCenter(), true);
        if (Gdx.input.isKeyPressed(Input.Keys.RIGHT) && player.b2body.getLinearVelocity().x <= 2)
            player.b2body.applyLinearImpulse(new Vector2(0.1f ,0), player.b2body.getWorldCenter(), true);
        if (Gdx.input.isKeyPressed(Input.Keys.LEFT) && player.b2body.getLinearVelocity().x <= 2)
            player.b2body.applyLinearImpulse(new Vector2(-0.1f ,0), player.b2body.getWorldCenter(), true);

        if (Gdx.input.isKeyJustPressed(Input.Keys.RIGHT))
            player.setPosition(player.getX() + 0.1f, player.getY());


    }

    public void update(float dt){
        handleInput(dt);

        world.step(1/60f, 6, 2);
        gamecam.position.x = player.b2body.getPosition().x;
        //gamecam.position.x = player.getX();


        gamecam.update();
        renderer.setView(gamecam);
    }



    @Override
    public void render(float delta) {
        update(delta);

        Gdx.gl.glClearColor(0, 0, 0, 1);
        Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT);


        renderer.render();


        game.batch.setProjectionMatrix(gamecam.combined);

        b2dr.render(world, gamecam.combined);

        if (Gdx.input.isKeyPressed(Input.Keys.ESCAPE)){
            game.setScreen(new Pause(game));
            pause();
        }


        if (gameOver()){
            game.setScreen(new GameOverScreen(game));
            dispose();
        }




    }

    public boolean gameOver(){
        if(player.b2body.getPosition().y < -1){
            return true;
        }
        return false;
    }


    @Override
    public void resize(int width, int height) {
        gamePort.update(width, height);
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
        map.dispose();
        renderer.dispose();
        world.dispose();
        b2dr.dispose();

    }
}