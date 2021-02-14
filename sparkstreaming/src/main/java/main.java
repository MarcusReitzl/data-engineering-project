import org.apache.commons.io.IOUtils;
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.Text;
import org.apache.spark.*;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.function.*;
import org.apache.spark.streaming.*;
import org.apache.spark.streaming.api.java.*;
import org.json.JSONArray;
import org.json.JSONObject;
import org.mortbay.util.ajax.JSON;
import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.core.Scalar;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;
import scala.Tuple2;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.awt.image.RenderedImage;
import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import javax.imageio.*;
import javax.swing.*;
import org.opencv.*;


public class main {

    public static void main(String[] args) throws InterruptedException, IOException {


        SparkConf conf = new SparkConf();
        conf.setAppName("ImageStreaming");
        JavaStreamingContext ssc = new JavaStreamingContext(conf, Durations.seconds(30));


        File jsonFile = new File("/home/de/Project/sources.json");
        InputStream is = new FileInputStream(jsonFile);
        String text = IOUtils.toString(is, "UTF-8");
        JSONObject jsonObject = new JSONObject(text);
        JSONArray cams = jsonObject.getJSONArray("cams");

        ExecuteImageDetection pyInstance = new ExecuteImageDetection();

        for (int i = 0; i < cams.length(); i++) {

            JSONObject cam = cams.getJSONObject(i);
            String url = cam.getString("url");
            String camId = cam.getString("camID");

            ImageReceiver receiver = new ImageReceiver(url,20);
            JavaReceiverInputDStream<byte[]> camStream = ssc.receiverStream(receiver);
            camStream.foreachRDD(imgRdd -> imgRdd.foreach(imgByteArr -> {

                pyInstance.runPython(imgByteArr,camId);



               /* BufferedImage img = createImageFromBytes(imgByteArr);

                Image outImg = imageProcessing(img);
                JFrame frame = new JFrame();
                frame.setSize(300, 300);
                JLabel label = new JLabel(new ImageIcon(outImg));
                frame.add(label);
                frame.setVisible(true);*/
            }));

        }




/*
        CustomReceiver receiver = new CustomReceiver("/home/de/testspark/sources.json");
        JavaReceiverInputDStream<String> json = ssc.receiverStream(receiver);
        CustomReceiver receiver2 = new CustomReceiver("/home/de/testspark/sources2.json");
        JavaReceiverInputDStream<String> json2= ssc.receiverStream(receiver2);
        json2.print();
        JavaDStream<String> camUrls = json.flatMap(j -> {

            JSONObject jObject = new JSONObject(j);
            JSONArray cams = jObject.getJSONArray("cams");

            String[] camurls = new String[cams.length()];

            for (int i = 0; i < cams.length()-1; i++) {

                JSONObject cam = cams.getJSONObject(i);
                camurls[i] = cam.getString("url");
            }
            return Arrays.stream(camurls).iterator();
        });
        camUrls.print();

*/
        ssc.start();
        ssc.awaitTermination();
       // ssc.stop();

    }

    private static BufferedImage createImageFromBytes(byte[] imageData) {
        ByteArrayInputStream bais = new ByteArrayInputStream(imageData);
        try {
            return ImageIO.read(bais);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static Mat BufferedImage2Mat(BufferedImage image) throws IOException {
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        ImageIO.write(image, "jpg", byteArrayOutputStream);
        byteArrayOutputStream.flush();
        return Imgcodecs.imdecode(new MatOfByte(byteArrayOutputStream.toByteArray()), Imgcodecs.CV_LOAD_IMAGE_UNCHANGED);
    }

    public static Image imageProcessing(BufferedImage inImg) throws Exception {
        // Loading the OpenCV core library


        // Reading the Image from the file and storing it in to a Matrix object
        Mat matrix = BufferedImage2Mat(inImg);

        // Drawing a Rectangle
        Imgproc.rectangle(
                matrix,                    //Matrix obj of the image
                new org.opencv.core.Point(130, 50),        //p1
                new org.opencv.core.Point(300, 280),       //p2
                new Scalar(0, 0, 255),     //Scalar object for color
                5                          //Thickness of the line
        );

        // Encoding the image
        MatOfByte matOfByte = new MatOfByte();
        Imgcodecs.imencode(".jpg", matrix, matOfByte);

        // Storing the encoded Mat in a byte array
        byte[] byteArray = matOfByte.toArray();

        // Displaying the image
        InputStream in = new ByteArrayInputStream(byteArray);
        BufferedImage bufImage = ImageIO.read(in);


        return bufImage;
    }


}
