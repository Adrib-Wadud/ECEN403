package com.example.solar_powered_air_cooler;

import androidx.appcompat.app.AppCompatActivity;

import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

public class PowerActivity extends AppCompatActivity {
    BluetoothSocket btSocket = MainActivity.btSocket;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_power);
    }

    public void getPowerData(View v){
        if(btSocket!=null) {

            MainActivity.sendMessageToServer("Get current bat_volt!");
            String bat_volt = MainActivity.recvdMessageFromServer();
            TextView bat_volt_text = (TextView) findViewById(R.id.bat_volt);
            bat_volt_text.setText(bat_volt);

            MainActivity.sendMessageToServer("Get current charge_amps!");
            String charge_amps = MainActivity.recvdMessageFromServer();
            TextView charge_amps_text = (TextView) findViewById(R.id.charge_amps);
            charge_amps_text.setText(charge_amps);

            MainActivity.sendMessageToServer("Get current pan_watts!");
            String pan_watts = MainActivity.recvdMessageFromServer();
            TextView pan_watts_text = (TextView) findViewById(R.id.pan_watts);
            pan_watts_text.setText(pan_watts);

            MainActivity.sendMessageToServer("Get current pan_amps!");
            String pan_amps = MainActivity.recvdMessageFromServer();
            TextView pan_amps_text = (TextView) findViewById(R.id.pan_amps);
            pan_amps_text.setText(pan_amps);
        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_SHORT);
            toast.show();
        }

        Toast toast = Toast.makeText(this, "Power button pressed!", Toast.LENGTH_SHORT);
        toast.show();

    }


}