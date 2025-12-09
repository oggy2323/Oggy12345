import os
import zipfile

# প্রজেক্টের মূল নাম
PROJECT_NAME = "CryptoVoiceTrackerPro"
PACKAGE_DIR = "com/cryptovoicetracker/pro"
APP_DIR = os.path.join(PROJECT_NAME, "app")
MAIN_DIR = os.path.join(APP_DIR, "src", "main")
JAVA_PATH = os.path.join(MAIN_DIR, "java", PACKAGE_DIR)
RES_LAYOUT_PATH = os.path.join(MAIN_DIR, "res", "layout")

# সমস্ত কোড এখানে ইনলাইন করা হয়েছে (আপনার চূড়ান্ত কোড)

# 1. AndroidManifest.xml
MANIFEST_XML = """
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.cryptovoicetracker.pro">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="Crypto Voice Tracker Pro"
        android:theme="@style/Theme.AppCompat.Light">

        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <service android:name=".CryptoService" 
                 android:foregroundServiceType="dataSync"
                 android:enabled="true" 
                 android:exported="false"/>
    </application>
</manifest>
"""

# 2. activity_main.xml
ACTIVITY_MAIN_XML = """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:background="#F5F5F5"
    android:padding="16dp">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Crypto Voice Tracker Pro"
        android:textSize="24sp"
        android:textStyle="bold"
        android:textColor="#333333"
        android:gravity="center"
        android:layout_marginBottom="20dp"/>

    <androidx.cardview.widget.CardView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginBottom="16dp"
        app:cardCornerRadius="12dp"
        app:cardElevation="4dp">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:padding="16dp"
            android:gravity="center_vertical">

            <Switch
                android:id="@+id/switchVoice"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="Voice Alerts"
                android:checked="true"
                android:textSize="16sp"/>

            <Button
                android:id="@+id/btnRefresh"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Refresh"
                /> 
        </LinearLayout>
    </androidx.cardview.widget.CardView>

    <ScrollView
        android:layout_width="match_parent"
        android:layout_height="match_parent">
        
        <LinearLayout
            android:id="@+id/containerCoins"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical">
            <TextView android:id="@+id/txtLog" 
                      android:layout_width="match_parent" 
                      android:layout_height="wrap_content" 
                      android:text="Service Status: Waiting..."
                      android:layout_marginTop="10dp"/>
        </LinearLayout>
    </ScrollView>
</LinearLayout>
"""

# 3. MainActivity.java
MAIN_ACTIVITY_JAVA = """
package com.cryptovoicetracker.pro;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.Switch;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;
import java.util.HashMap;
import java.util.Locale;

public class MainActivity extends AppCompatActivity {

    private LinearLayout containerCoins;
    private Switch switchVoice;
    private Button btnRefresh;
    private HashMap<String, TextView> priceViews = new HashMap<>();
    private HashMap<String, TextView> changeViews = new HashMap<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        containerCoins = findViewById(R.id.containerCoins);
        switchVoice = findViewById(R.id.switchVoice);
        btnRefresh = findViewById(R.id.btnRefresh);

        createCoinCard("Bitcoin");
        createCoinCard("Ethereum");
        createCoinCard("BNB");
        createCoinCard("Solana");
        createCoinCard("Doge");

        Intent serviceIntent = new Intent(this, CryptoService.class);
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            startForegroundService(serviceIntent);
        } else {
            startService(serviceIntent);
        }

        switchVoice.setOnCheckedChangeListener((buttonView, isChecked) -> {
            Intent intent = new Intent(this, CryptoService.class);
            intent.putExtra("VOICE_ENABLE", isChecked);
            startService(intent);
        });

        btnRefresh.setOnClickListener(v -> {
            stopService(new Intent(this, CryptoService.class));
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                startForegroundService(new Intent(this, CryptoService.class));
            } else {
                startService(new Intent(this, CryptoService.class));
            }
        });
    }

    private void createCoinCard(String coinName) {
        CardView card = new CardView(this);
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        params.setMargins(0, 0, 0, 20);
        card.setLayoutParams(params);
        card.setRadius(15);
        card.setCardElevation(5);
        card.setContentPadding(30, 30, 30, 30);

        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);

        TextView name = new TextView(this);
        name.setText(coinName);
        name.setTextSize(18);
        name.setTextColor(Color.BLACK);

        TextView price = new TextView(this);
        price.setText("Loading...");
        price.setTextSize(20);
        price.setTypeface(null, android.graphics.Typeface.BOLD);

        TextView change = new TextView(this);
        change.setText("Wait for update...");
        
        layout.addView(name);
        layout.addView(price);
        layout.addView(change);
        card.addView(layout);

        containerCoins.addView(card);
        
        priceViews.put(coinName, price);
        changeViews.put(coinName, change);
    }

    private BroadcastReceiver updateReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String name = intent.getStringExtra("coin");
            double price = intent.getDoubleExtra("price", 0);
            double change = intent.getDoubleExtra("change", 0);

            if (priceViews.containsKey(name)) {
                priceViews.get(name).setText("$" + String.format(Locale.US, "%,.2f", price));
                
                TextView changeView = changeViews.get(name);
                changeView.setText(String.format(Locale.US, "%.2f%%", change));
                
                if (change >= 0) {
                    changeView.setTextColor(Color.parseColor("#4CAF50"));
                } else {
                    changeView.setTextColor(Color.parseColor("#F44336"));
                }
            }
            
            TextView logView = findViewById(R.id.txtLog);
            if (logView != null) {
                logView.setText("Service Status: Prices Updated at " + java.text.DateFormat.getTimeInstance(java.text.DateFormat.MEDIUM).format(new java.util.Date()));
            }
        }
    };

    @Override
    protected void onResume() {
        super.onResume();
        registerReceiver(updateReceiver, new IntentFilter("UPDATE_UI"));
    }

    @Override
    protected void onPause() {
        super.onPause();
        unregisterReceiver(updateReceiver);
    }
}
"""

# 4. CryptoService.java
CRYPTO_SERVICE_JAVA = """
package com.cryptovoicetracker.pro;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.speech.tts.TextToSpeech;
import androidx.core.app.NotificationCompat;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Locale;

public class CryptoService extends Service implements TextToSpeech.OnInitListener {

    private Handler handler = new Handler();
    private TextToSpeech tts;
    private boolean isVoiceEnabled = true;
    private final int INTERVAL = 10 * 60 * 1000; 
    
    private final String API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin,solana,dogecoin&vs_currencies=usd";
    
    @Override
    public void onCreate() {
        super.onCreate();
        tts = new TextToSpeech(this, this);
        startForegroundService();
        startTracking();
    }

    private void startForegroundService() {
        String CHANNEL_ID = "CryptoChannel";
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(CHANNEL_ID, "Crypto Service", NotificationManager.IMPORTANCE_LOW);
            getSystemService(NotificationManager.class).createNotificationChannel(channel);
        }

        Notification notification = new NotificationCompat.Builder(this, CHANNEL_ID)
                .setContentTitle("Crypto Voice Tracker Pro")
                .setContentText("Tracking prices in background...")
                .setSmallIcon(android.R.drawable.ic_menu_rotate)
                .build();

        startForeground(1, notification);
    }

    private void startTracking() {
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                fetchPrices();
                handler.postDelayed(this, INTERVAL);
            }
        }, 0);
    }

    private void fetchPrices() {
        new Thread(() -> {
            try {
                URL url = new URL(API_URL);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                
                BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) response.append(line);
                reader.close();

                processData(new JSONObject(response.toString()));

            } catch (Exception e) {
                e.printStackTrace();
            }
        }).start();
    }

    private void processData(JSONObject json) {
        SharedPreferences prefs = getSharedPreferences("CryptoData", MODE_PRIVATE);
        SharedPreferences.Editor editor = prefs.edit();

        String[] coins = {"bitcoin", "ethereum", "binancecoin", "solana", "dogecoin"};
        String[] names = {"Bitcoin", "Ethereum", "BNB", "Solana", "Doge"};

        StringBuilder speechText = new StringBuilder();

        for (int i = 0; i < coins.length; i++) {
            String id = coins[i];
            String name = names[i];

            if (json.has(id)) {
                double newPrice = json.getJSONObject(id).getDouble("usd");
                float oldPrice = prefs.getFloat(id, 0);

                if (oldPrice != 0) {
                    double change = ((newPrice - oldPrice) / oldPrice) * 100;
                    
                    String direction = change >= 0 ? "up" : "down";
                    String percent = String.format(Locale.US, "%.2f", Math.abs(change));
                    
                    speechText.append(name).append(" is ").append(direction).append(" ").append(percent).append(" percent. ");
                }

                editor.putFloat(id, (float) newPrice);
                
                Intent intent = new Intent("UPDATE_UI");
                intent.putExtra("coin", name);
                intent.putExtra("price", newPrice);
                intent.putExtra("change", oldPrice == 0 ? 0 : ((newPrice - oldPrice) / oldPrice) * 100);
                sendBroadcast(intent);
            }
        }
        editor.apply();

        if (isVoiceEnabled && speechText.length() > 0) {
            speak(speechText.toString());
        }
    }

    private void speak(String text) {
        if (tts != null) {
            tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, null);
        }
    }

    @Override
    public void onInit(int status) {
        if (status == TextToSpeech.SUCCESS) {
            tts.setLanguage(Locale.US);
        }
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (intent != null && intent.hasExtra("VOICE_ENABLE")) {
            isVoiceEnabled = intent.getBooleanExtra("VOICE_ENABLE", true);
        }
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) { return null; }
    
    @Override
    public void onDestroy() {
        if(tts != null) { tts.stop(); tts.shutdown(); }
        super.onDestroy();
    }
}
"""

# 5. app/build.gradle
APP_BUILD_GRADLE = """
apply plugin: 'com.android.application'

android {
    compileSdkVersion 29
    defaultConfig {
        applicationId "com.cryptovoicetracker.pro"
        minSdkVersion 23
        targetSdkVersion 29
        versionCode 1
        versionName "1.0"
    }
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}

dependencies {
    implementation fileTree(dir: 'libs', include: ['*.jar'])

    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.9.0'
    implementation 'androidx.cardview:cardview:1.0.0'
    
    // Test dependencies removed for simplicity in cloud build
}
"""

# 6. Project-level build.gradle
PROJECT_BUILD_GRADLE = """
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:4.2.2'
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
"""

# 7. settings.gradle
SETTINGS_GRADLE = """
rootProject.name = "CryptoVoiceTrackerPro"
include ':app'
"""

def create_and_write_file(filepath, content):
    """Creates directory if necessary and writes content to the file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content.strip())
    print(f"Created: {filepath}")

def create_zip_file(folder_to_zip, zip_filename):
    """Creates a zip file of the specified folder."""
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_to_zip):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, os.path.dirname(folder_to_zip))
                    zipf.write(full_path, arcname)
        print(f"\n✅ SUCCESS: Project zipped to {zip_filename}")
        print("Now upload this ZIP file to GitHub!")
    except Exception as e:
        print(f"Error zipping files: {e}")

# --- প্রধান ফাংশন ---
def generate_android_project_zip():
    # 1. ফাইল তৈরি করা
    create_and_write_file(os.path.join(MAIN_DIR, "AndroidManifest.xml"), MANIFEST_XML)
    create_and_write_file(os.path.join(RES_LAYOUT_PATH, "activity_main.xml"), ACTIVITY_MAIN_XML)
    create_and_write_file(os.path.join(JAVA_PATH, "MainActivity.java"), MAIN_ACTIVITY_JAVA)
    create_and_write_file(os.path.join(JAVA_PATH, "CryptoService.java"), CRYPTO_SERVICE_JAVA)
    create_and_write_file(os.path.join(APP_DIR, "build.gradle"), APP_BUILD_GRADLE)
    create_and_write_file(os.path.join(PROJECT_NAME, "build.gradle"), PROJECT_BUILD_GRADLE)
    create_and_write_file(os.path.join(PROJECT_NAME, "settings.gradle"), SETTINGS_GRADLE)

    # 2. .gitignore ফাইল যোগ করা (Gitpod/Codespaces এর জন্য প্রয়োজন হতে পারে)
    create_and_write_file(os.path.join(PROJECT_NAME, ".gitignore"), "build/\n.gradle/\nlocal.properties\n*.apk\n")
    
    # 3. ZIP তৈরি করা
    zip_filename = f"{PROJECT_NAME}_GitHub_Upload.zip"
    create_zip_file(PROJECT_NAME, zip_filename)

if __name__ == "__main__":
    generate_android_project_zip()

