import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.URI;
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


//https://www.programcreek.com/java-api-examples/org.apache.hadoop.io.SequenceFile --Example 17
//https://hadoop.apache.org/docs/stable/api/index.html?org/apache/hadoop/io/BytesWritable.html


public class SequenceFileCreator
{
    public static void main(String[] args) throws IOException {

        String pathToRead = "/home/de/Project/archive/archive/cams/";
        //git spackt wenn i des in project ordner save
        //String outputPath = "/home/de/IdeaProjects/SequenceFile/sequenceFile";

        String outputPath = "/home/de/Project/sequenceFile";


        Configuration config = new Configuration();

        BytesWritable key = new BytesWritable();
        Text value = new Text();

        FileSystem fs = FileSystem.get(URI.create(outputPath), config);

        SequenceFile.Writer writer = null;

        try{
            writer = SequenceFile.createWriter(fs, config, new Path(outputPath), key.getClass(), value.getClass());
            final File dir = new File(pathToRead);
            for(final File imgFile : dir.listFiles()) {

                value.set(imgFile.getName());

                byte[] data = Files.readAllBytes(Paths.get(pathToRead+imgFile.getName()));

                key.set(data, 0, data.length);

                writer.append(key, value);
            }
        } finally {
            IOUtils.closeStream(writer);
        }

    }



    public static byte[] BytesFromImage(File img) throws IOException {
        BufferedImage bufferedImage = ImageIO.read(img);
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        if(bufferedImage!=null) {
            //remove alpha channel (rgba to rgb)
            BufferedImage result = new BufferedImage(bufferedImage.getWidth(), bufferedImage.getHeight(), BufferedImage.TYPE_INT_RGB);
            result.createGraphics().drawImage(bufferedImage, 0, 0, Color.BLACK, null);
            bufferedImage = result;

        }

        ImageIO.write(bufferedImage, "jpg", bos );
        return bos.toByteArray();
    }

}
