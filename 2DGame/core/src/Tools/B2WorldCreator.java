package Tools;

import com.badlogic.gdx.maps.MapObject;
import com.badlogic.gdx.maps.objects.RectangleMapObject;
import com.badlogic.gdx.maps.tiled.TiledMap;
import com.badlogic.gdx.math.Rectangle;
import com.badlogic.gdx.physics.box2d.*;
import com.mygdx.game.Start2d;

public class B2WorldCreator {
    public B2WorldCreator(World world, TiledMap map){
        BodyDef bdef = new BodyDef();
        PolygonShape shape = new PolygonShape();
        FixtureDef fdef = new FixtureDef();
        Body body;

        // Create ground
        for(MapObject object : map.getLayers().get(2).getObjects().getByType(RectangleMapObject.class)) {
            Rectangle rec = ((RectangleMapObject) object).getRectangle();

            bdef.type = BodyDef.BodyType.StaticBody;
            bdef.position.set((rec.getX() + rec.getWidth() / 2) / Start2d.PPM, (rec.getY() + rec.getHeight() / 2) / Start2d.PPM);

            body = world.createBody(bdef);

            shape.setAsBox(rec.getWidth() / 2 / Start2d.PPM, rec.getHeight() / 2 / Start2d.PPM);
            fdef.shape = shape;
            body.createFixture(fdef);
        }

        //Create walls
        for(MapObject object : map.getLayers().get(3).getObjects().getByType(RectangleMapObject.class)) {
            Rectangle rec = ((RectangleMapObject) object).getRectangle();

            bdef.type = BodyDef.BodyType.StaticBody;
            bdef.position.set((rec.getX() + rec.getWidth() / 2) / Start2d.PPM, (rec.getY() + rec.getHeight() / 2) / Start2d.PPM);

            body = world.createBody(bdef);

            shape.setAsBox(rec.getWidth() / 2 / Start2d.PPM, rec.getHeight() / 2 / Start2d.PPM);
            fdef.shape = shape;
            body.createFixture(fdef);
        }


    }

}
