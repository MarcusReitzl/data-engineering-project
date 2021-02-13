import java.util.Arrays;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.BytesWritable;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.function.VoidFunction;
import scala.Tuple2;


public class ReadFromHDFS {

    public static void main(String[] args) {

        ExecuteImageDetection pyInstance = new ExecuteImageDetection();
        String uri = "hdfs://localhost:9000/monk";


        SparkConf conf = new SparkConf();
        conf.setAppName("ProcessingHistoricalData");
        conf.setMaster("spark://ubuntu:7077");
        JavaSparkContext sc = new JavaSparkContext(conf);
        sc.addJar("/home/de/IdeaProjects/SequenceFile/out/artifacts/SequenceFile_jar/SequenceFile.jar");


        JavaPairRDD<Text, BytesWritable> dataset = sc.sequenceFile(uri,Text.class,BytesWritable.class,5);

      /*  dataset.foreach(tuple -> {

            Text key = tuple._1;
            BytesWritable value = tuple._2;

            byte [] imageAsByteArray = Arrays.copyOf(value.getBytes(), value.getLength());
            pyInstance.runPython(imageAsByteArray, key.toString());

        });*/

        dataset.foreach(new VoidFunction<Tuple2<Text, BytesWritable>>() {
            @Override
            public void call(Tuple2<Text, BytesWritable> tuple) throws Exception {
                Text key = tuple._1;
                BytesWritable value = tuple._2;

                byte [] imageAsByteArray = Arrays.copyOf(value.getBytes(), value.getLength());
                pyInstance.runPython(imageAsByteArray, key.toString());
            }
        });

    }


}
