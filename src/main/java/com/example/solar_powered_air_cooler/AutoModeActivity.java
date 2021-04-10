package com.example.solar_powered_air_cooler;

import androidx.appcompat.app.AppCompatActivity;

import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;

public class AutoModeActivity extends AppCompatActivity {
    public BluetoothSocket btSocket = MainActivity.btSocket;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_auto_mode);
    }

    public void activateAutoMode(View v){

        if(btSocket!=null) {

                MainActivity.sendMessageToServer("Activate Auto Mode!");
                String message = MainActivity.recvdMessageFromServer();
                TextView mode_activated = (TextView)findViewById(R.id.textView22);
                mode_activated.setText("Auto mode activated");
                Toast toast = Toast.makeText(this, message, Toast.LENGTH_LONG);
                toast.show();
        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_LONG);
            toast.show();
        }

    }

    public void deactivateAutoMode(View v){
        if(btSocket!=null) {
            MainActivity.sendMessageToServer("Deactivate Auto Mode!");
            TextView mode_activated = (TextView)findViewById(R.id.textView22);
            mode_activated.setText("Auto mode not activated");
            String message = MainActivity.recvdMessageFromServer();
            Toast toast = Toast.makeText(this, message, Toast.LENGTH_LONG);
            toast.show();
        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_LONG);
            toast.show();
        }

    }


    public void temperatureUp(View v){

        if(btSocket!=null) {
            MainActivity.sendMessageToServer("Temperature Up!");
            String message = MainActivity.recvdMessageFromServer();
            Toast toast = Toast.makeText(this, message, Toast.LENGTH_LONG);
            toast.show();
        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_LONG);
            toast.show();
        }
    }

    public void temperatureDown(View v){

        if(btSocket!=null) {
            MainActivity.sendMessageToServer("Temperature Down!");
            String message = MainActivity.recvdMessageFromServer();
            Toast toast = Toast.makeText(this, message, Toast.LENGTH_LONG);
            toast.show();
        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_LONG);
            toast.show();
        }
    }

    public void humidityUp(View v){

        if(btSocket!=null) {
            MainActivity.sendMessageToServer("Humidity Up!");
            String message = MainActivity.recvdMessageFromServer();
            Toast toast = Toast.makeText(this, message, Toast.LENGTH_LONG);
            toast.show();

        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_LONG);
            toast.show();
        }
    }

    public void humidityDown(View v){

        if(btSocket!=null) {
            MainActivity.sendMessageToServer("Humidity Down!");
            String message = MainActivity.recvdMessageFromServer();
            Toast toast = Toast.makeText(this, message, Toast.LENGTH_LONG);
            toast.show();
        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_LONG);
            toast.show();
        }
    }
}
