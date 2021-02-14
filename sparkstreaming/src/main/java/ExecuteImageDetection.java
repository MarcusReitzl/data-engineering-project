import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Serializable;
import java.util.Base64;

public class ExecuteImageDetection implements Serializable {

    public static String s;
    public void runPython(byte [] dataKey, String dataValue ) throws IOException {
        String b64 = encodetoBase64(dataKey);
        String[] cmd = {
                //"spark-submit --master spark://ubuntu:7077 imageProcessingService.py",
                "python3",
                //"/home/de/Project/detection.py",
                "/home/de/Project/processImageFromLiveData.py",
                b64,
                dataValue
        };
     //   System.out.println(b64);
        System.out.println(dataValue);
        Runtime r =  Runtime.getRuntime();
        Process p = r.exec(cmd);
        BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));

        while((s=in.readLine()) != null){
            System.out.println(s);
        }
        //BufferedReader stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));

        //System.out.println("Here is the standard error of the command (if any):\n");
        //while ((s = stdError.readLine()) != null) {
        //    System.out.println(s);
        //}
    }

    private String encodetoBase64(byte [] iba){
        String encodedImage = Base64.getEncoder().encodeToString(iba);
        return encodedImage;
    }
}
