import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Base64;

public class ExecuteImageDetection {

    public static String s;
    public void runPython(byte [] dataKey, String dataValue ) throws IOException {
        String b64 = encodetoBase64(dataKey);
        String[] cmd = {
                "python",
                "/home/de/Project/detection.py",
                b64,
                dataValue
        };
        Runtime r =  Runtime.getRuntime();
        Process p = r.exec(cmd);
        BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
        while((s=in.readLine()) != null){
            System.out.println(s);
        }
    }

    private String encodetoBase64(byte [] iba){
        String encodedImage = Base64.getEncoder().encodeToString(iba);
        return encodedImage;
    }
}
