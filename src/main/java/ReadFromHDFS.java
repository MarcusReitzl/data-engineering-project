import java.util.Arrays;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.BytesWritable;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaSparkContext;




public class ReadFromHDFS {

    public static void main(String[] args) {

        ExecuteImageDetection pyInstance = new ExecuteImageDetection();
        String uri = "hdfs://localhost:9000/monk";


        SparkConf conf = new SparkConf().setAppName("ProcessingHistoricalData").setMaster("local[11]");
        JavaSparkContext sc = new JavaSparkContext(conf);


        JavaPairRDD<Text, BytesWritable> dataset = sc.sequenceFile(uri,Text.class,BytesWritable.class,10);

        dataset.foreach(tuple -> {

            Text key = tuple._1;
            BytesWritable value = tuple._2;

            byte [] imageAsByteArray = Arrays.copyOf(value.getBytes(), value.getLength());
            pyInstance.runPython(imageAsByteArray, key.toString());

        });


    }


}
