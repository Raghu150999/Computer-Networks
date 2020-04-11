/* BeginGroupMembers */
/* f20170703@hyderabad.bits-pilani.ac.in B Raghunathan */
/* f20171573@hyderabad.bits-pilani.ac.in Gunpreet Kaur */
/* f20170325@hyderabad.bits-pilani.ac.in Nihal Jain */
/* f20170297@hyderabad.bits-pilani.ac.in S Ankit */
/* EndGroupMembers */

/* Program to access and download content from websites through a proxy server using socket level requests */

import java.net.Socket;
import java.net.UnknownHostException;
import java.io.*;
import java.util.Base64;
import javax.net.ssl.*;
import java.nio.charset.StandardCharsets;
import java.util.regex.*;
import java.nio.file.*;

class HttpProxyDownload {

    private Socket sock = null;
    private String url, ip, username, password, fhtml, flogo;
    private int port;

    /**
     * Initialize class variables using commandline args
     * 
     * @param argv
     */
    public HttpProxyDownload(String[] argv) {
        url = argv[0];
        if(!url.substring(0, 4).equals("www.")) {
            url = "www." + url;
        }
        ip = argv[1];
        username = argv[3];
        password = argv[4];
        fhtml = argv[5];
        flogo = argv[6];
        port = Integer.parseInt(argv[2]);
    }

    /**
     * Makes a HTTP GET request and writes the data content to file
     * 
     * @param get      URL for GET
     * @param filename filepath to save response data
     * @return 1: on sucess, 0: error
     */
    public int makeRequest(String get, String filename) {
        try {
            sock = new Socket(ip, port);

            // Encode credentials
            String encodedKey = username + ":" + password;
            encodedKey = Base64.getEncoder().encodeToString(encodedKey.getBytes("utf-8"));
            String address = url + ":" + 443;
            String req = 
                "CONNECT " + address + " HTTP/1.1\r\n" + 
                "host: " + address + "\r\n" + 
                "proxy-connection: keep-alive\r\n" + 
                "proxy-authorization: Basic " + encodedKey + "\r\n" + 
                "\r\n";
            // Send CONNECT request
            // System.out.print(req);
            OutputStream out = sock.getOutputStream();
            out.write(req.getBytes(StandardCharsets.UTF_8));

            // Response from proxy
            BufferedReader in = new BufferedReader(new InputStreamReader(sock.getInputStream()));
            in.readLine();
            in.readLine();

            req = 
                "GET " + get + " HTTP/1.1\r\n" + 
                "host: " + url + "\r\n" + 
                "connection: close\r\n" + 
                "\r\n";

            // System.out.print(req);
            // Wrap using SSL for HTTPS connection
            SSLSocketFactory factory = (SSLSocketFactory) SSLSocketFactory.getDefault();
            SSLSocket sslsock = (SSLSocket) factory.createSocket(sock, sock.getInetAddress().getHostAddress(),
                    sock.getPort(), true);
            out = sslsock.getOutputStream();
            out.write(req.getBytes(StandardCharsets.UTF_8));

            InputStream fin = sslsock.getInputStream();
            int r;
            int prev[] = new int[4];
            int crlf[] = new int[4];
            int cr = '\r', lf = '\n';
            for (int i = 0; i < 4; i++) {
                if (i % 2 == 0)
                    crlf[i] = cr;
                else
                    crlf[i] = lf;
                prev[i] = -1;
            }

            int found = 0;

            // Open file to write
            File f = new File(filename);
            f.createNewFile();
            OutputStream fout = new FileOutputStream(f);
            while ((r = fin.read()) != -1) {
                if (found == 1) {
                    // Data section
                    fout.write(r);
                } else {
                    // Header section
                    // System.out.print((char) r);
                }
                for (int i = 0; i < 3; i++)
                    prev[i] = prev[i + 1];
                prev[3] = r;
                int ok = 1;
                for (int i = 0; i < 4; i++)
                    if (prev[i] != crlf[i])
                        ok = 0;
                if (ok == 1)
                    found = 1;
            }
            fout.close();
            fin.close();
            out.close();
            sock.close();
            return 1;
        } catch (UnknownHostException u) {
            System.out.println(u);
        } catch (IOException i) {
            System.out.println(i);
        }
        return 0;
    }

    public String getfhtml() {
        return fhtml;
    }

    public String getflogo() {
        return flogo;
    }

    public static void main(String[] argv) {
        HttpProxyDownload hpd = new HttpProxyDownload(argv);

        // GET html doc
        hpd.makeRequest("/", hpd.getfhtml());

        String htmldoc = null;
        try {
            htmldoc = new String(Files.readAllBytes(Paths.get(hpd.getfhtml())));
        } catch (IOException i) {
            System.out.println(i);
        }

        // Search for logo src in html doc
        Pattern p = Pattern.compile("<img[^>]*src=[\"']([^\"^']*)", Pattern.CASE_INSENSITIVE);
        Matcher m = p.matcher(htmldoc);

        if (m.find()) {
            String imgsrc = m.group(1);
            // handle relative path image URLs
            if (!imgsrc.substring(0, 6).equals("https:"))
                imgsrc = "/" + imgsrc;
            // System.out.println(imgsrc);
            // GET logo
            hpd.makeRequest(imgsrc, hpd.getflogo());
        }
    }
}