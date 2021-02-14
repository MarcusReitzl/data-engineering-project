import com.google.common.io.Closeables;

import org.apache.spark.SparkConf;
import org.apache.spark.storage.StorageLevel;
import org.apache.spark.streaming.Duration;
import org.apache.spark.streaming.api.java.JavaDStream;
import org.apache.spark.streaming.api.java.JavaPairDStream;
import org.apache.spark.streaming.api.java.JavaReceiverInputDStream;
import org.apache.spark.streaming.api.java.JavaStreamingContext;
import org.apache.spark.streaming.receiver.Receiver;
import scala.Tuple2;

import java.io.*;
import java.net.ConnectException;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.regex.Pattern;

import org.apache.commons.io.IOUtils;
import org.json.JSONException;
import org.json.JSONObject;


public class CustomReceiver extends Receiver<String> {

    String filepath = null;


    public CustomReceiver(String filepath) {
        super(StorageLevel.MEMORY_AND_DISK_2());
        this.filepath = filepath;

    }

    @Override
    public void onStart() {
        // Start the thread that receives data over a connection
        new Thread(this::readJson).start();
    }

    @Override
    public void onStop() {
        // There is nothing much to do as the thread calling receive()
        // is designed to stop by itself if isStopped() returns false
    }
    private void readJson() {

        try {
            File jsonFile = new File(filepath);
            InputStream is = new FileInputStream(jsonFile);
            String text = IOUtils.toString(is, "UTF-8");
            JSONObject myJsonObject = new JSONObject(text);
            store(myJsonObject.toString());
        } catch (IOException | JSONException e) {
            restart("Try like you have never caught before");
        }


    }
}