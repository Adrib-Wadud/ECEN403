package com.example.solar_powered_air_cooler;

import androidx.appcompat.app.AppCompatActivity;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.os.Bundle;
import android.view.View;
import android.content.Intent;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.UUID;

public class MainActivity extends AppCompatActivity {
    public static BluetoothSocket btSocket = null;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void launchAutoMode(View v){
        Intent i = new Intent(this,AutoModeActivity.class);
        startActivity(i);

    }


    public void launchManualMode(View v){
        Intent i = new Intent(this, ManualModeActivity.class);
        startActivity(i);
    }

    public void connectToPi(View v) throws IOException {

        BluetoothAdapter btAdapter = BluetoothAdapter.getDefaultAdapter();

        BluetoothDevice device = btAdapter.getRemoteDevice("B8:27:EB:FD:68:D8");

        UUID uuid = UUID.fromString("94f39d29-7d6d-437d-973b-fba39e49d4ee");
        btSocket = null;

        try{
             btSocket = device.createRfcommSocketToServiceRecord(uuid);
             btSocket.connect();
             if(btSocket.isConnected()){
                 Toast toast = Toast.makeText(this, "Connected", Toast.LENGTH_LONG);
                 toast.show();
                 TextView connected = (TextView)findViewById(R.id.textView10);
                 connected.setText("Yes");
             }
             else{
                 Toast toast = Toast.makeText(this, "Not Connected", Toast.LENGTH_LONG);
                 toast.show();
             }
        } catch (IOException e){
            Toast toast = Toast.makeText(this, "Cannot connect to Pi", Toast.LENGTH_LONG);
            e.printStackTrace();
        }




    }

    public void disconnectFromPi(View v){
        try {
            btSocket.close();
            TextView connected = (TextView)findViewById(R.id.textView10);
            connected.setText("No");
        } catch (IOException e) {
            e.printStackTrace();
        }
        Toast toast = Toast.makeText(this, "Disonnected", Toast.LENGTH_LONG);
    }

    public static void sendMessageToServer(String message){

        try{
            PrintWriter msg_out = new PrintWriter(btSocket.getOutputStream(), true);
            msg_out.println(message);

        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public static String recvdMessageFromServer(){
        byte[] buffer = new byte[1024];
        int bytes =0;
        try{
            InputStream msg_in = btSocket.getInputStream();
            bytes = msg_in.read(buffer);
        } catch (IOException e) {
            e.printStackTrace();
        }

        return new String(buffer, 0, bytes);
    }
}