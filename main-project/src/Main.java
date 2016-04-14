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
    public static void main(String[] args) throws IOException {

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
                    body.matches("(?s).*```.{10,}```.*");



            if (containsCodeBlock && talksAboutErrors)
                 System.out.println(object.getString("title"));
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
