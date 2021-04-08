package com.example.solar_powered_air_cooler;

import androidx.appcompat.app.AppCompatActivity;

import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

public class ManualModeActivity extends AppCompatActivity {
    BluetoothSocket btSocket = MainActivity.btSocket;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_manual_mode);
    }

    public void activateManualMode(View v){
        if(btSocket!=null) {

            MainActivity.sendMessageToServer("Activate Manual Mode!");
            String message = MainActivity.recvdMessageFromServer();
            Toast toast = Toast.makeText(this, message, Toast.LENGTH_LONG);
            toast.show();
        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_LONG);
            toast.show();
        }
    }

    public void fanSpeedUp(View v){
        if(btSocket!=null) {

            MainActivity.sendMessageToServer("Fan Speed Up!");
            String message = MainActivity.recvdMessageFromServer();
            Toast toast = Toast.makeText(this, message, Toast.LENGTH_LONG);
            toast.show();
        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_LONG);
            toast.show();
        }

    }

    public void fanSpeedDown(View v){
        if(btSocket!=null) {

            MainActivity.sendMessageToServer("Fan Speed Down!");
            String message = MainActivity.recvdMessageFromServer();
            Toast toast = Toast.makeText(this, message, Toast.LENGTH_LONG);
            toast.show();
        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_LONG);
            toast.show();
        }

    }

    public void humidIntensityUp(View v){
        if(btSocket!=null) {

            MainActivity.sendMessageToServer("Humidifier Intensity Up!");
            String message = MainActivity.recvdMessageFromServer();
            Toast toast = Toast.makeText(this, message, Toast.LENGTH_LONG);
            toast.show();
        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_LONG);
            toast.show();
        }

    }

    public void humidIntensityDown(View v){
        if(btSocket!=null) {

            MainActivity.sendMessageToServer("Humidifier Intensity Down!");
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