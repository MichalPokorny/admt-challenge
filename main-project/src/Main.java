import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import org.json.*;

public class Main {
    private static boolean testPython() throws InterruptedException, IOException {

        Process p = Runtime.getRuntime().exec("python", new String[] { "pythonfile.py" });
        p.waitFor();

        return true;
    }
    public static void main(String[] args) throws IOException, InterruptedException {


        String mypyIssuesUrl = "https://api.github.com/repos/python/mypy/issues?per_page=100";
        URL mypyUrl = new URL(mypyIssuesUrl);

        String thaJson = getHttp(mypyUrl);

        JSONArray issues = new JSONArray(thaJson);
        for (int i = 0; i < issues.length(); i++)
        {
            JSONObject object = issues.getJSONObject(i);
            String body = object.getString("body").toLowerCase();

            boolean talksAboutErrors =
                    body.contains("error") ||
                    body.contains("bug")||
                    body.contains("fix");

            boolean containsCodeBlock =
                    body.matches("(?s).*```(.{10,})```.*");




            if (containsCodeBlock && talksAboutErrors) {
                System.out.println("[ISSUE] " + object.getString("title"));
                Pattern pattern = Pattern.compile("(?s)```([^`]{10,})```");
                Matcher matcher = pattern.matcher(body);
                int mi = 0;
                while (matcher.find()) {
                    mi++;
                    String thaCode = matcher.group(1);
                    if (thaCode.startsWith("python")) {
                        thaCode = thaCode.substring(6);
                        System.out.println(">> CODE >> " + thaCode.replace('\n', ' ').replace('\r', ' ') );
                    }


                }
            }
        }


        System.out.println();
    }
    public static String getHttp(URL url) throws IOException {
        URLConnection conn = url.openConnection();
        String pageText;
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream(), "UTF-8"))) {
            pageText = reader.lines().collect(Collectors.joining("\n"));
        }
        return pageText;
    }
}
