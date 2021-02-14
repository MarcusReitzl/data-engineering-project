import org.apache.commons.io.IOUtils;
import org.apache.commons.net.util.Base64;
import org.apache.spark.storage.StorageLevel;
import org.apache.spark.streaming.receiver.Receiver;
import org.json.JSONException;
import org.json.JSONObject;
import javax.imageio.*;
import javax.swing.*;
import java.awt.*;
import java.awt.image.RenderedImage;
import java.io.*;
import java.net.URL;

public class ImageReceiver extends Receiver<byte[]> {
    String urlPath = null;
    long intervalSeconds = 0;


    public ImageReceiver(String urlPath,long intervalSeconds){
        super(StorageLevel.MEMORY_AND_DISK_2());
        this.urlPath = urlPath;
        this.intervalSeconds = intervalSeconds;
    }

    @Override
    public void onStart() {
        // Start the thread that receives data over a connection
        new Thread(this::receiveImage).start();
    }

    @Override
    public void onStop() {
        // There is nothing much to do as the thread calling receive()
        // is designed to stop by itself if isStopped() returns false
    }
    private void receiveImage() {
        Image image = null;
        try {
            URL url = new URL(urlPath);
            image = ImageIO.read(url);

            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            ImageIO.write((RenderedImage) image, "jpg", baos);
            byte[] bytes = baos.toByteArray();

            //String imageString = new String(bytes "UTF-8");

            store(bytes);
            Thread.sleep(intervalSeconds *1000);
            restart("Trying to connect again");
        } catch (IOException | JSONException | InterruptedException e) {
            restart("Try like you have never caught before");
        }

    }
}
