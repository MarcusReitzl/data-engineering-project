import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.net.URISyntaxException;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.apache.commons.io.output.ByteArrayOutputStream;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;
import org.apache.hadoop.io.SequenceFile;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.BytesWritable;



import javax.imageio.ImageIO;


public class ReadFromHDFS {
    public static void main(String[] args) throws IOException, URISyntaxException {
        String uri = "hdfs://localhost:9000/imagefiles";
        Configuration config  = new Configuration();
        Path path = new Path(uri);
        SequenceFile.Reader reader = null;
        //InputStream in = null;
        FileSystem filesystem = FileSystem.get(new URI(uri), config);

        try{
            reader = new SequenceFile.Reader(config, SequenceFile.Reader.file(path));

            Text value = new Text();
            BytesWritable key = new BytesWritable();

            while(reader.next(key, value)){
                System.out.println("key: "+key+"value: "+value);
            }
            //in = filesystem.open(path);
            //IOUtils.copyBytes(in, System.out, 4096, false);
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            reader.close();
        }
    }
}
